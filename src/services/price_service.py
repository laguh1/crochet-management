"""
Price calculation service.

Calculates suggested prices based on:
- Material cost (yarn prices)
- Labor cost (work hours × hourly rate)
- Stitch complexity factor
- Piece size factor
- Profit margin
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Tuple, Dict, Any

from ..config import config
from .data_service import DataService


@dataclass
class PriceConfig:
    """Configuration for price calculations."""
    hourly_rate: Decimal = Decimal("8.00")
    profit_margin: Decimal = Decimal("0.20")
    min_margin: Decimal = Decimal("0.10")
    round_to: int = 5  # Round to nearest N euros


@dataclass
class PriceBreakdown:
    """Detailed breakdown of a price calculation."""
    material_cost: Decimal
    labor_cost: Decimal
    subtotal: Decimal
    complexity_factor: Decimal
    size_factor: Decimal
    complexity_adjustment: Decimal
    adjusted_subtotal: Decimal
    profit_amount: Decimal
    total: Decimal
    rounded_price: Decimal

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display/JSON."""
        return {
            "material_cost": float(self.material_cost),
            "labor_cost": float(self.labor_cost),
            "subtotal": float(self.subtotal),
            "complexity_factor": float(self.complexity_factor),
            "size_factor": float(self.size_factor),
            "complexity_adjustment": float(self.complexity_adjustment),
            "adjusted_subtotal": float(self.adjusted_subtotal),
            "profit_amount": float(self.profit_amount),
            "total": float(self.total),
            "rounded_price": float(self.rounded_price),
        }


class PriceService:
    """Calculate suggested prices for pieces."""

    def __init__(self, price_config: PriceConfig = None, data_service: DataService = None):
        self.price_config = price_config or PriceConfig()
        self.data_service = data_service or DataService()

    def calculate_material_cost(self, piece_id: str) -> Decimal:
        """
        Calculate total material cost from yarns_used.

        Returns:
            Sum of (yarn.price_paid × quantity) for each yarn used.
        """
        piece = self.data_service.get_piece_by_id(piece_id)
        if not piece:
            return Decimal("0")

        total = Decimal("0")
        for yarn_id in piece.yarns_used:
            yarn = self.data_service.get_yarn_by_id(yarn_id)
            if yarn and yarn.price_paid:
                # Assume 1 ball used per yarn entry unless specified otherwise
                # Future: support yarns_used as objects with quantity
                total += yarn.price_paid

        return total

    def calculate_labor_cost(self, piece_id: str) -> Decimal:
        """
        Calculate labor cost from work hours.

        Returns:
            work_hours × hourly_rate
        """
        piece = self.data_service.get_piece_by_id(piece_id)
        if not piece:
            return Decimal("0")

        hours = piece.calculate_total_hours()
        return Decimal(str(hours)) * self.price_config.hourly_rate

    def get_complexity_factor(self, piece_id: str) -> Decimal:
        """
        Calculate complexity factor based on stitches used.

        Returns:
            Average complexity factor of all stitches used.
        """
        piece = self.data_service.get_piece_by_id(piece_id)
        if not piece or not piece.stitches_used:
            return Decimal("1.0")

        factors = []
        for stitch_id in piece.stitches_used:
            stitch = self.data_service.get_stitch_by_id(stitch_id)
            if stitch:
                category = stitch.category or "basic"
                factor = config.STITCH_COMPLEXITY.get(category, Decimal("1.0"))
                factors.append(factor)

        if not factors:
            return Decimal("1.0")

        return sum(factors) / len(factors)

    def get_size_factor(self, piece_type: str) -> Decimal:
        """
        Get size adjustment factor for piece type.

        Returns:
            Size factor from config (default 1.0).
        """
        return config.SIZE_FACTORS.get(piece_type, Decimal("1.0"))

    def calculate_price(self, piece_id: str) -> PriceBreakdown:
        """
        Calculate full price breakdown for a piece.

        Formula:
        1. subtotal = material_cost + labor_cost
        2. complexity_adjustment = subtotal × (complexity_factor - 1) × size_factor
        3. adjusted_subtotal = subtotal + complexity_adjustment
        4. profit = adjusted_subtotal × profit_margin
        5. total = adjusted_subtotal + profit
        6. rounded = round to nearest N euros

        Returns:
            PriceBreakdown with all cost components.
        """
        piece = self.data_service.get_piece_by_id(piece_id)
        if not piece:
            raise ValueError(f"Piece not found: {piece_id}")

        # Calculate base costs
        material_cost = self.calculate_material_cost(piece_id)
        labor_cost = self.calculate_labor_cost(piece_id)
        subtotal = material_cost + labor_cost

        # Calculate complexity and size adjustments
        complexity_factor = self.get_complexity_factor(piece_id)
        size_factor = self.get_size_factor(piece.type)

        # Adjustment = subtotal × (complexity - 1) × size
        complexity_adjustment = subtotal * (complexity_factor - Decimal("1")) * size_factor
        adjusted_subtotal = subtotal + complexity_adjustment

        # Add profit margin
        profit_amount = adjusted_subtotal * self.price_config.profit_margin
        total = adjusted_subtotal + profit_amount

        # Round to nearest N euros
        round_to = Decimal(str(self.price_config.round_to))
        rounded_price = (total / round_to).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * round_to

        return PriceBreakdown(
            material_cost=material_cost,
            labor_cost=labor_cost,
            subtotal=subtotal,
            complexity_factor=complexity_factor,
            size_factor=size_factor,
            complexity_adjustment=complexity_adjustment,
            adjusted_subtotal=adjusted_subtotal,
            profit_amount=profit_amount,
            total=total,
            rounded_price=rounded_price,
        )

    def suggest_price_range(self, piece_id: str) -> Tuple[Decimal, Decimal]:
        """
        Suggest min/max price range based on similar pieces.

        Returns:
            Tuple of (min_price, max_price).
        """
        piece = self.data_service.get_piece_by_id(piece_id)
        if not piece:
            return (Decimal("0"), Decimal("0"))

        # Find similar pieces (same type, same main stitch)
        all_pieces = self.data_service.load_pieces()
        similar = [
            p for p in all_pieces
            if p.type == piece.type
            and p.price is not None
            and p.id != piece_id
        ]

        if not similar:
            # No similar pieces, use calculated price with ±20%
            breakdown = self.calculate_price(piece_id)
            base = breakdown.rounded_price
            return (
                base * Decimal("0.8"),
                base * Decimal("1.2"),
            )

        prices = [p.price for p in similar]
        return (min(prices), max(prices))

    def compare_to_market(self, piece_id: str) -> Dict[str, Any]:
        """
        Compare suggested price to similar sold pieces.

        Returns:
            Dict with market analysis.
        """
        piece = self.data_service.get_piece_by_id(piece_id)
        if not piece:
            return {"error": "Piece not found"}

        breakdown = self.calculate_price(piece_id)
        suggested = breakdown.rounded_price

        # Find sold pieces of same type
        all_pieces = self.data_service.load_pieces(include_archived=True)
        sold_similar = [
            p for p in all_pieces
            if p.type == piece.type
            and p.destination == "sold"
            and p.sold_price is not None
        ]

        if not sold_similar:
            return {
                "suggested_price": float(suggested),
                "avg_sold_price": None,
                "comparison": "No similar sold pieces for comparison",
                "recommendation": "Use suggested price as starting point",
            }

        avg_sold = sum(p.sold_price for p in sold_similar) / len(sold_similar)
        diff = suggested - avg_sold
        diff_pct = (diff / avg_sold * 100) if avg_sold else Decimal("0")

        if diff_pct > 20:
            recommendation = "Suggested price is significantly higher than market average. Consider lowering."
        elif diff_pct < -20:
            recommendation = "Suggested price is below market average. You may be able to charge more."
        else:
            recommendation = "Suggested price is in line with market."

        return {
            "suggested_price": float(suggested),
            "avg_sold_price": float(avg_sold),
            "difference": float(diff),
            "difference_pct": float(diff_pct),
            "similar_pieces_count": len(sold_similar),
            "recommendation": recommendation,
        }

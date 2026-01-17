"""
Time calculation service.

Calculates and estimates work times based on:
- Work sessions logged per piece
- Historical data from similar pieces
- Style averages
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional, Dict, Any

from ..models.piece import WorkSession
from .data_service import DataService


@dataclass
class TimeEstimate:
    """Time estimation result."""
    total_hours_logged: float
    estimated_total_hours: Optional[float]
    estimated_remaining_hours: Optional[float]
    estimated_completion_date: Optional[date]
    confidence: str  # "low", "medium", "high"
    basis: str  # Description of how estimate was made


class TimeService:
    """Calculate and estimate work times."""

    def __init__(self, data_service: DataService = None):
        self.data_service = data_service or DataService()

    def calculate_total_hours(self, sessions: List[WorkSession]) -> float:
        """
        Sum all session hours.

        Args:
            sessions: List of WorkSession objects.

        Returns:
            Total hours worked.
        """
        return sum(session.hours for session in sessions)

    def get_piece_total_hours(self, piece_id: str) -> float:
        """
        Get total hours worked on a piece.

        Args:
            piece_id: ID of the piece.

        Returns:
            Total hours from sessions or work_hours field.
        """
        piece = self.data_service.get_piece_by_id(piece_id)
        if not piece:
            return 0.0
        return piece.calculate_total_hours()

    def get_average_hours_by_type(self, piece_type: str) -> Optional[float]:
        """
        Calculate average hours for all finished pieces of a type.

        Args:
            piece_type: Type of piece (scarf, shawl, etc.).

        Returns:
            Average hours or None if no data.
        """
        pieces = self.data_service.load_pieces(include_archived=True)
        finished = [
            p for p in pieces
            if p.type == piece_type
            and p.work_status in ("finished", "ready")
            and p.calculate_total_hours() > 0
        ]

        if not finished:
            return None

        total = sum(p.calculate_total_hours() for p in finished)
        return total / len(finished)

    def get_average_hours_by_stitch(self, stitch_id: str, piece_type: str = None) -> Optional[float]:
        """
        Calculate average hours for pieces using a specific stitch.

        Args:
            stitch_id: ID of the stitch.
            piece_type: Optional filter by piece type.

        Returns:
            Average hours or None if no data.
        """
        pieces = self.data_service.load_pieces(include_archived=True)
        matching = [
            p for p in pieces
            if stitch_id in p.stitches_used
            and p.work_status in ("finished", "ready")
            and p.calculate_total_hours() > 0
        ]

        if piece_type:
            matching = [p for p in matching if p.type == piece_type]

        if not matching:
            return None

        total = sum(p.calculate_total_hours() for p in matching)
        return total / len(matching)

    def estimate_total_hours(self, piece_id: str) -> TimeEstimate:
        """
        Estimate total hours needed for a piece.

        Uses multiple data sources:
        1. If piece is finished, return actual hours
        2. Look at similar pieces (same type + same stitch)
        3. Look at pieces of same type
        4. Fall back to piece type defaults

        Args:
            piece_id: ID of the piece.

        Returns:
            TimeEstimate with hours and confidence.
        """
        piece = self.data_service.get_piece_by_id(piece_id)
        if not piece:
            return TimeEstimate(
                total_hours_logged=0,
                estimated_total_hours=None,
                estimated_remaining_hours=None,
                estimated_completion_date=None,
                confidence="low",
                basis="Piece not found",
            )

        logged_hours = piece.calculate_total_hours()

        # If finished, return actual hours
        if piece.work_status in ("finished", "ready"):
            return TimeEstimate(
                total_hours_logged=logged_hours,
                estimated_total_hours=logged_hours,
                estimated_remaining_hours=0,
                estimated_completion_date=piece.date_finished,
                confidence="high",
                basis="Piece is complete",
            )

        # Try to find similar pieces (same type + same main stitch)
        if piece.stitches_used:
            main_stitch = piece.stitches_used[0]
            avg = self.get_average_hours_by_stitch(main_stitch, piece.type)
            if avg is not None:
                return TimeEstimate(
                    total_hours_logged=logged_hours,
                    estimated_total_hours=avg,
                    estimated_remaining_hours=max(0, avg - logged_hours),
                    estimated_completion_date=None,
                    confidence="medium",
                    basis=f"Based on similar {piece.type} pieces using {main_stitch}",
                )

        # Try average by type
        type_avg = self.get_average_hours_by_type(piece.type)
        if type_avg is not None:
            return TimeEstimate(
                total_hours_logged=logged_hours,
                estimated_total_hours=type_avg,
                estimated_remaining_hours=max(0, type_avg - logged_hours),
                estimated_completion_date=None,
                confidence="medium",
                basis=f"Based on average for {piece.type} pieces",
            )

        # Use type defaults
        defaults = {
            "hat": 6.0,
            "cowl": 8.0,
            "scarf": 12.0,
            "shawl": 20.0,
            "blanket": 40.0,
            "other": 15.0,
        }
        default_hours = defaults.get(piece.type, 15.0)

        return TimeEstimate(
            total_hours_logged=logged_hours,
            estimated_total_hours=default_hours,
            estimated_remaining_hours=max(0, default_hours - logged_hours),
            estimated_completion_date=None,
            confidence="low",
            basis=f"Using default estimate for {piece.type}",
        )

    def predict_completion_date(
        self,
        piece_id: str,
        hours_per_week: float = 5.0
    ) -> Optional[date]:
        """
        Predict when a piece will be finished.

        Args:
            piece_id: ID of the piece.
            hours_per_week: Expected hours of work per week.

        Returns:
            Predicted completion date or None.
        """
        estimate = self.estimate_total_hours(piece_id)
        if estimate.estimated_remaining_hours is None or estimate.estimated_remaining_hours <= 0:
            return None

        weeks_remaining = estimate.estimated_remaining_hours / hours_per_week
        days_remaining = int(weeks_remaining * 7)

        return date.today() + timedelta(days=days_remaining)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall time statistics.

        Returns:
            Dict with various time statistics.
        """
        pieces = self.data_service.load_pieces(include_archived=True)

        # Calculate averages by type
        type_stats = {}
        for piece in pieces:
            if piece.work_status in ("finished", "ready") and piece.calculate_total_hours() > 0:
                if piece.type not in type_stats:
                    type_stats[piece.type] = {"total_hours": 0, "count": 0}
                type_stats[piece.type]["total_hours"] += piece.calculate_total_hours()
                type_stats[piece.type]["count"] += 1

        for ptype, stats in type_stats.items():
            stats["average_hours"] = stats["total_hours"] / stats["count"] if stats["count"] > 0 else 0

        # Total hours across all pieces
        total_hours = sum(p.calculate_total_hours() for p in pieces)

        # In progress pieces
        in_progress = [p for p in pieces if p.work_status == "in_progress"]

        return {
            "total_hours_all_time": total_hours,
            "pieces_completed": len([p for p in pieces if p.work_status in ("finished", "ready")]),
            "pieces_in_progress": len(in_progress),
            "averages_by_type": type_stats,
        }

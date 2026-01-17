"""
Piece data model.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from enum import Enum


class WorkStatus(Enum):
    """Work progress status."""
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    READY = "ready"


class Destination(Enum):
    """Intended destination for the piece."""
    FOR_SALE = "for_sale"
    SOLD = "sold"
    FOR_GIFT = "for_gift"
    GIFTED = "gifted"
    FOR_SELF = "for_self"
    IN_USE = "in_use"


class PieceType(Enum):
    """Types of crochet pieces."""
    SHAWL = "shawl"
    SCARF = "scarf"
    BED_THROW = "bed_throw"
    BLANKET = "blanket"
    COWL = "cowl"
    PONCHO = "poncho"
    CARDIGAN = "cardigan"
    HAT = "hat"
    BAG = "bag"
    HOME_DECOR = "home_decor"
    OTHER = "other"


@dataclass
class WorkSession:
    """A single work session on a piece."""
    date: date
    hours: float
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date.isoformat(),
            "hours": self.hours,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkSession":
        return cls(
            date=date.fromisoformat(data["date"]),
            hours=float(data["hours"]),
            notes=data.get("notes"),
        )


@dataclass
class Dimensions:
    """Piece dimensions."""
    width_cm: Optional[float] = None
    length_cm: Optional[float] = None
    depth_cm: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "width_cm": self.width_cm,
            "length_cm": self.length_cm,
            "depth_cm": self.depth_cm,
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Dimensions"]:
        if data is None:
            return None
        return cls(
            width_cm=data.get("width_cm"),
            length_cm=data.get("length_cm"),
            depth_cm=data.get("depth_cm"),
        )


@dataclass
class Piece:
    """A crochet piece (finished or in progress)."""

    id: str
    name: str
    type: str
    work_status: str
    destination: str
    stitches_used: List[str] = field(default_factory=list)
    yarns_used: List[str] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)

    # Optional fields
    dimensions: Optional[Dimensions] = None
    date_started: Optional[date] = None
    date_finished: Optional[date] = None
    work_hours: Optional[float] = None
    work_sessions: List[WorkSession] = field(default_factory=list)
    hook_size_mm: Optional[float] = None
    price: Optional[Decimal] = None
    suggested_price: Optional[Decimal] = None
    material_cost: Optional[Decimal] = None
    gift_recipient: Optional[str] = None
    sale_platform: Optional[str] = None
    sale_link: Optional[str] = None
    sold_date: Optional[date] = None
    sold_price: Optional[Decimal] = None
    notes: Optional[str] = None

    # Archive fields
    archived: bool = False
    archived_date: Optional[date] = None
    archived_reason: Optional[str] = None

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def calculate_total_hours(self) -> float:
        """Calculate total hours from work sessions."""
        if self.work_sessions:
            return sum(session.hours for session in self.work_sessions)
        return self.work_hours or 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "work_status": self.work_status,
            "destination": self.destination,
            "dimensions": self.dimensions.to_dict() if self.dimensions else None,
            "date_started": self.date_started.isoformat() if self.date_started else None,
            "date_finished": self.date_finished.isoformat() if self.date_finished else None,
            "work_hours": self.work_hours,
            "work_sessions": [s.to_dict() for s in self.work_sessions],
            "hook_size_mm": self.hook_size_mm,
            "photos": self.photos,
            "price": float(self.price) if self.price else None,
            "suggested_price": float(self.suggested_price) if self.suggested_price else None,
            "material_cost": float(self.material_cost) if self.material_cost else None,
            "gift_recipient": self.gift_recipient,
            "sale_platform": self.sale_platform,
            "sale_link": self.sale_link,
            "sold_date": self.sold_date.isoformat() if self.sold_date else None,
            "sold_price": float(self.sold_price) if self.sold_price else None,
            "yarns_used": self.yarns_used,
            "stitches_used": self.stitches_used,
            "notes": self.notes,
            "archived": self.archived,
            "archived_date": self.archived_date.isoformat() if self.archived_date else None,
            "archived_reason": self.archived_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Piece":
        """Create from dictionary (JSON data)."""
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            work_status=data.get("work_status", "in_progress"),
            destination=data.get("destination", "for_sale"),
            dimensions=Dimensions.from_dict(data.get("dimensions")),
            date_started=date.fromisoformat(data["date_started"]) if data.get("date_started") else None,
            date_finished=date.fromisoformat(data["date_finished"]) if data.get("date_finished") else None,
            work_hours=data.get("work_hours"),
            work_sessions=[WorkSession.from_dict(s) for s in data.get("work_sessions", [])],
            hook_size_mm=data.get("hook_size_mm"),
            photos=data.get("photos", []),
            price=Decimal(str(data["price"])) if data.get("price") else None,
            suggested_price=Decimal(str(data["suggested_price"])) if data.get("suggested_price") else None,
            material_cost=Decimal(str(data["material_cost"])) if data.get("material_cost") else None,
            gift_recipient=data.get("gift_recipient"),
            sale_platform=data.get("sale_platform"),
            sale_link=data.get("sale_link"),
            sold_date=date.fromisoformat(data["sold_date"]) if data.get("sold_date") else None,
            sold_price=Decimal(str(data["sold_price"])) if data.get("sold_price") else None,
            yarns_used=data.get("yarns_used", []),
            stitches_used=data.get("stitches_used", []),
            notes=data.get("notes"),
            archived=data.get("archived", False),
            archived_date=date.fromisoformat(data["archived_date"]) if data.get("archived_date") else None,
            archived_reason=data.get("archived_reason"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
        )

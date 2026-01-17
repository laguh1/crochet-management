"""
Yarn data model.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from enum import Enum


class Material(Enum):
    """Primary yarn materials."""
    COTTON = "cotton"
    WOOL = "wool"
    ACRYLIC = "acrylic"
    SILK = "silk"
    BLEND = "blend"
    OTHER = "other"


class WeightCategory(Enum):
    """Yarn weight categories."""
    LACE = "lace"
    FINGERING = "fingering"
    SPORT = "sport"
    DK = "dk"
    WORSTED = "worsted"
    ARAN = "aran"
    BULKY = "bulky"
    SUPER_BULKY = "super_bulky"


@dataclass
class CareInstructions:
    """Yarn care instructions."""
    wash_temp: Optional[str] = None
    machine_washable: bool = False
    tumble_dry: bool = False
    iron_temp: Optional[str] = None
    bleach: bool = False
    dry_clean: bool = False
    special_notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wash_temp": self.wash_temp,
            "machine_washable": self.machine_washable,
            "tumble_dry": self.tumble_dry,
            "iron_temp": self.iron_temp,
            "bleach": self.bleach,
            "dry_clean": self.dry_clean,
            "special_notes": self.special_notes,
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["CareInstructions"]:
        if data is None:
            return None
        return cls(
            wash_temp=data.get("wash_temp"),
            machine_washable=data.get("machine_washable", False),
            tumble_dry=data.get("tumble_dry", False),
            iron_temp=data.get("iron_temp"),
            bleach=data.get("bleach", False),
            dry_clean=data.get("dry_clean", False),
            special_notes=data.get("special_notes"),
        )


@dataclass
class Yarn:
    """A yarn in inventory."""

    id: str
    name: str
    color: str
    material: str
    photos: List[str] = field(default_factory=list)

    # Optional fields
    brand: Optional[str] = None
    color_code: Optional[str] = None
    material_composition: Optional[str] = None
    material_specs: Optional[str] = None
    weight_category: Optional[str] = None
    ball_weight_g: Optional[float] = None
    ball_length_m: Optional[float] = None
    price_paid: Optional[Decimal] = None
    purchase_location: Optional[str] = None
    purchase_link: Optional[str] = None
    purchase_date: Optional[date] = None
    quantity_owned: int = 1
    hook_size_mm: Optional[float] = None
    needle_size_mm: Optional[str] = None
    gauge: Optional[str] = None
    care_instructions: Optional[CareInstructions] = None
    notes: Optional[str] = None

    # Archive fields
    archived: bool = False
    archived_date: Optional[date] = None
    archived_reason: Optional[str] = None

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "color": self.color,
            "color_code": self.color_code,
            "material": self.material,
            "material_composition": self.material_composition,
            "material_specs": self.material_specs,
            "weight_category": self.weight_category,
            "ball_weight_g": self.ball_weight_g,
            "ball_length_m": self.ball_length_m,
            "price_paid": float(self.price_paid) if self.price_paid else None,
            "purchase_location": self.purchase_location,
            "purchase_link": self.purchase_link,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
            "quantity_owned": self.quantity_owned,
            "hook_size_mm": self.hook_size_mm,
            "needle_size_mm": self.needle_size_mm,
            "gauge": self.gauge,
            "care_instructions": self.care_instructions.to_dict() if self.care_instructions else None,
            "photos": self.photos,
            "notes": self.notes,
            "archived": self.archived,
            "archived_date": self.archived_date.isoformat() if self.archived_date else None,
            "archived_reason": self.archived_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Yarn":
        """Create from dictionary (JSON data)."""
        return cls(
            id=data["id"],
            name=data["name"],
            brand=data.get("brand"),
            color=data["color"],
            color_code=data.get("color_code"),
            material=data.get("material", "blend"),
            material_composition=data.get("material_composition"),
            material_specs=data.get("material_specs"),
            weight_category=data.get("weight_category"),
            ball_weight_g=data.get("ball_weight_g"),
            ball_length_m=data.get("ball_length_m"),
            price_paid=Decimal(str(data["price_paid"])) if data.get("price_paid") else None,
            purchase_location=data.get("purchase_location"),
            purchase_link=data.get("purchase_link"),
            purchase_date=date.fromisoformat(data["purchase_date"]) if data.get("purchase_date") else None,
            quantity_owned=data.get("quantity_owned", 1),
            hook_size_mm=data.get("hook_size_mm"),
            needle_size_mm=data.get("needle_size_mm"),
            gauge=data.get("gauge"),
            care_instructions=CareInstructions.from_dict(data.get("care_instructions")),
            photos=data.get("photos", []),
            notes=data.get("notes"),
            archived=data.get("archived", False),
            archived_date=date.fromisoformat(data["archived_date"]) if data.get("archived_date") else None,
            archived_reason=data.get("archived_reason"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
        )

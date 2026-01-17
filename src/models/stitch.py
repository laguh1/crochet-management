"""
Stitch data model.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class StitchCategory(Enum):
    """Stitch categories."""
    BASIC = "basic"
    TEXTURED = "textured"
    LACE = "lace"
    COLORWORK = "colorwork"
    SPECIALTY = "specialty"


class Difficulty(Enum):
    """Stitch difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class Stitch:
    """A crochet stitch/technique."""

    id: str
    name: str
    description: str
    photos: List[str] = field(default_factory=list)

    # Optional fields
    name_aliases: List[str] = field(default_factory=list)
    name_es: Optional[str] = None
    abbreviation: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    hookfully_link: Optional[str] = None
    instruction_link: Optional[str] = None
    video_link: Optional[str] = None
    notes: Optional[str] = None

    # Archive fields
    archived: bool = False
    archived_date: Optional[date] = None
    archived_reason: Optional[str] = None

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_complexity_factor(self) -> float:
        """Get complexity factor based on category."""
        from ..config import config

        category = self.category or "basic"
        return float(config.STITCH_COMPLEXITY.get(category, config.STITCH_COMPLEXITY["basic"]))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "name_aliases": self.name_aliases,
            "name_es": self.name_es,
            "abbreviation": self.abbreviation,
            "category": self.category,
            "difficulty": self.difficulty,
            "description": self.description,
            "hookfully_link": self.hookfully_link,
            "instruction_link": self.instruction_link,
            "video_link": self.video_link,
            "photos": self.photos,
            "notes": self.notes,
            "archived": self.archived,
            "archived_date": self.archived_date.isoformat() if self.archived_date else None,
            "archived_reason": self.archived_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Stitch":
        """Create from dictionary (JSON data)."""
        return cls(
            id=data["id"],
            name=data["name"],
            name_aliases=data.get("name_aliases", []),
            name_es=data.get("name_es"),
            abbreviation=data.get("abbreviation"),
            category=data.get("category"),
            difficulty=data.get("difficulty"),
            description=data.get("description", ""),
            hookfully_link=data.get("hookfully_link"),
            instruction_link=data.get("instruction_link"),
            video_link=data.get("video_link"),
            photos=data.get("photos", []),
            notes=data.get("notes"),
            archived=data.get("archived", False),
            archived_date=date.fromisoformat(data["archived_date"]) if data.get("archived_date") else None,
            archived_reason=data.get("archived_reason"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
        )

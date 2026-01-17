"""
Configuration settings for the Crochet Project Manager.
"""

from pathlib import Path
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class Config:
    """Application configuration."""

    # Paths
    BASE_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent)

    @property
    def DATA_DIR(self) -> Path:
        return self.BASE_DIR / "data"

    @property
    def IMAGES_DIR(self) -> Path:
        return self.BASE_DIR / "images"

    # Data files
    @property
    def PIECES_FILE(self) -> Path:
        return self.DATA_DIR / "pieces.json"

    @property
    def YARNS_FILE(self) -> Path:
        return self.DATA_DIR / "yarns.json"

    @property
    def STITCHES_FILE(self) -> Path:
        return self.DATA_DIR / "stitches.json"

    @property
    def STYLES_FILE(self) -> Path:
        return self.DATA_DIR / "styles.json"

    # Pricing defaults
    HOURLY_RATE: Decimal = Decimal("8.00")
    PROFIT_MARGIN: Decimal = Decimal("0.20")
    MIN_MARGIN: Decimal = Decimal("0.10")
    PRICE_ROUND_TO: int = 5

    # Stitch complexity factors by category
    STITCH_COMPLEXITY: Dict[str, Decimal] = field(default_factory=lambda: {
        "basic": Decimal("1.0"),
        "textured": Decimal("1.15"),
        "lace": Decimal("1.25"),
        "colorwork": Decimal("1.30"),
        "specialty": Decimal("1.40"),
    })

    # Size factors by piece type
    SIZE_FACTORS: Dict[str, Decimal] = field(default_factory=lambda: {
        "hat": Decimal("0.8"),
        "cowl": Decimal("0.9"),
        "scarf": Decimal("1.0"),
        "shawl": Decimal("1.2"),
        "blanket": Decimal("1.5"),
        "other": Decimal("1.0"),
    })

    # ID formats
    ID_PATTERNS = {
        "piece": "PIECE-{:03d}",
        "yarn": "YARN-{:03d}",
        "stitch": "STITCH-{:03d}",
        "style": "STYLE-{:03d}",
    }


# Default configuration instance
config = Config()

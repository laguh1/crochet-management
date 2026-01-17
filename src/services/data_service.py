"""
Data service for JSON CRUD operations.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any, TypeVar, Type

from ..config import config
from ..models.piece import Piece
from ..models.yarn import Yarn
from ..models.stitch import Stitch

T = TypeVar("T", Piece, Yarn, Stitch)


class DataService:
    """CRUD operations for JSON data files."""

    def __init__(self, config_override=None):
        self.config = config_override or config

    # --- Generic Methods ---

    def _load_json(self, filepath: Path) -> Dict[str, Any]:
        """Load JSON file."""
        if not filepath.exists():
            return {"_meta": {"next_id": 1, "last_updated": datetime.now().isoformat()}}
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, filepath: Path, data: Dict[str, Any]) -> None:
        """Save JSON file."""
        data["_meta"]["last_updated"] = datetime.now().isoformat()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _get_next_id(self, entity_type: str) -> str:
        """Get next sequential ID for entity type."""
        if entity_type == "piece":
            data = self._load_json(self.config.PIECES_FILE)
            key = "pieces"
        elif entity_type == "yarn":
            data = self._load_json(self.config.YARNS_FILE)
            key = "yarns"
        elif entity_type == "stitch":
            data = self._load_json(self.config.STITCHES_FILE)
            key = "stitches"
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")

        items = data.get(key, [])
        if not items:
            return self.config.ID_PATTERNS[entity_type].format(1)

        # Find max ID
        max_num = 0
        prefix = entity_type.upper() + "-"
        for item in items:
            item_id = item.get("id", "")
            if item_id.startswith(prefix):
                try:
                    num = int(item_id.split("-")[1])
                    max_num = max(max_num, num)
                except (IndexError, ValueError):
                    pass

        return self.config.ID_PATTERNS[entity_type].format(max_num + 1)

    # --- Pieces ---

    def load_pieces(self, include_archived: bool = False) -> List[Piece]:
        """Load all pieces from JSON."""
        data = self._load_json(self.config.PIECES_FILE)
        pieces = [Piece.from_dict(p) for p in data.get("pieces", [])]
        if not include_archived:
            pieces = [p for p in pieces if not p.archived]
        return pieces

    def save_pieces(self, pieces: List[Piece]) -> None:
        """Save all pieces to JSON."""
        data = self._load_json(self.config.PIECES_FILE)
        data["pieces"] = [p.to_dict() for p in pieces]
        self._save_json(self.config.PIECES_FILE, data)

    def get_piece_by_id(self, piece_id: str) -> Optional[Piece]:
        """Get a single piece by ID."""
        pieces = self.load_pieces(include_archived=True)
        for piece in pieces:
            if piece.id == piece_id:
                return piece
        return None

    def create_piece(self, piece: Piece) -> str:
        """Create a new piece. Returns the assigned ID."""
        if not piece.id:
            piece.id = self._get_next_id("piece")
        piece.created_at = datetime.now()
        piece.updated_at = datetime.now()

        pieces = self.load_pieces(include_archived=True)
        pieces.append(piece)
        self.save_pieces(pieces)
        return piece.id

    def update_piece(self, piece: Piece) -> None:
        """Update an existing piece."""
        piece.updated_at = datetime.now()
        pieces = self.load_pieces(include_archived=True)
        for i, p in enumerate(pieces):
            if p.id == piece.id:
                pieces[i] = piece
                break
        self.save_pieces(pieces)

    def archive_piece(self, piece_id: str, reason: str = None) -> None:
        """Archive a piece (soft delete)."""
        piece = self.get_piece_by_id(piece_id)
        if piece:
            piece.archived = True
            piece.archived_date = datetime.now().date()
            piece.archived_reason = reason
            self.update_piece(piece)

    # --- Yarns ---

    def load_yarns(self, include_archived: bool = False) -> List[Yarn]:
        """Load all yarns from JSON."""
        data = self._load_json(self.config.YARNS_FILE)
        yarns = [Yarn.from_dict(y) for y in data.get("yarns", [])]
        if not include_archived:
            yarns = [y for y in yarns if not y.archived]
        return yarns

    def save_yarns(self, yarns: List[Yarn]) -> None:
        """Save all yarns to JSON."""
        data = self._load_json(self.config.YARNS_FILE)
        data["yarns"] = [y.to_dict() for y in yarns]
        self._save_json(self.config.YARNS_FILE, data)

    def get_yarn_by_id(self, yarn_id: str) -> Optional[Yarn]:
        """Get a single yarn by ID."""
        yarns = self.load_yarns(include_archived=True)
        for yarn in yarns:
            if yarn.id == yarn_id:
                return yarn
        return None

    def create_yarn(self, yarn: Yarn) -> str:
        """Create a new yarn. Returns the assigned ID."""
        if not yarn.id:
            yarn.id = self._get_next_id("yarn")
        yarn.created_at = datetime.now()
        yarn.updated_at = datetime.now()

        yarns = self.load_yarns(include_archived=True)
        yarns.append(yarn)
        self.save_yarns(yarns)
        return yarn.id

    def update_yarn(self, yarn: Yarn) -> None:
        """Update an existing yarn."""
        yarn.updated_at = datetime.now()
        yarns = self.load_yarns(include_archived=True)
        for i, y in enumerate(yarns):
            if y.id == yarn.id:
                yarns[i] = yarn
                break
        self.save_yarns(yarns)

    # --- Stitches ---

    def load_stitches(self, include_archived: bool = False) -> List[Stitch]:
        """Load all stitches from JSON."""
        data = self._load_json(self.config.STITCHES_FILE)
        stitches = [Stitch.from_dict(s) for s in data.get("stitches", [])]
        if not include_archived:
            stitches = [s for s in stitches if not s.archived]
        return stitches

    def save_stitches(self, stitches: List[Stitch]) -> None:
        """Save all stitches to JSON."""
        data = self._load_json(self.config.STITCHES_FILE)
        data["stitches"] = [s.to_dict() for s in stitches]
        self._save_json(self.config.STITCHES_FILE, data)

    def get_stitch_by_id(self, stitch_id: str) -> Optional[Stitch]:
        """Get a single stitch by ID."""
        stitches = self.load_stitches(include_archived=True)
        for stitch in stitches:
            if stitch.id == stitch_id:
                return stitch
        return None

    def create_stitch(self, stitch: Stitch) -> str:
        """Create a new stitch. Returns the assigned ID."""
        if not stitch.id:
            stitch.id = self._get_next_id("stitch")
        stitch.created_at = datetime.now()
        stitch.updated_at = datetime.now()

        stitches = self.load_stitches(include_archived=True)
        stitches.append(stitch)
        self.save_stitches(stitches)
        return stitch.id

    def update_stitch(self, stitch: Stitch) -> None:
        """Update an existing stitch."""
        stitch.updated_at = datetime.now()
        stitches = self.load_stitches(include_archived=True)
        for i, s in enumerate(stitches):
            if s.id == stitch.id:
                stitches[i] = stitch
                break
        self.save_stitches(stitches)

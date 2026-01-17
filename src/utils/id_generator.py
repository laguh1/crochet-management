"""
ID generation utilities.

Generates sequential IDs for pieces, yarns, and stitches
following the format: ENTITY-NNN (e.g., PIECE-001, YARN-042).
"""

import re
from typing import List, Optional


class IDGenerator:
    """Generate sequential IDs for entities."""

    PATTERNS = {
        "piece": "PIECE-{:03d}",
        "yarn": "YARN-{:03d}",
        "stitch": "STITCH-{:03d}",
    }

    PREFIXES = {
        "piece": "PIECE-",
        "yarn": "YARN-",
        "stitch": "STITCH-",
    }

    @classmethod
    def extract_number(cls, entity_id: str) -> Optional[int]:
        """
        Extract the numeric part from an entity ID.

        Args:
            entity_id: ID string like "PIECE-042".

        Returns:
            The numeric part (42) or None if invalid.
        """
        match = re.search(r"-(\d+)$", entity_id)
        if match:
            return int(match.group(1))
        return None

    @classmethod
    def get_next_id(cls, entity_type: str, existing_ids: List[str]) -> str:
        """
        Generate the next sequential ID for an entity type.

        Args:
            entity_type: "piece", "yarn", or "stitch".
            existing_ids: List of existing IDs of this type.

        Returns:
            Next ID string (e.g., "PIECE-043").
        """
        if entity_type not in cls.PATTERNS:
            raise ValueError(f"Unknown entity type: {entity_type}")

        prefix = cls.PREFIXES[entity_type]
        pattern = cls.PATTERNS[entity_type]

        max_num = 0
        for eid in existing_ids:
            if eid.startswith(prefix):
                num = cls.extract_number(eid)
                if num is not None and num > max_num:
                    max_num = num

        return pattern.format(max_num + 1)

    @classmethod
    def validate_id(cls, entity_id: str, entity_type: str = None) -> bool:
        """
        Validate an entity ID format.

        Args:
            entity_id: ID string to validate.
            entity_type: Optional type to validate against.

        Returns:
            True if valid, False otherwise.
        """
        if entity_type:
            prefix = cls.PREFIXES.get(entity_type)
            if not prefix:
                return False
            if not entity_id.startswith(prefix):
                return False

        # Check format: PREFIX-NNN
        pattern = r"^(PIECE|YARN|STITCH)-\d{3}$"
        return bool(re.match(pattern, entity_id))

    @classmethod
    def get_entity_type(cls, entity_id: str) -> Optional[str]:
        """
        Determine entity type from ID.

        Args:
            entity_id: ID string like "YARN-001".

        Returns:
            Entity type ("piece", "yarn", "stitch") or None.
        """
        for entity_type, prefix in cls.PREFIXES.items():
            if entity_id.startswith(prefix):
                return entity_type
        return None

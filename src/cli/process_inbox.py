"""
Inbox processing for photos and files.

Processes files in inbox directories and creates/updates entities.
"""

from pathlib import Path
from typing import List, Dict, Any

from ..config import config
from ..services import DataService
from ..utils.photo_utils import PhotoUtils
from ..utils.date_utils import DateUtils
from .rename_files import FileRenamer


class InboxProcessor:
    """Process inbox files for entity creation."""

    def __init__(self, data_service: DataService = None):
        self.data_service = data_service or DataService()
        self.images_path = config.DATA_DIR.parent / "images"

    def check_all_inboxes(self) -> Dict[str, List[Path]]:
        """
        Check all inbox directories for pending files.

        Returns:
            Dict mapping entity type to list of files.
        """
        results = {}

        for entity_type in ["piece", "yarn", "stitch"]:
            inbox = PhotoUtils.get_inbox_directory(self.images_path, entity_type)
            files = PhotoUtils.list_images_in_directory(inbox)
            if files:
                results[entity_type] = files

        return results

    def print_inbox_summary(self, inboxes: Dict[str, List[Path]]) -> None:
        """
        Print summary of pending inbox files.

        Args:
            inboxes: Dict from check_all_inboxes.
        """
        if not inboxes:
            print("All inboxes are empty.")
            return

        print("\nPending inbox files:")
        print("-" * 40)

        for entity_type, files in inboxes.items():
            print(f"\n{entity_type.title()}s inbox: {len(files)} file(s)")
            for f in files[:5]:
                print(f"  - {f.name}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")

    def group_files_by_entity(
        self,
        files: List[Path],
        entity_type: str
    ) -> List[List[Path]]:
        """
        Group files that belong to the same entity.

        This is a simple grouping based on filename patterns.
        For more sophisticated grouping (visual analysis), use AI.

        Args:
            files: List of file paths.
            entity_type: Type of entity.

        Returns:
            List of file groups (each group = one entity).
        """
        groups = []
        current_group = []
        last_prefix = None

        for filepath in sorted(files):
            # Extract date or identifier prefix
            date = DateUtils.extract_date_from_filename(filepath.name)
            prefix = date.isoformat() if date else filepath.stem[:10]

            if last_prefix is None or prefix == last_prefix:
                current_group.append(filepath)
            else:
                if current_group:
                    groups.append(current_group)
                current_group = [filepath]

            last_prefix = prefix

        if current_group:
            groups.append(current_group)

        return groups

    def process_yarn_inbox(self, dry_run: bool = True) -> List[str]:
        """
        Process yarn inbox files.

        Args:
            dry_run: If True, only show what would be done.

        Returns:
            List of created yarn IDs.
        """
        inbox = PhotoUtils.get_inbox_directory(self.images_path, "yarn")
        files = PhotoUtils.list_images_in_directory(inbox)

        if not files:
            print("No files in yarn inbox.")
            return []

        created_ids = []
        groups = self.group_files_by_entity(files, "yarn")

        print(f"\nFound {len(files)} files in {len(groups)} group(s)")

        for i, group in enumerate(groups, 1):
            print(f"\n--- Group {i} ({len(group)} files) ---")
            for f in group:
                print(f"  {f.name}")

            if not dry_run:
                # In real implementation, would prompt for yarn details
                # or use AI to extract from screenshots
                print("  [Would create yarn and move files]")

        return created_ids

    def process_stitch_inbox(self, dry_run: bool = True) -> List[str]:
        """
        Process stitch inbox files.

        Args:
            dry_run: If True, only show what would be done.

        Returns:
            List of created stitch IDs.
        """
        inbox = PhotoUtils.get_inbox_directory(self.images_path, "stitch")
        files = PhotoUtils.list_images_in_directory(inbox)

        if not files:
            print("No files in stitch inbox.")
            return []

        created_ids = []

        print(f"\nFound {len(files)} stitch reference files")

        for f in files:
            print(f"  {f.name}")

            if not dry_run:
                # Would analyze image to identify stitch
                # Cross-reference with Hookfully
                # Create or update stitch entry
                print("  [Would identify stitch and create entry]")

        return created_ids

    def process_piece_inbox(self, dry_run: bool = True) -> List[str]:
        """
        Process piece inbox files.

        Args:
            dry_run: If True, only show what would be done.

        Returns:
            List of created piece IDs.
        """
        inbox = PhotoUtils.get_inbox_directory(self.images_path, "piece")
        files = PhotoUtils.list_images_in_directory(inbox)

        if not files:
            print("No files in pieces inbox.")
            return []

        created_ids = []
        groups = self.group_files_by_entity(files, "piece")

        print(f"\nFound {len(files)} files in {len(groups)} piece(s)")

        for i, group in enumerate(groups, 1):
            print(f"\n--- Piece {i} ({len(group)} photos) ---")

            # Extract date from first file if available
            first_date = DateUtils.extract_date_from_filename(group[0].name)
            if first_date:
                print(f"  Date: {first_date}")

            for f in group:
                print(f"  {f.name}")

            if not dry_run:
                # Would prompt for piece details
                # Identify stitches visually
                # Create piece entry
                # Move and rename files
                print("  [Would create piece and move files]")

        return created_ids


def process_inbox(entity_type: str, dry_run: bool = True) -> None:
    """
    Process inbox for specified entity type.

    Args:
        entity_type: "pieces", "yarns", "stitches", or "all".
        dry_run: If True, only show what would be done.
    """
    processor = InboxProcessor()

    if entity_type == "all":
        inboxes = processor.check_all_inboxes()
        processor.print_inbox_summary(inboxes)

        for etype in inboxes.keys():
            print(f"\n{'=' * 40}")
            print(f"Processing {etype}s inbox")
            print("=" * 40)

            if etype == "yarn":
                processor.process_yarn_inbox(dry_run)
            elif etype == "stitch":
                processor.process_stitch_inbox(dry_run)
            elif etype == "piece":
                processor.process_piece_inbox(dry_run)

    elif entity_type == "yarns":
        processor.process_yarn_inbox(dry_run)
    elif entity_type == "stitches":
        processor.process_stitch_inbox(dry_run)
    elif entity_type == "pieces":
        processor.process_piece_inbox(dry_run)
    else:
        print(f"Unknown entity type: {entity_type}")

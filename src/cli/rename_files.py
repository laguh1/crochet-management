"""
File renaming utilities.

Handles batch renaming of photos according to naming conventions.
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional

from ..utils.photo_utils import PhotoUtils
from ..utils.date_utils import DateUtils


class FileRenamer:
    """Batch file renaming operations."""

    def __init__(self, base_path: Path):
        """
        Initialize the file renamer.

        Args:
            base_path: Base path to the images directory.
        """
        self.base_path = base_path

    def generate_rename_plan(
        self,
        files: List[Path],
        entity_id: str,
        descriptors: Optional[List[str]] = None
    ) -> List[Tuple[Path, str]]:
        """
        Generate a rename plan for a list of files.

        Args:
            files: List of file paths to rename.
            entity_id: Entity ID for the new names.
            descriptors: Optional list of descriptors for each file.

        Returns:
            List of (source_path, new_filename) tuples.
        """
        plan = []

        for i, filepath in enumerate(files):
            ext = filepath.suffix.lower()

            if descriptors and i < len(descriptors):
                descriptor = descriptors[i]
            else:
                # Generate descriptor from original filename or index
                descriptor = self._infer_descriptor(filepath, i)

            new_name = PhotoUtils.generate_photo_filename(
                entity_id=entity_id,
                descriptor=descriptor,
                extension=ext,
                index=i + 1 if len(files) > 1 else None
            )

            plan.append((filepath, new_name))

        return plan

    def _infer_descriptor(self, filepath: Path, index: int) -> str:
        """
        Infer a descriptor from the original filename.

        Args:
            filepath: Original file path.
            index: Position in the file list.

        Returns:
            Inferred descriptor string.
        """
        name = filepath.stem.lower()

        # Common descriptors to detect
        descriptor_keywords = {
            "front": ["front", "main", "hero"],
            "back": ["back", "reverse"],
            "detail": ["detail", "closeup", "close-up", "macro"],
            "label": ["label", "tag", "brand"],
            "ball": ["ball", "skein"],
            "texture": ["texture", "swatch"],
            "wip": ["wip", "progress", "working"],
            "finished": ["finished", "done", "complete", "final"],
            "worn": ["worn", "wearing", "model", "mannequin"],
            "folded": ["folded", "flat"],
            "diagram": ["diagram", "chart", "pattern"],
            "tutorial": ["tutorial", "screenshot", "screen"],
            "sample": ["sample", "example"],
            "shop": ["shop", "store", "website", "tienda"],
        }

        for descriptor, keywords in descriptor_keywords.items():
            for keyword in keywords:
                if keyword in name:
                    return descriptor

        # Default descriptors based on index
        defaults = ["photo", "image", "pic"]
        return f"photo{index + 1:02d}"

    def preview_rename(self, plan: List[Tuple[Path, str]]) -> str:
        """
        Generate a preview of the rename plan.

        Args:
            plan: List of (source_path, new_filename) tuples.

        Returns:
            Formatted preview string.
        """
        lines = ["Rename Plan:", "-" * 60]

        for source, new_name in plan:
            lines.append(f"  {source.name}")
            lines.append(f"    -> {new_name}")

        return "\n".join(lines)

    def execute_rename(
        self,
        plan: List[Tuple[Path, str]],
        dest_directory: Path,
        move: bool = True
    ) -> List[Path]:
        """
        Execute the rename plan.

        Args:
            plan: List of (source_path, new_filename) tuples.
            dest_directory: Destination directory.
            move: If True, move files; if False, copy.

        Returns:
            List of new file paths.
        """
        new_paths = []

        for source, new_name in plan:
            if move:
                new_path = PhotoUtils.rename_and_move_photo(
                    source=source,
                    dest_directory=dest_directory,
                    new_filename=new_name
                )
            else:
                new_path = PhotoUtils.copy_photo(
                    source=source,
                    dest_directory=dest_directory,
                    new_filename=new_name
                )
            new_paths.append(new_path)

        return new_paths


def rename_inbox_files(
    base_path: Path,
    entity_type: str,
    entity_id: str,
    descriptors: Optional[List[str]] = None,
    dry_run: bool = False
) -> List[Path]:
    """
    Rename files from inbox to entity folder.

    Args:
        base_path: Base images path.
        entity_type: "piece", "yarn", or "stitch".
        entity_id: Entity ID for naming.
        descriptors: Optional descriptors for files.
        dry_run: If True, only show plan without executing.

    Returns:
        List of new file paths (empty if dry_run).
    """
    renamer = FileRenamer(base_path)

    inbox = PhotoUtils.get_inbox_directory(base_path, entity_type)
    dest = PhotoUtils.get_entity_photo_directory(base_path, entity_id)

    files = PhotoUtils.list_images_in_directory(inbox)

    if not files:
        print(f"No files found in {inbox}")
        return []

    plan = renamer.generate_rename_plan(files, entity_id, descriptors)

    if dry_run:
        print(renamer.preview_rename(plan))
        return []

    return renamer.execute_rename(plan, dest, move=True)

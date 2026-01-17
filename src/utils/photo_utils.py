"""
Photo file management utilities.

Handles renaming, moving, and organizing photo files.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple


class PhotoUtils:
    """Photo file management utilities."""

    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"}

    @classmethod
    def is_image_file(cls, filepath: Path) -> bool:
        """
        Check if a file is a supported image format.

        Args:
            filepath: Path to check.

        Returns:
            True if supported image file.
        """
        return filepath.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    @classmethod
    def list_images_in_directory(cls, directory: Path) -> List[Path]:
        """
        List all image files in a directory.

        Args:
            directory: Directory to scan.

        Returns:
            List of image file paths.
        """
        if not directory.exists():
            return []

        images = []
        for filepath in directory.iterdir():
            if filepath.is_file() and cls.is_image_file(filepath):
                images.append(filepath)

        return sorted(images)

    @classmethod
    def generate_photo_filename(
        cls,
        entity_id: str,
        descriptor: str,
        extension: str,
        index: Optional[int] = None
    ) -> str:
        """
        Generate a standardized photo filename.

        Args:
            entity_id: Entity ID (e.g., "PIECE-001").
            descriptor: Photo descriptor (e.g., "front", "detail").
            extension: File extension (with or without dot).
            index: Optional index number for multiple photos.

        Returns:
            Standardized filename.

        Examples:
            - PIECE-001_front.jpg
            - PIECE-001_01_wip.jpg
            - YARN-005_label.png
        """
        if not extension.startswith("."):
            extension = f".{extension}"

        extension = extension.lower()

        if index is not None:
            return f"{entity_id}_{index:02d}_{descriptor}{extension}"
        else:
            return f"{entity_id}_{descriptor}{extension}"

    @classmethod
    def rename_and_move_photo(
        cls,
        source: Path,
        dest_directory: Path,
        new_filename: str,
        create_dir: bool = True
    ) -> Path:
        """
        Rename and move a photo to a new location.

        Args:
            source: Source file path.
            dest_directory: Destination directory.
            new_filename: New filename.
            create_dir: Create destination directory if missing.

        Returns:
            Path to the new file location.
        """
        if create_dir:
            dest_directory.mkdir(parents=True, exist_ok=True)

        dest_path = dest_directory / new_filename

        # Handle file already exists
        if dest_path.exists():
            base, ext = os.path.splitext(new_filename)
            counter = 1
            while dest_path.exists():
                dest_path = dest_directory / f"{base}_{counter}{ext}"
                counter += 1

        shutil.move(str(source), str(dest_path))
        return dest_path

    @classmethod
    def copy_photo(
        cls,
        source: Path,
        dest_directory: Path,
        new_filename: str,
        create_dir: bool = True
    ) -> Path:
        """
        Copy a photo to a new location.

        Args:
            source: Source file path.
            dest_directory: Destination directory.
            new_filename: New filename.
            create_dir: Create destination directory if missing.

        Returns:
            Path to the copied file.
        """
        if create_dir:
            dest_directory.mkdir(parents=True, exist_ok=True)

        dest_path = dest_directory / new_filename
        shutil.copy2(str(source), str(dest_path))
        return dest_path

    @classmethod
    def get_entity_photo_directory(cls, base_path: Path, entity_id: str) -> Path:
        """
        Get the photo directory for an entity.

        Args:
            base_path: Base images path.
            entity_id: Entity ID (e.g., "PIECE-001").

        Returns:
            Path to entity's photo directory.
        """
        if entity_id.startswith("PIECE-"):
            return base_path / "pieces" / entity_id
        elif entity_id.startswith("YARN-"):
            return base_path / "yarns" / entity_id
        elif entity_id.startswith("STITCH-"):
            return base_path / "stitches" / entity_id
        else:
            raise ValueError(f"Unknown entity type for ID: {entity_id}")

    @classmethod
    def get_inbox_directory(cls, base_path: Path, entity_type: str) -> Path:
        """
        Get the inbox directory for an entity type.

        Args:
            base_path: Base images path.
            entity_type: "piece", "yarn", or "stitch".

        Returns:
            Path to inbox directory.
        """
        mapping = {
            "piece": "pieces",
            "yarn": "yarns",
            "stitch": "stitches",
        }

        folder = mapping.get(entity_type)
        if not folder:
            raise ValueError(f"Unknown entity type: {entity_type}")

        return base_path / folder / "inbox"

    @classmethod
    def extract_photos_info(cls, photos: List[str]) -> List[Tuple[str, str]]:
        """
        Extract info from a list of photo filenames.

        Args:
            photos: List of photo filenames.

        Returns:
            List of (descriptor, extension) tuples.
        """
        results = []
        for photo in photos:
            path = Path(photo)
            name = path.stem
            ext = path.suffix

            # Try to extract descriptor from name
            # e.g., "PIECE-001_front" -> "front"
            # e.g., "PIECE-001_01_wip" -> "wip"
            parts = name.split("_")
            if len(parts) >= 2:
                descriptor = parts[-1]
            else:
                descriptor = name

            results.append((descriptor, ext))

        return results

"""
Date parsing and formatting utilities.

Handles extraction of dates from filenames and various date formats.
"""

import re
from datetime import date, datetime
from typing import Optional, Tuple


class DateUtils:
    """Date parsing and formatting utilities."""

    # Common date patterns in filenames
    FILENAME_PATTERNS = [
        # YYYYMMDD
        (r"(\d{4})(\d{2})(\d{2})", "%Y%m%d"),
        # YYYY-MM-DD
        (r"(\d{4})-(\d{2})-(\d{2})", "%Y-%m-%d"),
        # YYYY_MM_DD
        (r"(\d{4})_(\d{2})_(\d{2})", "%Y_%m_%d"),
        # DD-MM-YYYY
        (r"(\d{2})-(\d{2})-(\d{4})", "%d-%m-%Y"),
        # DD_MM_YYYY
        (r"(\d{2})_(\d{2})_(\d{4})", "%d_%m_%Y"),
    ]

    @classmethod
    def extract_date_from_filename(cls, filename: str) -> Optional[date]:
        """
        Extract a date from a filename.

        Handles common patterns like:
        - IMG_20260115.jpg -> 2026-01-15
        - 2026-01-15_photo.jpg -> 2026-01-15
        - screenshot_15-01-2026.png -> 2026-01-15

        Args:
            filename: Filename to parse.

        Returns:
            Extracted date or None if not found.
        """
        for pattern, date_format in cls.FILENAME_PATTERNS:
            match = re.search(pattern, filename)
            if match:
                try:
                    date_str = match.group(0)
                    parsed = datetime.strptime(date_str, date_format)
                    # Validate reasonable date range
                    if 2000 <= parsed.year <= 2100:
                        return parsed.date()
                except ValueError:
                    continue
        return None

    @classmethod
    def parse_date(cls, date_string: str) -> Optional[date]:
        """
        Parse a date from various string formats.

        Args:
            date_string: Date string to parse.

        Returns:
            Parsed date or None if invalid.
        """
        formats = [
            "%Y-%m-%d",  # ISO format
            "%d/%m/%Y",  # European
            "%m/%d/%Y",  # American
            "%d-%m-%Y",
            "%Y/%m/%d",
            "%B %d, %Y",  # "January 15, 2026"
            "%d %B %Y",   # "15 January 2026"
            "%b %d, %Y",  # "Jan 15, 2026"
            "%d %b %Y",   # "15 Jan 2026"
        ]

        date_string = date_string.strip()

        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt).date()
            except ValueError:
                continue

        return None

    @classmethod
    def format_date(cls, d: date, format_type: str = "iso") -> str:
        """
        Format a date for display or storage.

        Args:
            d: Date to format.
            format_type: "iso", "display", "filename".

        Returns:
            Formatted date string.
        """
        formats = {
            "iso": "%Y-%m-%d",
            "display": "%d %B %Y",
            "filename": "%Y%m%d",
            "short": "%d/%m/%Y",
        }

        fmt = formats.get(format_type, formats["iso"])
        return d.strftime(fmt)

    @classmethod
    def date_range_days(cls, start: date, end: date) -> int:
        """
        Calculate days between two dates.

        Args:
            start: Start date.
            end: End date.

        Returns:
            Number of days between dates.
        """
        return (end - start).days

    @classmethod
    def get_week_info(cls, d: date) -> Tuple[int, int]:
        """
        Get week number and year for a date.

        Args:
            d: Date to analyze.

        Returns:
            Tuple of (week_number, year).
        """
        iso_calendar = d.isocalendar()
        return (iso_calendar.week, iso_calendar.year)

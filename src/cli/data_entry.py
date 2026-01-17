"""
Interactive data entry for crochet entities.

Provides prompts for creating new pieces, yarns, and stitches.
"""

from datetime import date
from decimal import Decimal
from typing import Optional, List, Any, Dict

from ..models.piece import Piece, Dimensions, WorkSession
from ..models.yarn import Yarn, CareInstructions
from ..models.stitch import Stitch
from ..services import DataService


class DataEntryHelper:
    """Interactive data entry helper."""

    def __init__(self, data_service: DataService = None):
        self.data_service = data_service or DataService()

    def prompt(self, message: str, default: Any = None, required: bool = False) -> str:
        """
        Prompt user for input.

        Args:
            message: Prompt message.
            default: Default value.
            required: If True, keep prompting until value provided.

        Returns:
            User input or default.
        """
        if default is not None:
            display = f"{message} [{default}]: "
        else:
            display = f"{message}: "

        while True:
            value = input(display).strip()

            if not value:
                if default is not None:
                    return str(default)
                if required:
                    print("  This field is required.")
                    continue
                return ""

            return value

    def prompt_choice(
        self,
        message: str,
        choices: List[str],
        default: str = None
    ) -> str:
        """
        Prompt user to choose from options.

        Args:
            message: Prompt message.
            choices: List of valid choices.
            default: Default choice.

        Returns:
            Selected choice.
        """
        print(f"{message}")
        for i, choice in enumerate(choices, 1):
            marker = "*" if choice == default else " "
            print(f"  {marker}{i}. {choice}")

        while True:
            value = self.prompt("Enter number or value", default)

            # Check if it's a number
            try:
                idx = int(value)
                if 1 <= idx <= len(choices):
                    return choices[idx - 1]
            except ValueError:
                pass

            # Check if it's a valid choice
            if value in choices:
                return value

            print(f"  Invalid choice. Enter 1-{len(choices)} or type the value.")

    def prompt_number(
        self,
        message: str,
        default: float = None,
        required: bool = False
    ) -> Optional[float]:
        """
        Prompt for a numeric value.

        Args:
            message: Prompt message.
            default: Default value.
            required: If True, keep prompting until valid.

        Returns:
            Numeric value or None.
        """
        while True:
            value = self.prompt(message, default, required)

            if not value:
                return None

            try:
                return float(value)
            except ValueError:
                print("  Please enter a valid number.")

    def prompt_date(
        self,
        message: str,
        default: date = None,
        required: bool = False
    ) -> Optional[date]:
        """
        Prompt for a date.

        Args:
            message: Prompt message.
            default: Default date.
            required: If True, keep prompting until valid.

        Returns:
            Date value or None.
        """
        from ..utils.date_utils import DateUtils

        default_str = default.isoformat() if default else None

        while True:
            value = self.prompt(f"{message} (YYYY-MM-DD)", default_str, required)

            if not value:
                return None

            parsed = DateUtils.parse_date(value)
            if parsed:
                return parsed

            print("  Please enter a valid date (YYYY-MM-DD).")

    def prompt_list(
        self,
        message: str,
        separator: str = ","
    ) -> List[str]:
        """
        Prompt for a comma-separated list.

        Args:
            message: Prompt message.
            separator: List separator.

        Returns:
            List of values.
        """
        value = self.prompt(f"{message} (comma-separated)")
        if not value:
            return []

        return [item.strip() for item in value.split(separator) if item.strip()]

    def create_piece_interactive(self) -> Piece:
        """
        Create a new piece through interactive prompts.

        Returns:
            New Piece object (not yet saved).
        """
        print("\n=== Create New Piece ===\n")

        name = self.prompt("Name", required=True)

        piece_types = ["shawl", "scarf", "cowl", "blanket", "hat", "bag", "other"]
        piece_type = self.prompt_choice("Type", piece_types)

        # Dimensions
        print("\nDimensions:")
        width = self.prompt_number("  Width (cm)", required=True)
        length = self.prompt_number("  Length (cm)", required=True)
        depth = self.prompt_number("  Depth (cm)")
        dimensions = Dimensions(width_cm=width, length_cm=length, depth_cm=depth)

        date_started = self.prompt_date("Date started", date.today(), required=True)
        date_finished = self.prompt_date("Date finished (if complete)")

        work_hours = self.prompt_number("Work hours (if known)")

        # Status
        work_statuses = ["in_progress", "finished", "ready"]
        work_status = self.prompt_choice("Work status", work_statuses, "in_progress")

        destinations = ["for_sale", "for_gift", "for_self"]
        destination = self.prompt_choice("Destination", destinations, "for_sale")

        # Linked entities
        yarns = self.prompt_list("Yarn IDs used (e.g., YARN-001, YARN-002)")
        stitches = self.prompt_list("Stitch IDs used (e.g., STITCH-001)")

        hook_size = self.prompt_number("Hook size (mm)")

        notes = self.prompt("Notes")

        piece = Piece(
            id="",  # Will be assigned by data service
            name=name,
            type=piece_type,
            dimensions=dimensions,
            date_started=date_started,
            date_finished=date_finished,
            work_hours=work_hours,
            work_status=work_status,
            destination=destination,
            yarns_used=yarns,
            stitches_used=stitches,
            hook_size_mm=hook_size,
            notes=notes or None,
        )

        return piece

    def create_yarn_interactive(self) -> Yarn:
        """
        Create a new yarn through interactive prompts.

        Returns:
            New Yarn object (not yet saved).
        """
        print("\n=== Create New Yarn ===\n")

        name = self.prompt("Name", required=True)
        brand = self.prompt("Brand")
        color = self.prompt("Color", required=True)
        color_code = self.prompt("Color code")

        materials = ["cotton", "wool", "acrylic", "silk", "blend", "other"]
        material = self.prompt_choice("Material", materials, "cotton")

        composition = self.prompt("Material composition (e.g., 100% Cotton)")

        weight_cats = ["lace", "fingering", "sport", "dk", "worsted", "aran", "bulky"]
        weight = self.prompt_choice("Weight category", weight_cats, "dk")

        ball_weight = self.prompt_number("Ball weight (g)")
        ball_length = self.prompt_number("Ball length (m)")

        price = self.prompt_number("Price paid (EUR)")
        purchase_location = self.prompt("Purchase location")
        purchase_link = self.prompt("Purchase link")
        purchase_date = self.prompt_date("Purchase date")

        quantity = self.prompt_number("Quantity owned", 1)

        hook_size = self.prompt_number("Recommended hook size (mm)")

        notes = self.prompt("Notes")

        yarn = Yarn(
            id="",  # Will be assigned by data service
            name=name,
            brand=brand or None,
            color=color,
            color_code=color_code or None,
            material=material,
            material_composition=composition or None,
            weight_category=weight,
            ball_weight_g=ball_weight,
            ball_length_m=ball_length,
            price_paid=Decimal(str(price)) if price else None,
            purchase_location=purchase_location or None,
            purchase_link=purchase_link or None,
            purchase_date=purchase_date,
            quantity_owned=int(quantity) if quantity else 1,
            hook_size_mm=hook_size,
            notes=notes or None,
        )

        return yarn

    def create_stitch_interactive(self) -> Stitch:
        """
        Create a new stitch through interactive prompts.

        Returns:
            New Stitch object (not yet saved).
        """
        print("\n=== Create New Stitch ===\n")

        name = self.prompt("Name (use Hookfully standard name)", required=True)
        aliases = self.prompt_list("Name aliases (alternative names)")
        name_es = self.prompt("Spanish name")
        abbreviation = self.prompt("Abbreviation (e.g., sc, dc)")

        categories = ["basic", "textured", "lace", "colorwork", "specialty"]
        category = self.prompt_choice("Category", categories, "basic")

        difficulties = ["beginner", "intermediate", "advanced"]
        difficulty = self.prompt_choice("Difficulty", difficulties, "beginner")

        description = self.prompt("Description", required=True)

        hookfully_link = self.prompt("Hookfully link")
        instruction_link = self.prompt("Instruction link")
        video_link = self.prompt("Video link")

        notes = self.prompt("Notes")

        stitch = Stitch(
            id="",  # Will be assigned by data service
            name=name,
            name_aliases=aliases,
            name_es=name_es or None,
            abbreviation=abbreviation or None,
            category=category,
            difficulty=difficulty,
            description=description,
            hookfully_link=hookfully_link or None,
            instruction_link=instruction_link or None,
            video_link=video_link or None,
            notes=notes or None,
        )

        return stitch


def interactive_entry(entity_type: str) -> None:
    """
    Run interactive data entry for an entity type.

    Args:
        entity_type: "piece", "yarn", or "stitch".
    """
    helper = DataEntryHelper()
    data_service = DataService()

    if entity_type == "piece":
        entity = helper.create_piece_interactive()
        entity_id = data_service.create_piece(entity)
    elif entity_type == "yarn":
        entity = helper.create_yarn_interactive()
        entity_id = data_service.create_yarn(entity)
    elif entity_type == "stitch":
        entity = helper.create_stitch_interactive()
        entity_id = data_service.create_stitch(entity)
    else:
        print(f"Unknown entity type: {entity_type}")
        return

    print(f"\nCreated {entity_type} with ID: {entity_id}")

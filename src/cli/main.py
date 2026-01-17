"""
Main CLI entry point for Crochet Project Manager.

Usage:
    python -m src.cli.main <command> [options]

Commands:
    inbox       Process inbox files
    price       Calculate price for a piece
    time        Estimate time for a piece
    list        List entities (pieces, yarns, stitches)
    stats       Show statistics
"""

import argparse
import sys
from typing import List

from ..services import DataService, PriceService, TimeService


def cmd_inbox(args):
    """Process inbox files."""
    from .process_inbox import process_inbox
    process_inbox(args.entity_type)


def cmd_price(args):
    """Calculate price for a piece."""
    price_service = PriceService()

    try:
        breakdown = price_service.calculate_price(args.piece_id)
        print(f"\nPrice Breakdown for {args.piece_id}")
        print("-" * 40)
        print(f"Material cost:      EUR {breakdown.material_cost:.2f}")
        print(f"Labor cost:         EUR {breakdown.labor_cost:.2f}")
        print(f"Subtotal:           EUR {breakdown.subtotal:.2f}")
        print(f"Complexity factor:  {breakdown.complexity_factor:.2f}x")
        print(f"Size factor:        {breakdown.size_factor:.2f}x")
        print(f"Adjustment:         EUR {breakdown.complexity_adjustment:.2f}")
        print(f"Profit margin:      EUR {breakdown.profit_amount:.2f}")
        print("-" * 40)
        print(f"Total:              EUR {breakdown.total:.2f}")
        print(f"Suggested price:    EUR {breakdown.rounded_price:.2f}")

        if args.compare:
            comparison = price_service.compare_to_market(args.piece_id)
            print(f"\nMarket Comparison:")
            print(f"  {comparison.get('recommendation', 'No comparison data')}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_time(args):
    """Estimate time for a piece."""
    time_service = TimeService()

    estimate = time_service.estimate_total_hours(args.piece_id)
    print(f"\nTime Estimate for {args.piece_id}")
    print("-" * 40)
    print(f"Hours logged:       {estimate.total_hours_logged:.1f}")

    if estimate.estimated_total_hours:
        print(f"Estimated total:    {estimate.estimated_total_hours:.1f} hours")
        print(f"Remaining:          {estimate.estimated_remaining_hours:.1f} hours")
        print(f"Confidence:         {estimate.confidence}")
        print(f"Basis:              {estimate.basis}")

    if args.predict and estimate.estimated_remaining_hours:
        completion = time_service.predict_completion_date(
            args.piece_id,
            hours_per_week=args.hours_per_week
        )
        if completion:
            print(f"\nAt {args.hours_per_week} hours/week:")
            print(f"  Predicted completion: {completion}")


def cmd_list(args):
    """List entities."""
    data_service = DataService()

    if args.entity_type == "pieces":
        items = data_service.load_pieces(include_archived=args.all)
        print(f"\nPieces ({len(items)}):")
        for item in items:
            status = f"[{item.work_status}]" if item.work_status else ""
            print(f"  {item.id}: {item.name} {status}")

    elif args.entity_type == "yarns":
        items = data_service.load_yarns(include_archived=args.all)
        print(f"\nYarns ({len(items)}):")
        for item in items:
            qty = f"({item.quantity_owned} balls)" if item.quantity_owned else ""
            print(f"  {item.id}: {item.name} - {item.color} {qty}")

    elif args.entity_type == "stitches":
        items = data_service.load_stitches(include_archived=args.all)
        print(f"\nStitches ({len(items)}):")
        for item in items:
            cat = f"[{item.category}]" if item.category else ""
            print(f"  {item.id}: {item.name} {cat}")


def cmd_stats(args):
    """Show statistics."""
    time_service = TimeService()
    data_service = DataService()

    stats = time_service.get_statistics()

    print("\nCrochet Project Statistics")
    print("=" * 40)
    print(f"Total hours worked:    {stats['total_hours_all_time']:.1f}")
    print(f"Pieces completed:      {stats['pieces_completed']}")
    print(f"Pieces in progress:    {stats['pieces_in_progress']}")

    if stats['averages_by_type']:
        print("\nAverage hours by type:")
        for ptype, data in stats['averages_by_type'].items():
            print(f"  {ptype}: {data['average_hours']:.1f} hours ({data['count']} pieces)")

    # Yarn inventory
    yarns = data_service.load_yarns()
    total_balls = sum(y.quantity_owned or 0 for y in yarns)
    print(f"\nYarn inventory:        {len(yarns)} types, {total_balls} balls")

    # Stitch library
    stitches = data_service.load_stitches()
    print(f"Stitch library:        {len(stitches)} stitches")


def main(argv: List[str] = None):
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Crochet Project Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # inbox command
    inbox_parser = subparsers.add_parser("inbox", help="Process inbox files")
    inbox_parser.add_argument(
        "entity_type",
        choices=["pieces", "yarns", "stitches", "all"],
        help="Entity type to process"
    )

    # price command
    price_parser = subparsers.add_parser("price", help="Calculate price for a piece")
    price_parser.add_argument("piece_id", help="Piece ID (e.g., PIECE-001)")
    price_parser.add_argument(
        "--compare", "-c",
        action="store_true",
        help="Compare to market prices"
    )

    # time command
    time_parser = subparsers.add_parser("time", help="Estimate time for a piece")
    time_parser.add_argument("piece_id", help="Piece ID (e.g., PIECE-001)")
    time_parser.add_argument(
        "--predict", "-p",
        action="store_true",
        help="Predict completion date"
    )
    time_parser.add_argument(
        "--hours-per-week", "-w",
        type=float,
        default=5.0,
        help="Hours worked per week (default: 5)"
    )

    # list command
    list_parser = subparsers.add_parser("list", help="List entities")
    list_parser.add_argument(
        "entity_type",
        choices=["pieces", "yarns", "stitches"],
        help="Entity type to list"
    )
    list_parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Include archived items"
    )

    # stats command
    subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "inbox": cmd_inbox,
        "price": cmd_price,
        "time": cmd_time,
        "list": cmd_list,
        "stats": cmd_stats,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()

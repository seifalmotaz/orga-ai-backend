#!/usr/bin/env python3
"""Command-line interface for database seeding operations."""

import asyncio
import argparse
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.database.seeds.seed_runner import run_all_seeds, clear_all_data, seed_minimal


async def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Database seeding utility for Orga-AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.database.seeds.cli seed --full
  python -m src.database.seeds.cli seed --minimal
  python -m src.database.seeds.cli clear
  python -m src.database.seeds.cli seed --clear-first
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Seed command
    seed_parser = subparsers.add_parser("seed", help="Seed the database with test data")
    seed_group = seed_parser.add_mutually_exclusive_group()
    seed_group.add_argument(
        "--full", 
        action="store_true", 
        help="Seed full test dataset (default)"
    )
    seed_group.add_argument(
        "--minimal", 
        action="store_true", 
        help="Seed minimal test dataset"
    )
    seed_parser.add_argument(
        "--clear-first", 
        action="store_true", 
        help="Clear existing data before seeding"
    )
    
    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear all seed data from database")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show database seeding status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "seed":
            if args.minimal:
                results = await seed_minimal()
            else:
                # Default to full seeding
                results = await run_all_seeds(clear_existing=args.clear_first)
            
            print(f"\n✨ Seeding operation completed successfully!")
            
        elif args.command == "clear":
            from src.database import init
            await init()
            await clear_all_data()
            print("\n✨ Clear operation completed successfully!")
            
        elif args.command == "status":
            await show_status()
            
    except Exception as e:
        print(f"\n❌ Error during {args.command} operation: {e}")
        sys.exit(1)


async def show_status():
    """Show the current status of seeded data."""
    from src.database import init
    from src.database.models import User, Category, Task
    
    await init()
    
    print("📊 Database Seeding Status")
    print("=" * 30)
    
    # Count records
    user_count = await User.all().count()
    category_count = await Category.all().count()
    task_count = await Task.all().count()

    # Count subtasks by checking for non-null parent_task_id
    all_tasks = await Task.all()
    subtask_count = sum(1 for task in all_tasks if task.parent_task_id is not None)
    
    print(f"👥 Users: {user_count}")
    print(f"📁 Categories: {category_count}")
    print(f"📋 Tasks: {task_count}")
    print(f"📝 Subtasks: {subtask_count}")
    print(f"📊 Total records: {user_count + category_count + task_count}")
    
    if user_count > 0:
        print("\n👥 Sample Users:")
        users = await User.all().limit(3)
        for user in users:
            print(f"  • {user.email} ({user.username}) - {user.timezone}")
    
    if task_count > 0:
        print("\n📋 Sample Tasks:")
        tasks = await Task.all().limit(3)
        for task in tasks:
            print(f"  • {task.title} - {task.status} ({task.priority})")


if __name__ == "__main__":
    asyncio.run(main())

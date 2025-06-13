"""Main seed runner for orchestrating database seeding."""

import asyncio
from typing import Optional
from src.database import init
from .user_seeds import seed_users, clear_user_data
from .category_seeds import seed_categories, clear_category_data
from .task_seeds import seed_tasks, seed_subtasks, clear_task_data


async def run_all_seeds(clear_existing: bool = False) -> dict:
    """Run all seed functions in the correct order.

    Args:
        clear_existing: Whether to clear existing data before seeding.

    Returns:
        Dictionary with counts of created records.
    """
    print("🚀 Starting database seeding process...")

    # Initialize database connection
    await init()

    # Clear existing data if requested
    if clear_existing:
        print("\n🧹 Clearing existing data...")
        await clear_all_data()

    # Seed in dependency order
    print("\n📊 Seeding database with test data...")

    # 1. Seed users (no dependencies)
    users = await seed_users()

    # 2. Seed categories (depends on users)
    categories = await seed_categories(users)

    # 3. Seed tasks (depends on users and categories)
    tasks = await seed_tasks(users, categories)

    # 4. Seed subtasks (depends on tasks)
    subtasks = await seed_subtasks(tasks)

    # Summary
    results = {
        "users": len(users),
        "categories": len(categories),
        "tasks": len(tasks),
        "subtasks": len(subtasks),
        "total": len(users) + len(categories) + len(tasks) + len(subtasks),
    }

    print(f"\n🎉 Seeding completed successfully!")
    print(f"   👥 Users: {results['users']}")
    print(f"   📁 Categories: {results['categories']}")
    print(f"   📋 Tasks: {results['tasks']}")
    print(f"   📝 Subtasks: {results['subtasks']}")
    print(f"   📊 Total records: {results['total']}")

    return results


async def clear_all_data():
    """Clear all seeded data from the database in reverse dependency order."""
    print("🧹 Clearing all seed data...")

    # Clear in reverse dependency order
    await clear_task_data()  # Tasks and subtasks
    await clear_category_data()  # Categories
    await clear_user_data()  # Users and devices

    print("✅ All seed data cleared")


async def seed_minimal() -> dict:
    """Seed minimal data for basic testing.

    Returns:
        Dictionary with counts of created records.
    """
    print("🚀 Starting minimal database seeding...")

    # Initialize database connection
    await init()

    # Create just one user with basic data
    from src.database.models import User, Category, Task
    from src.database.models.enums import NotificationType, TaskStatus, Priority

    # Create one test user
    user = await User.create(
        clerk_id="user_test_minimal",
        email="test@example.com",
        username="testuser",
        timezone="UTC",
        default_reminder_minutes=15,
        preferred_notification_type=NotificationType.PUSH,
    )
    print(f"✅ Created test user: {user.email}")

    # Create one category
    category = await Category.create(
        user=user,
        name="Test Category",
        color="#FF6B6B",
    )
    print(f"✅ Created test category: {category.name}")

    # Create one task
    task = await Task.create(
        user=user,
        title="Test Task",
        description="A simple test task for development",
        status=TaskStatus.PENDING,
        priority=Priority.MEDIUM,
        completion_percentage=0,
        category=category,
    )
    print(f"✅ Created test task: {task.title}")

    results = {
        "users": 1,
        "categories": 1,
        "tasks": 1,
        "subtasks": 0,
        "total": 3,
    }

    print(f"\n🎉 Minimal seeding completed!")
    print(f"   📊 Total records: {results['total']}")

    return results


if __name__ == "__main__":
    import sys

    async def main():
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()

            if command == "clear":
                await init()
                await clear_all_data()
            elif command == "minimal":
                await seed_minimal()
            elif command == "full":
                await run_all_seeds(clear_existing=True)
            else:
                print("Usage: python seed_runner.py [clear|minimal|full]")
                print("  clear   - Clear all seed data")
                print("  minimal - Seed minimal test data")
                print("  full    - Seed full test data (default)")
        else:
            # Default: run full seeding
            await run_all_seeds(clear_existing=False)

    asyncio.run(main())

"""Task seed data for testing and development."""

import asyncio
from datetime import date, time, datetime, timedelta
from typing import List, Optional
from src.database.models import Task, User, Category
from src.database.models.enums import TaskStatus, Priority


# Sample task data templates
TASK_SEED_DATA = [
    {
        "title": "Complete quarterly report",
        "description": "Finish the Q4 financial report and submit to management",
        "due_date": date.today() + timedelta(days=7),
        "due_time": time(17, 0),
        "status": TaskStatus.IN_PROGRESS,
        "priority": Priority.HIGH,
        "completion_percentage": 60,
        "estimated_duration": 240,  # 4 hours
        "category_name": "Work",
    },
    {
        "title": "Plan weekend trip",
        "description": "Research destinations and book accommodation for weekend getaway",
        "due_date": date.today() + timedelta(days=3),
        "due_time": time(20, 0),
        "status": TaskStatus.PENDING,
        "priority": Priority.MEDIUM,
        "completion_percentage": 0,
        "estimated_duration": 120,  # 2 hours
        "category_name": "Travel",
    },
    {
        "title": "Morning workout routine",
        "description": "30-minute cardio and strength training session",
        "due_date": date.today() + timedelta(days=1),
        "due_time": "07:00:00",
        "status": TaskStatus.PENDING,
        "priority": Priority.MEDIUM,
        "completion_percentage": 0,
        "estimated_duration": 30,
        "category_name": "Health & Fitness",
    },
    {
        "title": "Read Python documentation",
        "description": "Study advanced Python concepts and best practices",
        "due_date": date.today() + timedelta(days=14),
        "due_time": None,
        "status": TaskStatus.PENDING,
        "priority": Priority.LOW,
        "completion_percentage": 25,
        "estimated_duration": 180,  # 3 hours
        "category_name": "Learning",
    },
    {
        "title": "Grocery shopping",
        "description": "Buy weekly groceries and household items",
        "due_date": date.today() + timedelta(days=2),
        "due_time": "18:00:00",
        "status": TaskStatus.PENDING,
        "priority": Priority.MEDIUM,
        "completion_percentage": 0,
        "estimated_duration": 60,
        "category_name": "Home",
    },
    {
        "title": "Call dentist for appointment",
        "description": "Schedule routine dental checkup",
        "due_date": date.today() + timedelta(days=1),
        "due_time": "09:00:00",
        "status": TaskStatus.PENDING,
        "priority": Priority.HIGH,
        "completion_percentage": 0,
        "estimated_duration": 15,
        "category_name": "Health & Fitness",
    },
    {
        "title": "Update portfolio website",
        "description": "Add recent projects and update contact information",
        "due_date": date.today() + timedelta(days=10),
        "due_time": None,
        "status": TaskStatus.IN_PROGRESS,
        "priority": Priority.MEDIUM,
        "completion_percentage": 40,
        "estimated_duration": 300,  # 5 hours
        "category_name": "Work",
    },
    {
        "title": "Organize digital photos",
        "description": "Sort and backup photos from last vacation",
        "due_date": None,
        "due_time": None,
        "status": TaskStatus.PENDING,
        "priority": Priority.LOW,
        "completion_percentage": 0,
        "estimated_duration": 120,
        "category_name": "Personal",
    },
    {
        "title": "Review monthly budget",
        "description": "Analyze expenses and adjust budget for next month",
        "due_date": date.today() + timedelta(days=5),
        "due_time": "19:00:00",
        "status": TaskStatus.PENDING,
        "priority": Priority.HIGH,
        "completion_percentage": 0,
        "estimated_duration": 90,
        "category_name": "Finance",
    },
    {
        "title": "Team building event planning",
        "description": "Organize team lunch and activities for next month",
        "due_date": date.today() + timedelta(days=21),
        "due_time": None,
        "status": TaskStatus.PENDING,
        "priority": Priority.MEDIUM,
        "completion_percentage": 10,
        "estimated_duration": 180,
        "category_name": "Social",
    },
]

# Completed tasks (for demonstration)
COMPLETED_TASK_DATA = [
    {
        "title": "Submit tax documents",
        "description": "File annual tax return with all required documents",
        "due_date": date.today() - timedelta(days=5),
        "due_time": "23:59:00",
        "status": TaskStatus.COMPLETED,
        "priority": Priority.URGENT,
        "completion_percentage": 100,
        "estimated_duration": 180,
        "actual_duration": 195,
        "completed_at": datetime.now() - timedelta(days=3),
        "category_name": "Finance",
    },
    {
        "title": "Clean garage",
        "description": "Organize tools and dispose of old items",
        "due_date": date.today() - timedelta(days=2),
        "due_time": None,
        "status": TaskStatus.COMPLETED,
        "priority": Priority.LOW,
        "completion_percentage": 100,
        "estimated_duration": 240,
        "actual_duration": 280,
        "completed_at": datetime.now() - timedelta(days=1),
        "category_name": "Home",
    },
]


async def seed_tasks(users: List[User] = None, categories: List[Category] = None) -> List[Task]:
    """Create seed tasks in the database.

    Args:
        users: List of users to create tasks for. If None, gets all users.
        categories: List of categories to assign to tasks. If None, gets all categories.

    Returns:
        List of created Task instances.
    """
    print("🌱 Seeding tasks...")

    if users is None:
        users = await User.all()

    if not users:
        print("  ⚠️  No users found. Please seed users first.")
        return []

    if categories is None:
        categories = await Category.all()

    created_tasks = []

    # Create main tasks for each user
    for i, user in enumerate(users):
        print(f"  👤 Creating tasks for user: {user.email}")

        # Get user's categories
        user_categories = [cat for cat in categories if cat.user_id == user.id]
        category_map = {cat.name: cat for cat in user_categories}

        # Create a subset of tasks for each user (not all tasks for all users)
        user_task_data = TASK_SEED_DATA[i * 2:(i + 1) * 2 + 2]  # 2-4 tasks per user

        for task_data in user_task_data:
            # Check if task already exists for this user
            existing_task = await Task.filter(
                user=user,
                title=task_data["title"]
            ).first()

            if existing_task:
                print(f"    ⚠️  Task '{task_data['title']}' already exists for {user.email}, skipping...")
                created_tasks.append(existing_task)
                continue

            # Prepare task data
            task_data_with_user = task_data.copy()
            task_data_with_user["user"] = user

            # Assign category if available
            category_name = task_data_with_user.pop("category_name", None)
            if category_name and category_name in category_map:
                task_data_with_user["category"] = category_map[category_name]

            # Create task
            task = await Task.create(**task_data_with_user)
            created_tasks.append(task)
            print(f"    ✅ Created task: {task.title} (Status: {task.status}, Priority: {task.priority})")

    # Create some completed tasks for the first user
    if users:
        first_user = users[0]
        user_categories = [cat for cat in categories if cat.user_id == first_user.id]
        category_map = {cat.name: cat for cat in user_categories}

        print(f"  👤 Creating completed tasks for user: {first_user.email}")

        for task_data in COMPLETED_TASK_DATA:
            # Check if task already exists
            existing_task = await Task.filter(
                user=first_user,
                title=task_data["title"]
            ).first()

            if existing_task:
                print(f"    ⚠️  Task '{task_data['title']}' already exists, skipping...")
                continue

            # Prepare task data
            task_data_with_user = task_data.copy()
            task_data_with_user["user"] = first_user

            # Assign category if available
            category_name = task_data_with_user.pop("category_name", None)
            if category_name and category_name in category_map:
                task_data_with_user["category"] = category_map[category_name]

            # Create task
            task = await Task.create(**task_data_with_user)
            created_tasks.append(task)
            print(f"    ✅ Created completed task: {task.title}")

    print(f"✅ Seeded {len(created_tasks)} tasks")
    return created_tasks


async def seed_subtasks(tasks: List[Task] = None) -> List[Task]:
    """Create seed subtasks in the database.

    Args:
        tasks: List of existing tasks to create subtasks for. If None, gets all tasks.

    Returns:
        List of created subtask instances.
    """
    print("🌱 Seeding subtasks...")

    if tasks is None:
        tasks = await Task.all()

    if not tasks:
        print("  ⚠️  No tasks found. Please seed tasks first.")
        return []

    created_subtasks = []

    # Create subtasks based on SUBTASK_DATA
    for subtask_group in SUBTASK_DATA:
        parent_title = subtask_group["parent_title"]

        # Find the parent task
        parent_task = None
        for task in tasks:
            if task.title == parent_title:
                parent_task = task
                break

        if not parent_task:
            print(f"  ⚠️  Parent task '{parent_title}' not found, skipping subtasks...")
            continue

        print(f"  📋 Creating subtasks for: {parent_title}")

        for subtask_data in subtask_group["subtasks"]:
            # Check if subtask already exists
            existing_subtask = await Task.filter(
                user=parent_task.user,
                title=subtask_data["title"],
                parent_task=parent_task
            ).first()

            if existing_subtask:
                print(f"    ⚠️  Subtask '{subtask_data['title']}' already exists, skipping...")
                created_subtasks.append(existing_subtask)
                continue

            # Prepare subtask data
            subtask_data_with_parent = subtask_data.copy()
            subtask_data_with_parent["user"] = parent_task.user
            subtask_data_with_parent["parent_task"] = parent_task
            subtask_data_with_parent["category"] = parent_task.category

            # Create subtask
            subtask = await Task.create(**subtask_data_with_parent)
            created_subtasks.append(subtask)
            print(f"    ✅ Created subtask: {subtask.title} (Status: {subtask.status})")

    print(f"✅ Seeded {len(created_subtasks)} subtasks")
    return created_subtasks


async def clear_task_data():
    """Clear all task data from the database."""
    print("🧹 Clearing task data...")

    deleted_tasks = await Task.all().delete()
    print(f"  🗑️  Deleted {deleted_tasks} tasks")

    print("✅ Task data cleared")


if __name__ == "__main__":
    # For testing the seed function directly
    async def main():
        from src.database import init
        await init()

        # Get users and categories first
        users = await User.all()
        categories = await Category.all()

        if not users:
            print("No users found. Please run user seeds first.")
            return

        if not categories:
            print("No categories found. Please run category seeds first.")
            return

        tasks = await seed_tasks(users, categories)
        await seed_subtasks(tasks)

    asyncio.run(main())

# Parent-child task relationships
SUBTASK_DATA = [
    {
        "parent_title": "Complete quarterly report",
        "subtasks": [
            {
                "title": "Gather financial data",
                "description": "Collect all Q4 financial records and receipts",
                "due_date": date.today() + timedelta(days=2),
                "status": TaskStatus.COMPLETED,
                "priority": Priority.HIGH,
                "completion_percentage": 100,
                "completed_at": datetime.now() - timedelta(hours=12),
            },
            {
                "title": "Create charts and graphs",
                "description": "Design visual representations of financial data",
                "due_date": date.today() + timedelta(days=4),
                "status": TaskStatus.IN_PROGRESS,
                "priority": Priority.MEDIUM,
                "completion_percentage": 70,
            },
            {
                "title": "Write executive summary",
                "description": "Summarize key findings and recommendations",
                "due_date": date.today() + timedelta(days=6),
                "status": TaskStatus.PENDING,
                "priority": Priority.HIGH,
                "completion_percentage": 0,
            },
        ]
    }
]

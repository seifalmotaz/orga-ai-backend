# Database Seeds

This directory contains database seeding functionality for the Orga-AI application. Seeds provide test data for development and testing purposes.

## Overview

The seeding system creates realistic test data for:
- **Users**: Test users with different timezones and preferences
- **Categories**: Common task categories (Work, Personal, Health, etc.)
- **Tasks**: Various tasks with different statuses, priorities, and due dates
- **Subtasks**: Parent-child task relationships

## Quick Start

### Using the CLI (Recommended)

```bash
# Seed full test dataset
python -m src.database.seeds.cli seed --full

# Seed minimal test dataset (1 user, 1 category, 1 task)
python -m src.database.seeds.cli seed --minimal

# Clear existing data and seed fresh
python -m src.database.seeds.cli seed --clear-first

# Clear all seed data
python -m src.database.seeds.cli clear

# Check current status
python -m src.database.seeds.cli status
```

### Using Python directly

```python
import asyncio
from src.database.seeds import run_all_seeds, clear_all_data

# Seed all data
async def seed_db():
    results = await run_all_seeds(clear_existing=True)
    print(f"Created {results['total']} records")

asyncio.run(seed_db())
```

## Seed Data Details

### Users (5 test users)
- **john.doe@example.com** - New York timezone, PUSH notifications
- **jane.smith@example.com** - London timezone, EMAIL notifications  
- **mike.johnson@example.com** - Los Angeles timezone, WEB_PUSH notifications
- **sarah.wilson@example.com** - Tokyo timezone, PUSH notifications
- **alex.brown@example.com** - Sydney timezone, EMAIL notifications

### Categories (8 categories per user)
- Work (Red)
- Personal (Teal)
- Health & Fitness (Blue)
- Learning (Green)
- Home (Yellow)
- Finance (Purple)
- Social (Light Green)
- Travel (Light Yellow)

### Tasks (Various per user)
- **Pending tasks**: New tasks waiting to be started
- **In-progress tasks**: Tasks currently being worked on
- **Completed tasks**: Finished tasks with completion dates
- **Subtasks**: Child tasks linked to parent tasks

### Task Examples
- Complete quarterly report (HIGH priority, IN_PROGRESS)
- Plan weekend trip (MEDIUM priority, PENDING)
- Morning workout routine (MEDIUM priority, PENDING)
- Read Python documentation (LOW priority, PENDING)
- Submit tax documents (URGENT priority, COMPLETED)

## File Structure

```
src/database/seeds/
├── __init__.py           # Package exports
├── README.md            # This documentation
├── cli.py               # Command-line interface
├── seed_runner.py       # Main orchestration
├── user_seeds.py        # User and UserDevice seeds
├── category_seeds.py    # Category seeds
└── task_seeds.py        # Task and subtask seeds
```

## Individual Seed Modules

### user_seeds.py
- Creates test users with realistic data
- Creates user devices for push notifications
- Handles different timezones and preferences

### category_seeds.py  
- Creates common task categories
- Assigns categories to each user
- Uses distinct colors for visual organization

### task_seeds.py
- Creates diverse tasks with various properties
- Includes completed tasks with actual durations
- Creates parent-child task relationships
- Distributes tasks across users and categories

## Development Usage

### Running Tests
The seed data is perfect for testing API endpoints:

```bash
# Seed test data
python -m src.database.seeds.cli seed --full

# Run API tests
make test

# Clear test data
python -m src.database.seeds.cli clear
```

### Custom Seeding
You can also run individual seed functions:

```python
from src.database.seeds import seed_users, seed_categories, seed_tasks

# Seed only users
users = await seed_users()

# Seed categories for specific users  
categories = await seed_categories(users[:2])

# Seed tasks for specific users and categories
tasks = await seed_tasks(users[:1], categories)
```

## Data Relationships

The seeding system maintains proper foreign key relationships:

```
User (1) ──→ (N) Category
User (1) ──→ (N) Task
User (1) ──→ (N) UserDevice
Category (1) ──→ (N) Task
Task (1) ──→ (N) Task (parent-child)
```

## Best Practices

1. **Always clear before production**: Never run seeds in production
2. **Use minimal for quick tests**: Use `--minimal` for fast iteration
3. **Check status regularly**: Use `status` command to verify data
4. **Clear between test runs**: Use `--clear-first` for clean tests

## Troubleshooting

### Common Issues

**"No users found" error**:
```bash
# Make sure to seed users first
python -m src.database.seeds.cli seed --full
```

**Database connection errors**:
```bash
# Check your DATABASE_URL environment variable
echo $DATABASE_URL

# Make sure database is initialized
python -c "from src.database import init; import asyncio; asyncio.run(init())"
```

**Duplicate data warnings**:
- Seeds check for existing data and skip duplicates
- Use `--clear-first` to start fresh

### Getting Help

```bash
# Show CLI help
python -m src.database.seeds.cli --help

# Show command-specific help
python -m src.database.seeds.cli seed --help
```

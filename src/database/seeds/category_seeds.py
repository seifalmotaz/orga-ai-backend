"""Category seed data for testing and development."""

import asyncio
from typing import List
from src.database.models import Category, User


# Sample category data (will be created for each user)
CATEGORY_SEED_DATA = [
    {
        "name": "Work",
        "color": "#FF6B6B",
    },
    {
        "name": "Personal",
        "color": "#4ECDC4",
    },
    {
        "name": "Health & Fitness",
        "color": "#45B7D1",
    },
    {
        "name": "Learning",
        "color": "#96CEB4",
    },
    {
        "name": "Home",
        "color": "#FFEAA7",
    },
    {
        "name": "Finance",
        "color": "#DDA0DD",
    },
    {
        "name": "Social",
        "color": "#98D8C8",
    },
    {
        "name": "Travel",
        "color": "#F7DC6F",
    },
]


async def seed_categories(users: List[User] = None) -> List[Category]:
    """Create seed categories in the database.
    
    Args:
        users: List of users to create categories for. If None, gets all users.
        
    Returns:
        List of created Category instances.
    """
    print("🌱 Seeding categories...")
    
    if users is None:
        users = await User.all()
    
    if not users:
        print("  ⚠️  No users found. Please seed users first.")
        return []
    
    created_categories = []
    
    for user in users:
        print(f"  👤 Creating categories for user: {user.email}")
        
        for category_data in CATEGORY_SEED_DATA:
            # Check if category already exists for this user
            existing_category = await Category.filter(
                user=user, 
                name=category_data["name"]
            ).first()
            
            if existing_category:
                print(f"    ⚠️  Category '{category_data['name']}' already exists for {user.email}, skipping...")
                created_categories.append(existing_category)
                continue
            
            # Create new category
            category_data_with_user = category_data.copy()
            category_data_with_user["user"] = user
            
            category = await Category.create(**category_data_with_user)
            created_categories.append(category)
            print(f"    ✅ Created category: {category.name} ({category.color})")
    
    print(f"✅ Seeded {len(created_categories)} categories")
    return created_categories


async def clear_category_data():
    """Clear all category data from the database."""
    print("🧹 Clearing category data...")
    
    deleted_categories = await Category.all().delete()
    print(f"  🗑️  Deleted {deleted_categories} categories")
    
    print("✅ Category data cleared")


if __name__ == "__main__":
    # For testing the seed function directly
    async def main():
        from src.database import init
        await init()
        
        # Get users first
        users = await User.all()
        if not users:
            print("No users found. Please run user seeds first.")
            return
            
        await seed_categories(users)
    
    asyncio.run(main())

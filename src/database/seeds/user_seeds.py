"""User seed data for testing and development."""

import asyncio
from typing import List
from src.database.models import User, UserDevice
from src.database.models.enums import NotificationType, DeviceType


# Sample user data
USER_SEED_DATA = [
    {
        "clerk_id": "user_2abc123def456ghi789",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "timezone": "America/New_York",
        "default_reminder_minutes": 15,
        "preferred_notification_type": NotificationType.PUSH,
    },
    {
        "clerk_id": "user_3def456ghi789abc123",
        "email": "jane.smith@example.com",
        "username": "janesmith",
        "timezone": "Europe/London",
        "default_reminder_minutes": 30,
        "preferred_notification_type": NotificationType.EMAIL,
    },
    {
        "clerk_id": "user_4ghi789abc123def456",
        "email": "mike.johnson@example.com",
        "username": "mikej",
        "timezone": "America/Los_Angeles",
        "default_reminder_minutes": 10,
        "preferred_notification_type": NotificationType.WEB_PUSH,
    },
    {
        "clerk_id": "user_5abc789def123ghi456",
        "email": "sarah.wilson@example.com",
        "username": "sarahw",
        "timezone": "Asia/Tokyo",
        "default_reminder_minutes": 20,
        "preferred_notification_type": NotificationType.PUSH,
    },
    {
        "clerk_id": "user_6def123ghi456abc789",
        "email": "alex.brown@example.com",
        "username": "alexb",
        "timezone": "Australia/Sydney",
        "default_reminder_minutes": 5,
        "preferred_notification_type": NotificationType.EMAIL,
    },
]

# Sample user device data
USER_DEVICE_SEED_DATA = [
    {
        "device_type": DeviceType.WEB,
        "push_token": None,
        "endpoint_url": "https://fcm.googleapis.com/fcm/send/web_token_1",
        "is_active": True,
    },
    {
        "device_type": DeviceType.IOS,
        "push_token": "ios_push_token_abc123",
        "endpoint_url": None,
        "is_active": True,
    },
    {
        "device_type": DeviceType.ANDROID,
        "push_token": "android_push_token_def456",
        "endpoint_url": None,
        "is_active": True,
    },
    {
        "device_type": DeviceType.DESKTOP,
        "push_token": None,
        "endpoint_url": "https://fcm.googleapis.com/fcm/send/desktop_token_1",
        "is_active": False,
    },
]


async def seed_users() -> List[User]:
    """Create seed users in the database.

    Returns:
        List of created User instances.
    """
    print("🌱 Seeding users...")

    created_users = []

    for user_data in USER_SEED_DATA:
        # Check if user already exists
        existing_user = await User.filter(email=user_data["email"]).first()
        if existing_user:
            print(f"  ⚠️  User {user_data['email']} already exists, skipping...")
            created_users.append(existing_user)
            continue

        # Create new user
        user = await User.create(**user_data)
        created_users.append(user)
        print(f"  ✅ Created user: {user.email} ({user.username})")

        # Create a device for the first few users
        if len(created_users) <= len(USER_DEVICE_SEED_DATA):
            device_data = USER_DEVICE_SEED_DATA[len(created_users) - 1].copy()
            device_data["user"] = user

            device = await UserDevice.create(**device_data)
            print(f"    📱 Created device: {device.device_type} for {user.email}")

    print(f"✅ Seeded {len(created_users)} users")
    return created_users


async def clear_user_data():
    """Clear all user and user device data from the database."""
    print("🧹 Clearing user data...")

    # Delete user devices first (foreign key constraint)
    deleted_devices = await UserDevice.all().delete()
    print(f"  🗑️  Deleted {deleted_devices} user devices")

    # Delete users
    deleted_users = await User.all().delete()
    print(f"  🗑️  Deleted {deleted_users} users")

    print("✅ User data cleared")


if __name__ == "__main__":
    # For testing the seed function directly
    async def main():
        from src.database import init

        await init()
        await seed_users()

    asyncio.run(main())

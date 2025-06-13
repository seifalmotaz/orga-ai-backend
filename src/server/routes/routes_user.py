from src.database.models import User
from robyn import SubRouter, Response, Request
from tortoise.exceptions import DoesNotExist

user_route = SubRouter(__file__, prefix="/users")


@user_route.get("/")
async def get_users():
    """Get all users."""
    try:
        users = await User.all()
        # Convert to list of dictionaries for JSON serialization
        users_data = []
        for user in users:
            users_data.append(
                {
                    "id": user.id,
                    "clerk_id": user.clerk_id,
                    "email": user.email,
                    "username": user.username,
                    "timezone": user.timezone,
                    "default_reminder_minutes": user.default_reminder_minutes,
                    "preferred_notification_type": user.preferred_notification_type,
                    "created_at": user.created_at.isoformat()
                    if user.created_at
                    else None,
                    "updated_at": user.updated_at.isoformat()
                    if user.updated_at
                    else None,
                }
            )
        return users_data
    except Exception as e:
        return {"error": str(e)}


@user_route.get("/:user_id")
async def get_user_by_id(request: Request):
    """Get a user by ID."""
    user_id = request.path_params.get("user_id")
    try:
        user = await User.get(id=user_id)
        user_data = {
            "id": user.id,
            "clerk_id": user.clerk_id,
            "email": user.email,
            "username": user.username,
            "timezone": user.timezone,
            "default_reminder_minutes": user.default_reminder_minutes,
            "preferred_notification_type": user.preferred_notification_type,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
        return {
            "status": "success",
            "data": user_data,
        }
    except DoesNotExist:
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

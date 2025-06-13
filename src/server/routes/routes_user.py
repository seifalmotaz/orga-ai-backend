from src.database.models import User
from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import DoesNotExist
from src.server.middleware.auth import get_current_user
from src.server.utils.jwt import create_access_token
import os

user_route = APIRouter(prefix="/users", tags=["users"])

if os.getenv("DEBUG") == "True":

    @user_route.post("/")
    async def login_user_test(user_id: str):
        token = create_access_token(user_id=user_id)
        return {"token": token}


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


@user_route.get("/{user_id}")
async def get_user_by_id(user_id: str):
    """Get a user by ID."""
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
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_route.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return {
        "id": current_user.id,
        "clerk_id": current_user.clerk_id,
        "email": current_user.email,
        "username": current_user.username,
        "timezone": current_user.timezone,
        "default_reminder_minutes": current_user.default_reminder_minutes,
        "preferred_notification_type": current_user.preferred_notification_type,
        "created_at": current_user.created_at.isoformat()
        if current_user.created_at
        else None,
        "updated_at": current_user.updated_at.isoformat()
        if current_user.updated_at
        else None,
    }

from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from config.db import conn
from schemas.user import userEntity, usersEntity
from bson import ObjectId
from utils.webhook_handler import send_webhook
from auth.auth import get_current_active_user, check_admin_access, get_password_hash

user = APIRouter(prefix="/users")

@user.get('/', response_model=list[dict])
async def find_all_users(current_user: User = Depends(get_current_active_user)):
    return usersEntity(conn.local.user.find())

@user.get('/{id}', response_model=dict)
async def find_one_user(id: str, current_user: User = Depends(get_current_active_user)):
    user = conn.local.user.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return userEntity(user)

@user.post('/', response_model=list[dict])
async def create_user(
    user: User,
    current_user: User = Depends(check_admin_access)  # Only admins can create users
):
    new_user = dict(user)
    new_user["hashed_password"] = get_password_hash(new_user.pop("password", ""))
    conn.local.user.insert_one(new_user)
    await send_webhook("user.created", userEntity(new_user))
    return usersEntity(conn.local.user.find())

@user.put('/{id}', response_model=dict)
async def update_user(
    id: str,
    user: User,
    current_user: User = Depends(check_admin_access)  # Only admins can update users
):
    updated_user = conn.local.user.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(user)},
        return_document=True
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    await send_webhook("user.updated", userEntity(updated_user))
    return userEntity(updated_user)

@user.delete('/{id}', response_model=dict)
async def delete_user(
    id: str,
    current_user: User = Depends(check_admin_access)  # Only admins can delete users
):
    deleted_user = conn.local.user.find_one_and_delete({"_id": ObjectId(id)})
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    await send_webhook("user.deleted", userEntity(deleted_user))
    return userEntity(deleted_user)
    
from .schema import UserCreate, UserRead
from typing import Any, Annotated
from .security import get_password_hash, verify_password, DUMMY_HASH
from pydantic import Field
from ..storage.memory import users 

def create_user(user: UserCreate) -> dict[str,Any] | None:
    """Store a user unless their ID is already in use.

    Args:
        user: Validated user model to store.

    Returns:
        The serialized user data when creation succeeds, or ``None`` when a
        user with the same ID already exists.
    """
    user_data = user.model_dump()
    plain_password: str = user_data.pop("password")
    
    for existing_users in users:
        if (existing_users.get("id") == user_data.get("id")):
            return None
        
    hashed_password = get_password_hash(plain_password)
    user_data["password_hash"] = hashed_password
    
    users.append(user_data)
    created_user: UserRead = UserRead.model_validate(user_data)
    return created_user.model_dump()

def get_user(user_id: int) -> dict[str,Any] | None:
    """Find a stored user by their numeric identifier.

    Args:
        user_id: Unique identifier of the user to find.

    Returns:
        The matching user record, or ``None`` when no match is found.
    """
    for existing_user in users:
        if(existing_user.get("id") == user_id):
            return UserRead(**existing_user).model_dump()
    return None

def delete_user(user_id: int) -> bool:
    for user in users:
        if(user.get("id") == user_id):
            users.remove(user)
            return True
    return False

def authenticate_user(user_id, password: str):
    user = get_user(user_id)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user
from .schema import UserCreate, UserRead, UserUpdate
from typing import Any, Annotated
from .security import get_password_hash, verify_password, DUMMY_HASH
from pydantic import Field
from ..storage.memory import users, departments

def create_user(user: UserCreate) -> dict[str,Any] | None:
    """Store a user unless their ID is already in use.

    Args:
        user: Validated user model to store.

    Returns:
        The serialized user data when creation succeeds, or ``None`` when a
        user with the same ID already exists.
    """
    user_data = user.model_dump(mode="json")
    if not department_exists(user_data["department_id"]):
        return None
    plain_password: str = user_data.pop("password")
    
    for existing_users in users:
        if (
            existing_users.get("id") == user_data.get("id")
            or existing_users.get("username") == user_data.get("username")
            or existing_users.get("email") == user_data.get("email")
        ):
            return None
        
    hashed_password = get_password_hash(plain_password)
    user_data["password_hash"] = hashed_password
    
    users.append(user_data)
    created_user: UserRead = UserRead.model_validate(user_data)
    return created_user.model_dump()

def get_users() -> list[dict[str, Any]]:
    return [UserRead.model_validate(user).model_dump() for user in users]

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

def update_user(user_id: int, user_update: UserUpdate) -> dict[str, Any] | None:
    update_data = user_update.model_dump(mode="json", exclude_unset=True)
    existing_user = get_user_record(user_id)
    if existing_user is None:
        return None
    if "department_id" in update_data and not department_exists(update_data["department_id"]):
        return None
    for user in users:
        if user.get("id") == user_id:
            continue
        if "username" in update_data and user.get("username") == update_data["username"]:
            return None
        if "email" in update_data and user.get("email") == update_data["email"]:
            return None
    plain_password = update_data.pop("password", None)
    if plain_password is not None:
        update_data["password_hash"] = get_password_hash(plain_password)
    existing_user.update(update_data)
    return UserRead.model_validate(existing_user).model_dump()

def delete_user(user_id: int) -> bool:
    for user in users:
        if(user.get("id") == user_id):
            users.remove(user)
            return True
    return False

def authenticate_user(user_id, password: str):
    user = get_user_record(user_id)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user["password_hash"]):
        return False
    return UserRead.model_validate(user).model_dump()

def get_user_record(user_id: int) -> dict[str, Any] | None:
    for user in users:
        if user.get("id") == user_id:
            return user
    return None

def department_exists(department_id: int) -> bool:
    for department in departments:
        if department.get("id") == department_id:
            return True
    return False

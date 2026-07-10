from .schema import UserCreate, UserRead, UserUpdate
from typing import Any
from ..auth.security import get_password_hash, verify_password, DUMMY_HASH
from ..storage.memory import users, departments
from .exceptions import (
    InvalidDepartmentError,
    DuplicateUserError,
    UserNotFoundError,
    UserDeleteError,
    UserIncorrectPasswordError,
)
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
        raise InvalidDepartmentError(f"Department {user_data['department_id']} does not exist")
    plain_password: str = user_data.pop("password")
    
    for existing_users in users:
        if (
            existing_users.get("id") == user_data.get("id")
            or existing_users.get("username") == user_data.get("username")
            or existing_users.get("email") == user_data.get("email")
        ):
            raise DuplicateUserError("Duplicate User")
        
    hashed_password = get_password_hash(plain_password)
    user_data["password_hash"] = hashed_password
    
    users.append(user_data)
    created_user: UserRead = UserRead.model_validate(user_data)
    return created_user.model_dump()

def get_users() -> list[dict[str, Any]]:
    return [UserRead.model_validate(user).model_dump() for user in users]

def get_user(user_id: int) -> dict[str, Any]:
    """Find a stored user by their numeric identifier.

    Args:
        user_id: Unique identifier of the user to find.

    Returns:
        The matching user record.

    Raises:
        UserNotFoundError: When no user with ``user_id`` exists.
    """
    if user_id >= 1:
        for existing_user in users:
            if existing_user.get("id") == user_id:
                return UserRead(**existing_user).model_dump()
    raise UserNotFoundError(f"User with id {user_id} does not exist")

def update_user(user_id: int, user_update: UserUpdate) -> dict[str, Any]:
    """Apply partial updates to a stored user.

    Args:
        user_id: Unique identifier of the user to update.
        user_update: Validated set of fields to change.

    Returns:
        The serialized user data after the update is applied.

    Raises:
        UserNotFoundError: When no user with ``user_id`` exists.
        InvalidDepartmentError: When the new department does not exist.
        DuplicateUserError: When the new username or email is already in use.
    """
    update_data = user_update.model_dump(mode="json", exclude_unset=True)
    existing_user = get_user_record(user_id)
    if existing_user is None:
        raise UserNotFoundError(f"User with id {user_id} does not exist")
    if "department_id" in update_data and not department_exists(update_data["department_id"]):
        raise InvalidDepartmentError(f"Department {update_data['department_id']} does not exist")
    for user in users:
        if user.get("id") == user_id:
            continue
        if "username" in update_data and user.get("username") == update_data["username"]:
            raise DuplicateUserError("Duplicate User")
        if "email" in update_data and user.get("email") == update_data["email"]:
            raise DuplicateUserError("Duplicate User")
    plain_password = update_data.pop("password", None)
    if plain_password is not None:
        update_data["password_hash"] = get_password_hash(plain_password)
    existing_user.update(update_data)
    return UserRead.model_validate(existing_user).model_dump()

def delete_user(user_id: int) -> None:
    """Remove a stored user by their numeric identifier.

    Args:
        user_id: Unique identifier of the user to delete.

    Raises:
        UserDeleteError: When no user with ``user_id`` exists.
    """
    for user in users:
        if user.get("id") == user_id:
            users.remove(user)
            return
    raise UserDeleteError(f"User with id {user_id} not found")

def get_user_record(user_id: int) -> dict[str, Any]:
    for user in users:
        if user.get("id") == user_id:
            return user
    raise UserNotFoundError(f"User with id: {user_id} not found")

def department_exists(department_id: int) -> bool:
    for department in departments:
        if department.get("id") == department_id:
            return True
    return False

def get_user_record_by_name(username: str) -> dict[str,Any]:
    for user in users:
        if user["username"] == username:
            return user
    raise UserNotFoundError(f"User with username: {username} not found")
from ..auth.security import verify_password, DUMMY_HASH
from .exceptions import (
    UserIncorrectPasswordError,
)
from ..users.services import get_user_by_name
from typing import Any
from ..users.schema import UserRead
from ..users.exceptions import UserNotFoundError
def authenticate_user(username: str, password: str) -> dict[str, Any]:
    """Verify a user's credentials.

    Args:
        username: Username of the user to identify
        password: Plain-text password to verify.

    Returns:
        The serialized user data when the credentials are valid.

    Raises:
        UserIncorrectPasswordError: When the user does not exist or the
            password does not match.
    """
    try:
        user = get_user_by_name(username)
    except UserNotFoundError:
        verify_password(password, DUMMY_HASH)
        raise UserIncorrectPasswordError("Incorrect username or password")
    if not verify_password(password, user["password_hash"]):
        raise UserIncorrectPasswordError("Incorrect username or password")
    return UserRead.model_validate(user).model_dump()
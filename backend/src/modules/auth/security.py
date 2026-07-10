from typing import Annotated, cast
from pwdlib import PasswordHash
from pydantic import Field
from fastapi.security import OAuth2PasswordBearer
import datetime as dt 
from starlette import status
from jose import jwt
import os
from .schema import Token

_secret_key = os.getenv("SECRET_KEY")
_algorithm = os.getenv("ALGORITHM")

if not _secret_key or not _algorithm:
    raise RuntimeError("SECRET_KEY and ALGORITHM must be set in the environment")

SECRET_KEY = cast(str, _secret_key)
ALGORITHM = cast(str, _algorithm)

password_hash = PasswordHash.recommended()
DUMMY_HASH= password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
def get_password_hash(password: Annotated[str, Field(min_length=5)]):
    return password_hash.hash(password)

def verify_password(plain_password: Annotated[str, Field(min_length=5)], hashed_password: Annotated[str, Field(min_length=5)]):
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(username: str, user_id: int, expiry_time: dt.timedelta) -> str:
    encode= {'sub': username, 'id': user_id}
    expires = dt.datetime.now(dt.timezone.utc) + expiry_time
    encode.update({'exp': expires})
    return jwt.encode(encode, str(SECRET_KEY), algorithm=str(ALGORITHM))
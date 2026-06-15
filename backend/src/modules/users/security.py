from typing import Annotated
from pwdlib import PasswordHash
from pydantic import Field
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


password_hash = PasswordHash.recommended()
DUMMY_HASH= password_hash.hash("dummypassword")

def get_password_hash(password: Annotated[str, Field(min_length=5)]):
    return password_hash.hash(password)

def verify_password(plain_password: Annotated[str, Field(min_length=5)], hashed_password: Annotated[str, Field(min_length=5)]):
    return password_hash.verify(plain_password, hashed_password)
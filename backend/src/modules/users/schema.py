from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
# NOTE: UserCreate includes id and plaintext password only for the in-memory alpha.
# PostgreSQL/auth will replace this with generated IDs and password hashes.

class UserCreate(BaseModel):
    id: Annotated[int, Field(ge=1)] #TODO remove when Database replaces in-memory storage
    username: Annotated[str, Field(min_length=3, max_length=30)]
    email: EmailStr
    password: Annotated[str, Field(min_length=5)] 
    department_id: Annotated[int, Field(ge=1)]

class UserRead(BaseModel):
    id: Annotated[int, Field(ge=1)]
    username: Annotated[str, Field(min_length=3, max_length=30)]
    email: EmailStr
    department_id: Annotated[int, Field(ge=1)]
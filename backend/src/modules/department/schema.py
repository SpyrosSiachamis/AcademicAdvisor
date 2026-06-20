from pydantic import BaseModel, Field
from typing import Annotated

class DepartmentCreate(BaseModel):
    id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=3)]
    university_id: Annotated[int, Field(gt=0)]

class DepartmentRead(BaseModel):
    id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=3)]
    university_id: Annotated[int, Field(gt=0)]

class DepartmentUpdate(BaseModel):
    name: Annotated[str, Field(min_length=3)] | None = None
    university_id: Annotated[int, Field(gt=0)] | None = None

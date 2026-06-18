from pydantic import BaseModel, Field
from typing import Annotated, Any

class DepartmentCreate(BaseModel):
    department_id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=3)]
    university_id: Annotated[int, Field(gt=0)]

class DepartmentRead(BaseModel):
    name: Annotated[str, Field(min_length=3)]
    university_id: Annotated[int, Field(gt=0)]
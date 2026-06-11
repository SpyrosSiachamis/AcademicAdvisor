from pydantic import BaseModel, Field 
from typing import Annotated

class Course(BaseModel):
    id: Annotated[int, Field(ge=0)]
    department_id: Annotated[int, Field(ge=0)]
    ects: Annotated[int, Field(gt=0, lt=40)]
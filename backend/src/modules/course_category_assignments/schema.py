from pydantic import BaseModel, Field
from typing import Annotated


class CourseCategoryAssignment(BaseModel):
    id: Annotated[int, Field(gt=0)]
    course_id: Annotated[int, Field(gt=0)]
    category_id: Annotated[int, Field(gt=0)]


class CourseCategoryAssignmentUpdate(BaseModel):
    course_id: Annotated[int, Field(gt=0)] | None = None
    category_id: Annotated[int, Field(gt=0)] | None = None

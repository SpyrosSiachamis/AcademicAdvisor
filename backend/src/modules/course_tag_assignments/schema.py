from pydantic import BaseModel, Field
from typing import Annotated


class CourseTagAssignment(BaseModel):
    id: Annotated[int, Field(gt=0)]
    course_id: Annotated[int, Field(gt=0)]
    tag_id: Annotated[int, Field(gt=0)]


class CourseTagAssignmentUpdate(BaseModel):
    course_id: Annotated[int, Field(gt=0)] | None = None
    tag_id: Annotated[int, Field(gt=0)] | None = None

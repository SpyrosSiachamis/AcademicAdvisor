from pydantic import BaseModel, Field
from typing import Annotated


class CoursePrerequisiteGroup(BaseModel):
    id: Annotated[int, Field(gt=0)]
    course_id: Annotated[int, Field(gt=0)]


class CoursePrerequisiteGroupUpdate(BaseModel):
    course_id: Annotated[int, Field(gt=0)] | None = None

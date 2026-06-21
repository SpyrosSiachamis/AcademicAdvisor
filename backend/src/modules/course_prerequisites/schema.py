from pydantic import BaseModel, Field
from typing import Annotated


class CoursePrerequisite(BaseModel):
    id: Annotated[int, Field(gt=0)]
    course_id: Annotated[int, Field(gt=0)]
    prerequisite_course_id: Annotated[int, Field(gt=0)]


class CoursePrerequisiteUpdate(BaseModel):
    course_id: Annotated[int, Field(gt=0)] | None = None
    prerequisite_course_id: Annotated[int, Field(gt=0)] | None = None

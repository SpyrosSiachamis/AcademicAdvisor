from pydantic import BaseModel, Field
from typing import Annotated


class CoursePrerequisite(BaseModel):
    id: Annotated[int, Field(gt=0)]
    prerequisite_course_id: Annotated[int, Field(gt=0)]
    group_id: Annotated[int, Field(gt=0)]


class CoursePrerequisiteUpdate(BaseModel):
    prerequisite_course_id: Annotated[int, Field(gt=0)] | None = None
    group_id: Annotated[int, Field(gt=0)] | None = None

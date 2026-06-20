from pydantic import BaseModel, Field
from typing import Annotated


class DepartmentCourse(BaseModel):
    id: Annotated[int, Field(gt=0)]
    department_id: Annotated[int, Field(gt=0)]
    course_id: Annotated[int, Field(gt=0)]
    department_course_code: Annotated[str, Field(min_length=2, max_length=20)]
    is_owner: bool


class DepartmentCourseUpdate(BaseModel):
    department_id: Annotated[int, Field(gt=0)] | None = None
    course_id: Annotated[int, Field(gt=0)] | None = None
    department_course_code: Annotated[str, Field(min_length=2, max_length=20)] | None = None
    is_owner: bool | None = None

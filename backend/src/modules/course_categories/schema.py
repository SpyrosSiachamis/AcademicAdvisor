from pydantic import BaseModel, Field
from typing import Annotated


class CourseCategory(BaseModel):
    id: Annotated[int, Field(gt=0)]
    code: Annotated[str, Field(min_length=2, max_length=20)]
    name: Annotated[str, Field(min_length=2, max_length=50)]


class CourseCategoryUpdate(BaseModel):
    code: Annotated[str, Field(min_length=2, max_length=20)] | None = None
    name: Annotated[str, Field(min_length=2, max_length=50)] | None = None

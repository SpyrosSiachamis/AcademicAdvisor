from pydantic import BaseModel, Field
from typing import Annotated


class CourseSuggested(BaseModel):
    id: Annotated[int, Field(gt=0)]
    course_id: Annotated[int, Field(gt=0)]
    suggested_course_id: Annotated[int, Field(gt=0)]


class CourseSuggestedUpdate(BaseModel):
    course_id: Annotated[int, Field(gt=0)] | None = None
    suggested_course_id: Annotated[int, Field(gt=0)] | None = None

from pydantic import BaseModel, Field
from typing import Annotated


Rating = Annotated[float, Field(ge=1, le=5)]


class CourseRating(BaseModel):
    id: Annotated[int, Field(gt=0)]
    course_id: Annotated[int, Field(gt=0)]
    user_id: Annotated[int, Field(gt=0)]
    difficulty_rating: Rating
    workload_rating: Rating
    enjoyment_rating: Rating
    interest_rating: Rating


class CourseRatingUpdate(BaseModel):
    course_id: Annotated[int, Field(gt=0)] | None = None
    user_id: Annotated[int, Field(gt=0)] | None = None
    difficulty_rating: Rating | None = None
    workload_rating: Rating | None = None
    enjoyment_rating: Rating | None = None
    interest_rating: Rating | None = None

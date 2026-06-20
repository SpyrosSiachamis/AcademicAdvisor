from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class Course(BaseModel):
    id: Annotated[int, Field(ge=1)]
    department_id: Annotated[int, Field(ge=1)]
    ects: Annotated[int, Field(gt=0, lt=40)]
    code: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[A-Z]{2,3}-\d{3}$")]
    name: Annotated[str, Field(min_length=2, max_length=50)]
    prerequisites: list[Annotated[int, Field(ge=1)]] = Field(default_factory=list) # Not permament, will be normalized
    suggested: list[Annotated[int, Field(ge=1)]] = Field(default_factory=list)     # Not permament, will be normalized
    contact_email: EmailStr | None = None
    difficulty_estimate: Annotated[float, Field(ge=1, le=5)] | None = None
    workload_estimate: Annotated[float, Field(ge=1, le=5)] | None = None

class CourseUpdate(BaseModel):
    department_id: Annotated[int, Field(ge=1)] | None = None
    ects: Annotated[int, Field(gt=0, lt=40)] | None = None
    code: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[A-Z]{2,3}-\d{3}$")] | None = None
    name: Annotated[str, Field(min_length=2, max_length=50)] | None = None
    prerequisites: list[Annotated[int, Field(ge=1)]] | None = None
    suggested: list[Annotated[int, Field(ge=1)]] | None = None
    contact_email: EmailStr | None = None
    difficulty_estimate: Annotated[float, Field(ge=1, le=5)] | None = None
    workload_estimate: Annotated[float, Field(ge=1, le=5)] | None = None

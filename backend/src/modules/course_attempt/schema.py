from pydantic import BaseModel, Field
from typing import Annotated,Any, ClassVar
from enum import Enum
import datetime

class Status(Enum):
    in_progress = 0
    failed = 1
    passed = 2
    ungraded = 3

class CoursePeriod(Enum):
    winter = 0
    spring = 1
    entire_year = 2
    summer = 3

class CourseAttempt(BaseModel):
    CURRENT_YEAR: ClassVar[datetime.datetime] = datetime.datetime.now()
    id: Annotated[int, Field(gt=0)]
    course_id: Annotated[int, Field(gt=0)]
    user_id: Annotated[int, Field(gt=0)]
    status: Status
    grade: Annotated[float, Field(ge=0, le=10)] | None
    course_period: CoursePeriod
    semester: Annotated[int, Field(ge=1, le=20)]
    academic_year: Annotated[int, Field(gt=2000, le=CURRENT_YEAR.year)] # eg. 2025 = "2025-2026". So. academic year - academic_year+1
    attempt_number: Annotated[int, Field(gt=0)]
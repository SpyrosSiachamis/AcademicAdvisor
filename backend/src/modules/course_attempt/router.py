from fastapi import APIRouter
from typing import Any
from .schema import CourseAttempt
router = APIRouter(prefix='/attempt', tags=['attempt', 'Course Attempt'])

@router.post('/add')
async def create_course_attempt(
    attempt: CourseAttempt
):
    return attempt
    # raise NotImplementedError()



# user_id: int,
#     course_id: int,
#     course_period: CoursePeriod, 
#     semester: int, 
#     academic_year: int, 
#     attempt_number: int,
#     status: Status = Status.in_progress, 
#     grade: float | None = None
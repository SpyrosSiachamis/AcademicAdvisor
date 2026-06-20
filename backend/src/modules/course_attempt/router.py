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
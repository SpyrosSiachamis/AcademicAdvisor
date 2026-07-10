from fastapi import APIRouter, HTTPException, Depends
from .schema import CourseAttempt, CourseAttemptUpdate
from .services import add_attempt, get_attempts, get_attempt, update_attempt, delete_attempt
from ..auth.dependencies import get_current_user
router = APIRouter(prefix='/attempt', tags=['attempt', 'Course Attempt'])

@router.post('/')
async def create_course_attempt_route(attempt: CourseAttempt, current_user: dict = Depends(get_current_user)):
    return await create_course_attempt(attempt)

@router.post('/add')
async def create_course_attempt(attempt: CourseAttempt, current_user: dict = Depends(get_current_user)):
    result = add_attempt(attempt)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate attempt or missing user/course")
    return {
        "message": "Course attempt created successfully",
        "created_attempt": result
    }

@router.get('/')
async def list_course_attempts(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Retrieved all course attempts",
        "attempts": get_attempts()
    }

@router.get('/{attempt_id}')
async def get_course_attempt(attempt_id: int, current_user: dict = Depends(get_current_user)):
    result = get_attempt(attempt_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course attempt not found")
    return {
        "message": "Course attempt found",
        "attempt": result
    }

@router.put('/{attempt_id}')
async def update_course_attempt(attempt_id: int, attempt_update: CourseAttemptUpdate, current_user: dict = Depends(get_current_user)):
    result = update_attempt(attempt_id, attempt_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Course attempt not found or missing user/course")
    return {
        "message": "Course attempt updated successfully",
        "attempt": result
    }

@router.delete('/{attempt_id}')
async def remove_course_attempt(attempt_id: int, current_user: dict = Depends(get_current_user)):
    result = delete_attempt(attempt_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course attempt not found")
    return {
        "message": "Course attempt deleted successfully"
    }

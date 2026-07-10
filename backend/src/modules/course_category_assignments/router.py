from fastapi import APIRouter, HTTPException, Depends

from .schema import CourseCategoryAssignment, CourseCategoryAssignmentUpdate
from .service import create_course_category_assignment, delete_course_category_assignment, get_course_category_assignment, get_course_category_assignments, update_course_category_assignment
from ..auth.dependencies import get_current_user


router = APIRouter(prefix="/course-category-assignments", tags=["course category assignments"])


@router.post("/")
async def add_course_category_assignment(assignment: CourseCategoryAssignment, current_user: dict = Depends(get_current_user)):
    result = create_course_category_assignment(assignment)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate assignment or missing course/category")
    return {"message": "Course category assignment created successfully", "assignment": result}


@router.get("/")
async def list_course_category_assignments():
    return {"message": "Retrieved all course category assignments", "assignments": get_course_category_assignments()}


@router.get("/{assignment_id}")
async def get_course_category_assignment_by_id(assignment_id: int):
    result = get_course_category_assignment(assignment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course category assignment not found")
    return {"message": "Course category assignment found", "assignment": result}


@router.put("/{assignment_id}")
async def update_course_category_assignment_by_id(assignment_id: int, assignment_update: CourseCategoryAssignmentUpdate, current_user: dict = Depends(get_current_user)):
    result = update_course_category_assignment(assignment_id, assignment_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Assignment not found, duplicate pair, or missing course/category")
    return {"message": "Course category assignment updated successfully", "assignment": result}


@router.delete("/{assignment_id}")
async def delete_course_category_assignment_by_id(assignment_id: int, current_user: dict = Depends(get_current_user)):
    result = delete_course_category_assignment(assignment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course category assignment not found")
    return {"message": "Course category assignment deleted successfully"}

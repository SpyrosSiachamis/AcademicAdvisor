from fastapi import APIRouter, HTTPException, Depends

from .schema import CourseTagAssignment, CourseTagAssignmentUpdate
from .service import create_course_tag_assignment, delete_course_tag_assignment, get_course_tag_assignment, get_course_tag_assignments, update_course_tag_assignment
from ..auth.dependencies import get_current_user


router = APIRouter(prefix="/course-tag-assignments", tags=["course tag assignments"])


@router.post("/")
async def add_course_tag_assignment(assignment: CourseTagAssignment, current_user: dict = Depends(get_current_user)):
    result = create_course_tag_assignment(assignment)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate assignment or missing course/tag")
    return {"message": "Course tag assignment created successfully", "assignment": result}


@router.get("/")
async def list_course_tag_assignments():
    return {"message": "Retrieved all course tag assignments", "assignments": get_course_tag_assignments()}


@router.get("/{assignment_id}")
async def get_course_tag_assignment_by_id(assignment_id: int):
    result = get_course_tag_assignment(assignment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course tag assignment not found")
    return {"message": "Course tag assignment found", "assignment": result}


@router.put("/{assignment_id}")
async def update_course_tag_assignment_by_id(assignment_id: int, assignment_update: CourseTagAssignmentUpdate, current_user: dict = Depends(get_current_user)):
    result = update_course_tag_assignment(assignment_id, assignment_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Assignment not found, duplicate pair, or missing course/tag")
    return {"message": "Course tag assignment updated successfully", "assignment": result}


@router.delete("/{assignment_id}")
async def delete_course_tag_assignment_by_id(assignment_id: int, current_user: dict = Depends(get_current_user)):
    result = delete_course_tag_assignment(assignment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course tag assignment not found")
    return {"message": "Course tag assignment deleted successfully"}

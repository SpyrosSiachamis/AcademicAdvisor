from fastapi import APIRouter, HTTPException, Depends

from .schema import CourseSuggested, CourseSuggestedUpdate
from .service import create_course_suggested, delete_course_suggested, get_course_suggested, get_course_suggested_by_id, update_course_suggested
from ..auth.dependencies import get_current_user


router = APIRouter(prefix="/course-suggested", tags=["course suggested"])


@router.post("/")
async def add_course_suggested(suggested: CourseSuggested, current_user: dict = Depends(get_current_user)):
    result = create_course_suggested(suggested)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate suggested course or missing course")
    return {"message": "Course suggested created successfully", "suggested": result}


@router.get("/")
async def list_course_suggested():
    return {"message": "Retrieved all course suggested records", "suggested": get_course_suggested()}


@router.get("/{suggested_id}")
async def get_course_suggested_record_by_id(suggested_id: int):
    result = get_course_suggested_by_id(suggested_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course suggested record not found")
    return {"message": "Course suggested record found", "suggested": result}


@router.put("/{suggested_id}")
async def update_course_suggested_by_id(suggested_id: int, suggested_update: CourseSuggestedUpdate, current_user: dict = Depends(get_current_user)):
    result = update_course_suggested(suggested_id, suggested_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Suggested record not found, duplicate pair, or missing course")
    return {"message": "Course suggested updated successfully", "suggested": result}


@router.delete("/{suggested_id}")
async def delete_course_suggested_by_id(suggested_id: int, current_user: dict = Depends(get_current_user)):
    result = delete_course_suggested(suggested_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course suggested record not found")
    return {"message": "Course suggested deleted successfully"}

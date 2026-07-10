from fastapi import APIRouter, HTTPException, Depends

from .schema import CourseCategory, CourseCategoryUpdate
from .service import create_course_category, delete_course_category, get_course_categories, get_course_category, update_course_category
from ..auth.dependencies import get_current_user


router = APIRouter(prefix="/course-categories", tags=["course categories"])


@router.post("/")
async def add_course_category(category: CourseCategory, current_user: dict = Depends(get_current_user)):
    result = create_course_category(category)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate course category")
    return {"message": "Course category created successfully", "category": result}


@router.get("/")
async def list_course_categories():
    return {"message": "Retrieved all course categories", "categories": get_course_categories()}


@router.get("/{category_id}")
async def get_course_category_by_id(category_id: int):
    result = get_course_category(category_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course category not found")
    return {"message": "Course category found", "category": result}


@router.put("/{category_id}")
async def update_course_category_by_id(category_id: int, category_update: CourseCategoryUpdate, current_user: dict = Depends(get_current_user)):
    result = update_course_category(category_id, category_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Course category not found or duplicate value")
    return {"message": "Course category updated successfully", "category": result}


@router.delete("/{category_id}")
async def delete_course_category_by_id(category_id: int, current_user: dict = Depends(get_current_user)):
    result = delete_course_category(category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course category not found")
    return {"message": "Course category deleted successfully"}

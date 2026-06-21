from fastapi import APIRouter, HTTPException

from .schema import CoursePrerequisite, CoursePrerequisiteUpdate
from .service import create_course_prerequisite, delete_course_prerequisite, get_course_prerequisite, get_course_prerequisites, update_course_prerequisite


router = APIRouter(prefix="/course-prerequisites", tags=["course prerequisites"])


@router.post("/")
async def add_course_prerequisite(prerequisite: CoursePrerequisite):
    result = create_course_prerequisite(prerequisite)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate prerequisite or missing course")
    return {"message": "Course prerequisite created successfully", "prerequisite": result}


@router.get("/")
async def list_course_prerequisites():
    return {"message": "Retrieved all course prerequisites", "prerequisites": get_course_prerequisites()}


@router.get("/{prerequisite_id}")
async def get_course_prerequisite_by_id(prerequisite_id: int):
    result = get_course_prerequisite(prerequisite_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course prerequisite not found")
    return {"message": "Course prerequisite found", "prerequisite": result}


@router.put("/{prerequisite_id}")
async def update_course_prerequisite_by_id(prerequisite_id: int, prerequisite_update: CoursePrerequisiteUpdate):
    result = update_course_prerequisite(prerequisite_id, prerequisite_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Prerequisite not found, duplicate pair, or missing course")
    return {"message": "Course prerequisite updated successfully", "prerequisite": result}


@router.delete("/{prerequisite_id}")
async def delete_course_prerequisite_by_id(prerequisite_id: int):
    result = delete_course_prerequisite(prerequisite_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course prerequisite not found")
    return {"message": "Course prerequisite deleted successfully"}

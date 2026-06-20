from fastapi import APIRouter, HTTPException

from .schema import DepartmentCourse, DepartmentCourseUpdate
from .service import create_department_course, delete_department_course, get_department_course, get_department_courses, update_department_course


router = APIRouter(prefix="/department-courses", tags=["department courses"])


@router.post("/")
async def add_department_course(department_course: DepartmentCourse):
    result = create_department_course(department_course)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate department course or missing department/course")
    return {"message": "Department course created successfully", "department_course": result}


@router.get("/")
async def list_department_courses():
    return {"message": "Retrieved all department courses", "department_courses": get_department_courses()}


@router.get("/{department_course_id}")
async def get_department_course_by_id(department_course_id: int):
    result = get_department_course(department_course_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Department course not found")
    return {"message": "Department course found", "department_course": result}


@router.put("/{department_course_id}")
async def update_department_course_by_id(department_course_id: int, department_course_update: DepartmentCourseUpdate):
    result = update_department_course(department_course_id, department_course_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Department course not found, duplicate pair, or missing department/course")
    return {"message": "Department course updated successfully", "department_course": result}


@router.delete("/{department_course_id}")
async def delete_department_course_by_id(department_course_id: int):
    result = delete_department_course(department_course_id)
    if not result:
        raise HTTPException(status_code=404, detail="Department course not found")
    return {"message": "Department course deleted successfully"}

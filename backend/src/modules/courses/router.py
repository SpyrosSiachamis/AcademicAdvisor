"""HTTP routes for creating and retrieving courses."""

from fastapi import APIRouter, HTTPException
from .schema import Course, CourseUpdate
from .service import create_course, get_all_courses, get_course_by_id, get_course_by_code, update_course, delete_course_from_id, delete_course_from_code, get_all_course_ids

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post('/')
async def create_course_route(course: Course):
    return await add_course(course)

@router.post('/add')
async def add_course(course: Course):
    """Create a course from the validated request body.

    Args:
        course: Course data validated against the ``Course`` schema.

    Returns:
        A response containing a confirmation message and the created course.

    Raises:
        HTTPException: If a course with the same ID already exists.
    """
    result = create_course(course)
    if(result is None):
        raise HTTPException(status_code=409, detail="Duplicate course or missing department")
    return{
        "message": "Course Created",
        "created_course": result
    }

@router.get('/')
async def get_courses():
    """Return every course currently available.

    Returns:
        A response containing a confirmation message and the course list.
    """
    available_courses = get_all_courses()
    return{
        "message": "Retrieved all courses",
        "courses": available_courses
    }

@router.get("/ids")
def get_course_ids():
    """Return every course id currently available.
    Returns:
        A response containing a confirmation message and the course id list.
    """
    available_courses = get_all_course_ids()
    return{
        "message": "Retrieved all courses",
        "course_ids": available_courses
    }

@router.get("/code/{course_code}")
async def get_course_with_code(course_code: str):
    """Retrieve a course by its course code.

    Args:
        course_code: Code of the course to retrieve.

    Returns:
        A response containing a confirmation message and the matching course.

    Raises:
        HTTPException: If no course has the requested code.
    """
    result = get_course_by_code(course_code)
    if(result is None):
        raise HTTPException(status_code=404, detail="Course not found")
    return {
        "message": "Successfully found course",
        "course": result
    }


@router.get("/{course_id}")
async def get_course_with_id(course_id: int):
    """Retrieve a course by its numeric identifier.

    Args:
        course_id: Unique identifier of the course to retrieve.

    Returns:
        A response containing a confirmation message and the matching course.

    Raises:
        HTTPException: If no course has the requested ID.
    """
    result = get_course_by_id(course_id)
    if(result is None):
        raise HTTPException(status_code=404, detail="Course not found")
    return {
        "message": "Successfully found course",
        "course": result
    }

@router.put("/{course_id}")
async def update_course_by_id(course_id: int, course_update: CourseUpdate):
    result = update_course(course_id, course_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Course not found, duplicate code, or missing department")
    return {
        "message": "Course updated successfully",
        "course": result
    }

@router.delete("/code/{course_code}")
async def delete_course_by_code(course_code: str):
    """Delete a course by its course code.

    Args:
        course_code: Code of the course to delete.

    Returns:
        A confirmation message and the deletion result.

    Raises:
        HTTPException: If no course has the requested code.
    """
    deleted_course = delete_course_from_code(course_code)
    if(not deleted_course):
        raise HTTPException(status_code=404, detail="Course not found")
    return{
        "message": "Course deleted successfully",
        "deleted_course": deleted_course
    }


@router.delete("/{course_id}")
async def delete_course_by_id(course_id: int):
    """Delete a course by its numeric identifier.

    Args:
        course_id: Unique identifier of the course to delete.

    Returns:
        A confirmation message when the course is deleted.

    Raises:
        HTTPException: If no course has the requested ID.
    """
    deleted_course = delete_course_from_id(course_id)
    if(not deleted_course):
        raise HTTPException(status_code=404, detail="Course not found")
    return{
        "message": "Course deleted successfully"
    }

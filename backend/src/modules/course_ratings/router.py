from fastapi import APIRouter, HTTPException

from .schema import CourseRating, CourseRatingUpdate
from .service import create_course_rating, delete_course_rating, get_course_rating, get_course_ratings, update_course_rating


router = APIRouter(prefix="/course-ratings", tags=["course ratings"])


@router.post("/")
async def add_course_rating(course_rating: CourseRating):
    result = create_course_rating(course_rating)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate course rating or missing user/course")
    return {"message": "Course rating created successfully", "course_rating": result}


@router.get("/")
async def list_course_ratings():
    return {"message": "Retrieved all course ratings", "course_ratings": get_course_ratings()}


@router.get("/{course_rating_id}")
async def get_course_rating_by_id(course_rating_id: int):
    result = get_course_rating(course_rating_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course rating not found")
    return {"message": "Course rating found", "course_rating": result}


@router.put("/{course_rating_id}")
async def update_course_rating_by_id(course_rating_id: int, course_rating_update: CourseRatingUpdate):
    result = update_course_rating(course_rating_id, course_rating_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Course rating not found, duplicate pair, or missing user/course")
    return {"message": "Course rating updated successfully", "course_rating": result}


@router.delete("/{course_rating_id}")
async def delete_course_rating_by_id(course_rating_id: int):
    result = delete_course_rating(course_rating_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course rating not found")
    return {"message": "Course rating deleted successfully"}

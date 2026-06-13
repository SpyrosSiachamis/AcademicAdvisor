from fastapi import APIRouter
from .schema import Course
from .service import create_course

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post('/add')
def add_course(course: Course):
    created_course = create_course(course)
    return{
        "message": "Course Created",
        "created_course:": created_course
    }
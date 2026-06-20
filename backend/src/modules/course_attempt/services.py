from .schema import CourseAttempt
from ..users.services import users
from ..courses.service import courses
from typing import Any
def add_attempt(attempt: CourseAttempt) -> dict[str,Any] | None:
    attempt_data = attempt.model_dump()
    user_found = get_user(attempt_data["user_id"])
    course_found = get_course()

def get_user(user_id: int) -> bool | None:
    for user in users:
        if(user["id"] == user_id):
            return True
    return False
def get_department(department_id: int)
    
def get_course(course_id) -> int | None:
    for course in courses:
        if(course["id"] == course_id):
            return course_id
    return None
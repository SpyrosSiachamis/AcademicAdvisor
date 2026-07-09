from ..storage.memory import course_attempts, courses
from ..course_attempt.schema import Status
from ..graph.builder import build_department_prerequisite_adj_list
from typing import Any
def get_passed_courses(user_id: int) -> set[int]:
    passed_courses: set[int] = set()
    for attempt in course_attempts:
        if (attempt['user_id'] == user_id) and (attempt['status'] == Status.passed.value):
            passed_courses.add(attempt['course_id'])
    return passed_courses

def get_course_prerequisites(course_id: int) -> list[list[int]] | None:
    course_prerequisites: dict[int, list[list[int]]] = build_department_prerequisite_adj_list()
    if course_id not in course_prerequisites:
        return None
    return course_prerequisites[course_id]

def get_all_course_eligibilities(user_id: int) -> dict[int,bool]:
    from ..eligibility.router import get_course_eligibility
    eligibilities: dict[int, bool] = {}

    for course in courses:
        course_id: int = course['id']
        result = get_course_eligibility(user_id,course_id)
        eligibilities[course_id] = result["eligible"]
    return eligibilities
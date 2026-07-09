from ..storage.memory import course_attempts, courses
from ..course_attempt.schema import Status
from ..graph.builder import build_department_prerequisite_adj_list
from typing import TypedDict, NotRequired
from ..eligibility.service import evaluate_prerequisite_rule

class CourseEligibility(TypedDict):
    eligible: bool
    missing_groups: NotRequired[list[list[int]]]

def get_passed_courses(user_id: int) -> set[int]:
    passed_courses: set[int] = set()
    for attempt in course_attempts:
        if (attempt['user_id'] == user_id) and (attempt['status'] == Status.passed.value):
            passed_courses.add(attempt['course_id'])
    return passed_courses

def get_course_prerequisites(course_id: int) -> list[list[int]]:
    course_prerequisites: dict[int, list[list[int]]] = build_department_prerequisite_adj_list()
    if course_id not in course_prerequisites:
        raise ValueError(f"Course {course_id} not found")
    return course_prerequisites[course_id]

def get_all_course_eligibilities(user_id: int) -> dict[int,CourseEligibility]:
    eligibilities: dict[int, CourseEligibility] = {}
    passed_courses: set[int] = get_passed_courses(user_id)
    for course in courses:
        course_id: int = course['id']
        prerequisites: list[list[int]] = get_course_prerequisites(course_id)
        result = evaluate_prerequisite_rule(prerequisites,passed_courses)
        if "missing_groups" not in result:
            eligibilities[course_id] = {"eligible": result["eligible"]}
        else:
            eligibilities[course_id] = {
                "eligible": result["eligible"], 
                "missing_groups": result["missing_groups"]
            }
    return eligibilities
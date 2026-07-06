from ..storage.memory import course_attempts
from ..course_attempt.schema import Status
from ..graph.builder import build_department_prerequisite_adj_list
def get_passed_courses(user_id: int) -> set[int]:
    passed_courses: set[int] = set()
    for attempt in course_attempts:
        if (attempt['user_id'] == user_id) and (attempt['status'] == Status.passed.value):
            passed_courses.add(attempt['course_id'])
    return passed_courses

def get_course_prerequisites(course_id: int) -> list[int]:
    course_prerequisites: dict[int, list[int]] = build_department_prerequisite_adj_list()
    return course_prerequisites[course_id]

# def translate_prerequisites_to_and_or(prerequisites: list[int], format) -> list[list[int]]:
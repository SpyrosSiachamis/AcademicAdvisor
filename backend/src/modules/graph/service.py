from ..storage.memory import course_attempts
from ..course_attempt.schema import Status

def get_passed_courses(user_id: int) -> set[int]:
    passed_courses: set[int] = set()
    for attempt in course_attempts:
        if (attempt['user_id'] == user_id) and (attempt['status'] == Status.passed.value):
            passed_courses.add(attempt['course_id'])
    return passed_courses
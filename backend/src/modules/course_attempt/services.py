from .schema import CourseAttempt, CourseAttemptUpdate
from ..storage.memory import course_attempts, courses, users
from typing import Any

def add_attempt(attempt: CourseAttempt) -> dict[str,Any] | None:
    attempt_data = attempt.model_dump(mode="json")
    user_found = get_user(attempt_data["user_id"])
    course_found = get_course(attempt_data["course_id"])
    if(not user_found or not course_found):
        return None
    for existing_attempt in course_attempts:
        if(existing_attempt.get("id") == attempt_data.get("id")):
            return None
    course_attempts.append(attempt_data)
    return attempt_data

def get_attempts() -> list[dict[str, Any]]:
    return course_attempts

def get_attempt(attempt_id: int) -> dict[str, Any] | None:
    for attempt in course_attempts:
        if attempt.get("id") == attempt_id:
            return attempt
    return None 

def update_attempt(attempt_id: int, attempt_update: CourseAttemptUpdate) -> dict[str, Any] | None:
    update_data = attempt_update.model_dump(mode="json", exclude_unset=True)
    existing_attempt = get_attempt(attempt_id)
    if existing_attempt is None:
        return None
    
    # This updates updated pairs by unpacking the same keys second
    candidate_attempt = {**existing_attempt, **update_data}

    if not get_user(candidate_attempt["user_id"]) or not get_course(candidate_attempt["course_id"]):
        return None
    
    existing_attempt.update(update_data)
    return existing_attempt

def delete_attempt(attempt_id: int) -> bool:
    for attempt in course_attempts:
        if attempt.get("id") == attempt_id:
            course_attempts.remove(attempt)
            return True
    return False

def get_user(user_id: int) -> bool | None:
    for user in users:
        if(user["id"] == user_id):
            return True
    return False

def get_course(course_id: int) -> bool | None:
    for course in courses:
        if(course["id"] == course_id):
            return True
    return False

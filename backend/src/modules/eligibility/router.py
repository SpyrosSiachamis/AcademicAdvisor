from fastapi import APIRouter, HTTPException
from .service import evaluate_prerequisite_rule
from ..users.services import get_user
from ..course_attempt.schema import Status
from ..course_attempt.services import get_attempts
from ..course_prerequisites.service import get_course_prerequisites

router = APIRouter(prefix="/get-eligibility", tags=['eligibility', 'course-eligibility'])

@router.get("/{user_id}/{course_id}")
def get_course_eligibility(user_id: int, course_id: int):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID: {user_id} not found")

    course_preq_rules = [
        [prerequisite["prerequisite_course_id"]] for prerequisite in get_course_prerequisites() if prerequisite["course_id"] == course_id]

    passed_courses = { attempt["course_id"] for attempt in get_attempts() if attempt["user_id"] == user_id and attempt["status"] == Status.passed.value }

    return evaluate_prerequisite_rule(course_preq_rules, passed_courses)
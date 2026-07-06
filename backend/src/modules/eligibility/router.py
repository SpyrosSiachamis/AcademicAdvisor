from fastapi import APIRouter, HTTPException
from .service import evaluate_prerequisite_rule
from ..users.services import get_user
from ..graph.service import get_passed_courses
from ..graph.builder import build_department_prerequisite_adj_list
router = APIRouter(prefix="/get-eligibility", tags=['eligibility', 'course-eligibility'])

@router.get("/{user_id}/{course_id}")
def get_course_eligibility(user_id: int, course_id: int):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID: {user_id} not found")

    adj_list = build_department_prerequisite_adj_list()
    course_preq_rules = adj_list.get(course_id, [])
    passed_courses = get_passed_courses(user_id)
    return evaluate_prerequisite_rule(course_preq_rules, passed_courses)

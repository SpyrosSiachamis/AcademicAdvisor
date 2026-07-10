from fastapi import APIRouter, HTTPException
from .service import evaluate_prerequisite_rule
from ..users.services import get_user
from ..users.exceptions import UserNotFoundError
from ..graph.service import get_passed_courses
from ..graph.builder import build_department_prerequisite_adj_list
router = APIRouter(prefix="/get-eligibility", tags=['eligibility', 'course-eligibility'])

@router.get("/{user_id}/{course_id}")
def get_course_eligibility(user_id: int, course_id: int):
    try:
        get_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    adj_list = build_department_prerequisite_adj_list()
    course_preq_rules = adj_list.get(course_id, [])
    passed_courses = get_passed_courses(user_id)
    return evaluate_prerequisite_rule(course_preq_rules, passed_courses)

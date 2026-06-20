from typing import Any

from .schema import CourseCategoryAssignment, CourseCategoryAssignmentUpdate
from ..storage.memory import course_categories, course_category_assignments, courses


def create_course_category_assignment(assignment: CourseCategoryAssignment) -> dict[str, Any] | None:
    assignment_data = assignment.model_dump(mode="json")
    if not references_exist(assignment_data["course_id"], assignment_data["category_id"]):
        return None
    for existing_assignment in course_category_assignments:
        if existing_assignment.get("id") == assignment_data["id"] or same_pair(existing_assignment, assignment_data):
            return None
    course_category_assignments.append(assignment_data)
    return assignment_data


def get_course_category_assignments() -> list[dict[str, Any]]:
    return course_category_assignments


def get_course_category_assignment(assignment_id: int) -> dict[str, Any] | None:
    for assignment in course_category_assignments:
        if assignment.get("id") == assignment_id:
            return assignment
    return None


def update_course_category_assignment(assignment_id: int, assignment_update: CourseCategoryAssignmentUpdate) -> dict[str, Any] | None:
    update_data = assignment_update.model_dump(mode="json", exclude_unset=True)
    existing_assignment = get_course_category_assignment(assignment_id)
    if existing_assignment is None:
        return None
    candidate_assignment = {**existing_assignment, **update_data}
    if not references_exist(candidate_assignment["course_id"], candidate_assignment["category_id"]):
        return None
    for assignment in course_category_assignments:
        if assignment.get("id") != assignment_id and same_pair(assignment, candidate_assignment):
            return None
    existing_assignment.update(update_data)
    return existing_assignment


def delete_course_category_assignment(assignment_id: int) -> bool:
    for assignment in course_category_assignments:
        if assignment.get("id") == assignment_id:
            course_category_assignments.remove(assignment)
            return True
    return False


def references_exist(course_id: int, category_id: int) -> bool:
    return any(course.get("id") == course_id for course in courses) and any(category.get("id") == category_id for category in course_categories)


def same_pair(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left.get("course_id") == right.get("course_id") and left.get("category_id") == right.get("category_id")

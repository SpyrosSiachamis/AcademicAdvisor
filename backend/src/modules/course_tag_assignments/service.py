from typing import Any

from .schema import CourseTagAssignment, CourseTagAssignmentUpdate
from ..storage.memory import course_tag_assignments, courses, tags


def create_course_tag_assignment(assignment: CourseTagAssignment) -> dict[str, Any] | None:
    assignment_data = assignment.model_dump(mode="json")
    if not references_exist(assignment_data["course_id"], assignment_data["tag_id"]):
        return None
    for existing_assignment in course_tag_assignments:
        if existing_assignment.get("id") == assignment_data["id"] or same_pair(existing_assignment, assignment_data):
            return None
    course_tag_assignments.append(assignment_data)
    return assignment_data


def get_course_tag_assignments() -> list[dict[str, Any]]:
    return course_tag_assignments


def get_course_tag_assignment(assignment_id: int) -> dict[str, Any] | None:
    for assignment in course_tag_assignments:
        if assignment.get("id") == assignment_id:
            return assignment
    return None


def update_course_tag_assignment(assignment_id: int, assignment_update: CourseTagAssignmentUpdate) -> dict[str, Any] | None:
    update_data = assignment_update.model_dump(mode="json", exclude_unset=True)
    existing_assignment = get_course_tag_assignment(assignment_id)
    if existing_assignment is None:
        return None
    candidate_assignment = {**existing_assignment, **update_data}
    if not references_exist(candidate_assignment["course_id"], candidate_assignment["tag_id"]):
        return None
    for assignment in course_tag_assignments:
        if assignment.get("id") != assignment_id and same_pair(assignment, candidate_assignment):
            return None
    existing_assignment.update(update_data)
    return existing_assignment


def delete_course_tag_assignment(assignment_id: int) -> bool:
    for assignment in course_tag_assignments:
        if assignment.get("id") == assignment_id:
            course_tag_assignments.remove(assignment)
            return True
    return False


def references_exist(course_id: int, tag_id: int) -> bool:
    return any(course.get("id") == course_id for course in courses) and any(tag.get("id") == tag_id for tag in tags)


def same_pair(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left.get("course_id") == right.get("course_id") and left.get("tag_id") == right.get("tag_id")

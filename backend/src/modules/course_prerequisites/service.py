from typing import Any

from .schema import CoursePrerequisite, CoursePrerequisiteUpdate
from ..storage.memory import course_prerequisites, course_prerequisite_groups, courses


def create_course_prerequisite(prerequisite: CoursePrerequisite) -> dict[str, Any] | None:
    prerequisite_data = prerequisite.model_dump(mode="json")
    if not references_exist(prerequisite_data["group_id"], prerequisite_data["prerequisite_course_id"]):
        return None
    for existing_prerequisite in course_prerequisites:
        if existing_prerequisite.get("id") == prerequisite_data["id"] or same_pair(existing_prerequisite, prerequisite_data):
            return None
    course_prerequisites.append(prerequisite_data)
    return prerequisite_data


def get_course_prerequisites() -> list[dict[str, Any]]:
    return course_prerequisites


def get_course_prerequisite(prerequisite_id: int) -> dict[str, Any] | None:
    for prerequisite in course_prerequisites:
        if prerequisite.get("id") == prerequisite_id:
            return prerequisite
    return None


def update_course_prerequisite(prerequisite_id: int, prerequisite_update: CoursePrerequisiteUpdate) -> dict[str, Any] | None:
    update_data = prerequisite_update.model_dump(mode="json", exclude_unset=True)
    existing_prerequisite = get_course_prerequisite(prerequisite_id)
    if existing_prerequisite is None:
        return None
    candidate_prerequisite = {**existing_prerequisite, **update_data}
    if not references_exist(candidate_prerequisite["group_id"], candidate_prerequisite["prerequisite_course_id"]):
        return None
    for prerequisite in course_prerequisites:
        if prerequisite.get("id") != prerequisite_id and same_pair(prerequisite, candidate_prerequisite):
            return None
    existing_prerequisite.update(update_data)
    return existing_prerequisite


def delete_course_prerequisite(prerequisite_id: int) -> bool:
    for prerequisite in course_prerequisites:
        if prerequisite.get("id") == prerequisite_id:
            course_prerequisites.remove(prerequisite)
            return True
    return False


def references_exist(group_id: int, prerequisite_course_id: int) -> bool:
    return (
        any(group.get("id") == group_id for group in course_prerequisite_groups)
        and any(course.get("id") == prerequisite_course_id for course in courses)
    )


def same_pair(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left.get("group_id") == right.get("group_id") and left.get("prerequisite_course_id") == right.get("prerequisite_course_id")

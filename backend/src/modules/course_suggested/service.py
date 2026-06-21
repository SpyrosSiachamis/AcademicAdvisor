from typing import Any

from .schema import CourseSuggested, CourseSuggestedUpdate
from ..storage.memory import course_suggested, courses


def create_course_suggested(suggested: CourseSuggested) -> dict[str, Any] | None:
    suggested_data = suggested.model_dump(mode="json")
    if not references_exist(suggested_data["course_id"], suggested_data["suggested_course_id"]):
        return None
    for existing_suggested in course_suggested:
        if existing_suggested.get("id") == suggested_data["id"] or same_pair(existing_suggested, suggested_data):
            return None
    course_suggested.append(suggested_data)
    return suggested_data


def get_course_suggested() -> list[dict[str, Any]]:
    return course_suggested


def get_course_suggested_by_id(suggested_id: int) -> dict[str, Any] | None:
    for suggested in course_suggested:
        if suggested.get("id") == suggested_id:
            return suggested
    return None


def update_course_suggested(suggested_id: int, suggested_update: CourseSuggestedUpdate) -> dict[str, Any] | None:
    update_data = suggested_update.model_dump(mode="json", exclude_unset=True)
    existing_suggested = get_course_suggested_by_id(suggested_id)
    if existing_suggested is None:
        return None
    candidate_suggested = {**existing_suggested, **update_data}
    if not references_exist(candidate_suggested["course_id"], candidate_suggested["suggested_course_id"]):
        return None
    for suggested in course_suggested:
        if suggested.get("id") != suggested_id and same_pair(suggested, candidate_suggested):
            return None
    existing_suggested.update(update_data)
    return existing_suggested


def delete_course_suggested(suggested_id: int) -> bool:
    for suggested in course_suggested:
        if suggested.get("id") == suggested_id:
            course_suggested.remove(suggested)
            return True
    return False


def references_exist(course_id: int, suggested_course_id: int) -> bool:
    return any(course.get("id") == course_id for course in courses) and any(course.get("id") == suggested_course_id for course in courses)


def same_pair(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left.get("course_id") == right.get("course_id") and left.get("suggested_course_id") == right.get("suggested_course_id")

from typing import Any

from .schema import CoursePrerequisiteGroup, CoursePrerequisiteGroupUpdate
from ..storage.memory import course_prerequisite_groups, courses


def create_course_prerequisite_group(group: CoursePrerequisiteGroup) -> dict[str, Any] | None:
    group_data = group.model_dump(mode="json")
    if not any(course.get("id") == group_data["course_id"] for course in courses):
        return None
    for existing_group in course_prerequisite_groups:
        if existing_group.get("id") == group_data["id"]:
            return None
    course_prerequisite_groups.append(group_data)
    return group_data


def get_course_prerequisite_groups() -> list[dict[str, Any]]:
    return course_prerequisite_groups


def get_course_prerequisite_group(group_id: int) -> dict[str, Any] | None:
    for group in course_prerequisite_groups:
        if group.get("id") == group_id:
            return group
    return None


def update_course_prerequisite_group(group_id: int, group_update: CoursePrerequisiteGroupUpdate) -> dict[str, Any] | None:
    update_data = group_update.model_dump(mode="json", exclude_unset=True)
    existing_group = get_course_prerequisite_group(group_id)
    if existing_group is None:
        return None
    candidate_group = {**existing_group, **update_data}
    if not any(course.get("id") == candidate_group["course_id"] for course in courses):
        return None
    existing_group.update(update_data)
    return existing_group


def delete_course_prerequisite_group(group_id: int) -> bool:
    for group in course_prerequisite_groups:
        if group.get("id") == group_id:
            course_prerequisite_groups.remove(group)
            return True
    return False

"""In-memory course storage and lookup operations."""

from .schema import Course, CourseUpdate
from typing import Any
from ..storage.memory import courses, departments


def create_course(course: Course) -> dict[str,Any] | None:
    """Store a course unless its ID is already in use.

    Args:
        course: Validated course model to store.
`
    Returns:
        The serialized course data when creation succeeds, or ``None`` when a
        course with the same ID already exists.
    """
    course_data = course.model_dump(mode="json")
    if not department_exists(course_data["department_id"]):
        return None
    for c in courses:
        if c.get("id") == course_data.get("id") or c.get("code") == course_data.get("code"):
            return None
    courses.append(course_data)
    return course_data


def get_all_courses() -> list[dict[str,Any]]:
    """Return all stored courses.

    Returns:
        The in-memory list of serialized course records.
    """
    return courses

def get_course_by_id(id: int) -> dict[str,Any] | None:
    """Find a stored course by its numeric identifier.

    Args:
        id: Unique identifier of the course to find.

    Returns:
        The matching course record, or ``None`` when no match is found.
    """
    for c in courses:
        if(c.get("id") == id):
            return c
    return None

def get_course_by_code(code: str) -> dict[str,Any] | None:
    """Find a stored course by its course code.

    Args:
        code: Course code to search for.

    Returns:
        The matching course record, or ``None`` when no match is found.
    """
    for c in courses:
        if(c.get("code") == code):
            return c
    return None

def update_course(course_id: int, course_update: CourseUpdate) -> dict[str, Any] | None:
    update_data = course_update.model_dump(mode="json", exclude_unset=True)
    existing_course = get_course_by_id(course_id)
    if existing_course is None:
        return None
    if "department_id" in update_data and not department_exists(update_data["department_id"]):
        return None
    if "code" in update_data:
        for course in courses:
            if course.get("id") != course_id and course.get("code") == update_data["code"]:
                return None
    existing_course.update(update_data)
    return existing_course

def delete_course_from_id(course_id: int) -> bool:
    """Delete a stored course by its numeric identifier.

    Args:
        course_id: Unique identifier of the course to delete.

    Returns:
        ``True`` when a course is deleted, otherwise ``False``.
    """
    for c in courses:
        if(c.get("id") == course_id):
            courses.remove(c)
            return True
    return False

def delete_course_from_code(course_code: str) -> bool:
    """Delete a stored course by its course code.

    Args:
        course_code: Code of the course to delete.

    Returns:
        ``True`` when a course is deleted, otherwise ``False``.
    """
    for c in courses:
        if(c.get("code") == course_code):
            courses.remove(c)
            return True
    return False

def department_exists(department_id: int) -> bool:
    for department in departments:
        if department.get("id") == department_id:
            return True
    return False

"""In-memory course storage and lookup operations."""

from .schema import Course
from typing import Any
from ..storage.memory import courses


def create_course(course: Course) -> dict[str,Any] | None:
    """Store a course unless its ID is already in use.

    Args:
        course: Validated course model to store.
`
    Returns:
        The serialized course data when creation succeeds, or ``None`` when a
        course with the same ID already exists.
    """
    course_data = course.model_dump()
    for c in courses:
        if(c.get("id") == course_data.get("id")):
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
from typing import Any

from .schema import DepartmentCourse, DepartmentCourseUpdate
from ..storage.memory import courses, department_courses, departments


def create_department_course(department_course: DepartmentCourse) -> dict[str, Any] | None:
    department_course_data = department_course.model_dump(mode="json")
    if not references_exist(department_course_data["department_id"], department_course_data["course_id"]):
        return None
    for existing_department_course in department_courses:
        if existing_department_course.get("id") == department_course_data["id"] or same_pair(existing_department_course, department_course_data):
            return None
    department_courses.append(department_course_data)
    return department_course_data


def get_department_courses() -> list[dict[str, Any]]:
    return department_courses


def get_department_course(department_course_id: int) -> dict[str, Any] | None:
    for department_course in department_courses:
        if department_course.get("id") == department_course_id:
            return department_course
    return None


def update_department_course(department_course_id: int, department_course_update: DepartmentCourseUpdate) -> dict[str, Any] | None:
    update_data = department_course_update.model_dump(mode="json", exclude_unset=True)
    existing_department_course = get_department_course(department_course_id)
    if existing_department_course is None:
        return None
    candidate_department_course = {**existing_department_course, **update_data}
    if not references_exist(candidate_department_course["department_id"], candidate_department_course["course_id"]):
        return None
    for department_course in department_courses:
        if department_course.get("id") != department_course_id and same_pair(department_course, candidate_department_course):
            return None
    existing_department_course.update(update_data)
    return existing_department_course


def delete_department_course(department_course_id: int) -> bool:
    for department_course in department_courses:
        if department_course.get("id") == department_course_id:
            department_courses.remove(department_course)
            return True
    return False


def references_exist(department_id: int, course_id: int) -> bool:
    return any(department.get("id") == department_id for department in departments) and any(course.get("id") == course_id for course in courses)


def same_pair(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left.get("department_id") == right.get("department_id") and left.get("course_id") == right.get("course_id")

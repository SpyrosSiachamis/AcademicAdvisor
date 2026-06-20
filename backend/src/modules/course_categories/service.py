from typing import Any

from .schema import CourseCategory, CourseCategoryUpdate
from ..storage.memory import course_categories


def create_course_category(category: CourseCategory) -> dict[str, Any] | None:
    category_data = category.model_dump(mode="json")
    for existing_category in course_categories:
        if (
            existing_category.get("id") == category_data["id"]
            or existing_category.get("code") == category_data["code"]
            or existing_category.get("name") == category_data["name"]
        ):
            return None
    course_categories.append(category_data)
    return category_data


def get_course_categories() -> list[dict[str, Any]]:
    return course_categories


def get_course_category(category_id: int) -> dict[str, Any] | None:
    for category in course_categories:
        if category.get("id") == category_id:
            return category
    return None


def update_course_category(category_id: int, category_update: CourseCategoryUpdate) -> dict[str, Any] | None:
    update_data = category_update.model_dump(mode="json", exclude_unset=True)
    existing_category = get_course_category(category_id)
    if existing_category is None:
        return None
    for category in course_categories:
        if category.get("id") == category_id:
            continue
        if "code" in update_data and category.get("code") == update_data["code"]:
            return None
        if "name" in update_data and category.get("name") == update_data["name"]:
            return None
    existing_category.update(update_data)
    return existing_category


def delete_course_category(category_id: int) -> bool:
    for category in course_categories:
        if category.get("id") == category_id:
            course_categories.remove(category)
            return True
    return False

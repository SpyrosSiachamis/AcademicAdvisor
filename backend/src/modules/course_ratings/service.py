from typing import Any

from .schema import CourseRating, CourseRatingUpdate
from ..storage.memory import course_ratings, courses, users


def create_course_rating(course_rating: CourseRating) -> dict[str, Any] | None:
    course_rating_data = course_rating.model_dump(mode="json")
    if not references_exist(course_rating_data["course_id"], course_rating_data["user_id"]):
        return None
    for existing_course_rating in course_ratings:
        if existing_course_rating.get("id") == course_rating_data["id"] or same_pair(existing_course_rating, course_rating_data):
            return None
    course_ratings.append(course_rating_data)
    return course_rating_data


def get_course_ratings() -> list[dict[str, Any]]:
    return course_ratings


def get_course_rating(course_rating_id: int) -> dict[str, Any] | None:
    for course_rating in course_ratings:
        if course_rating.get("id") == course_rating_id:
            return course_rating
    return None


def update_course_rating(course_rating_id: int, course_rating_update: CourseRatingUpdate) -> dict[str, Any] | None:
    update_data = course_rating_update.model_dump(mode="json", exclude_unset=True)
    existing_course_rating = get_course_rating(course_rating_id)
    if existing_course_rating is None:
        return None
    candidate_course_rating = {**existing_course_rating, **update_data}
    if not references_exist(candidate_course_rating["course_id"], candidate_course_rating["user_id"]):
        return None
    for course_rating in course_ratings:
        if course_rating.get("id") != course_rating_id and same_pair(course_rating, candidate_course_rating):
            return None
    existing_course_rating.update(update_data)
    return existing_course_rating


def delete_course_rating(course_rating_id: int) -> bool:
    for course_rating in course_ratings:
        if course_rating.get("id") == course_rating_id:
            course_ratings.remove(course_rating)
            return True
    return False


def references_exist(course_id: int, user_id: int) -> bool:
    return any(course.get("id") == course_id for course in courses) and any(user.get("id") == user_id for user in users)


def same_pair(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left.get("course_id") == right.get("course_id") and left.get("user_id") == right.get("user_id")

from typing import Any

# Temporary in-memory storage.
# Will be replaced by PostgreSQL repositories.
users: list[dict[str, Any]] = []
courses: list[dict[str, Any]] = []
departments: list[dict[str, Any]] = []
universities: list[dict[str, Any]] = []
course_attempts: list[dict[str, Any]] = []
course_ratings: list[dict[str, Any]] = []
tags: list[dict[str, Any]] = []
course_tag_assignments: list[dict[str, Any]] = []
course_categories: list[dict[str, Any]] = []
course_category_assignments: list[dict[str, Any]] = []
department_courses: list[dict[str, Any]] = []
course_prerequisites: list[dict[str, Any]] = []
course_suggested: list[dict[str, Any]] = []
from typing import Any

# Temporary in-memory storage.
# Will be replaced by PostgreSQL repositories.
users: list[dict[str, Any]] = []
courses: list[dict[str,Any]] = []
departments: list[dict[str,Any]] = []
universities: list[dict[str, Any]] = []
course_attempts: list[dict[str,Any]] = []
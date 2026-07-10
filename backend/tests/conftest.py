from fastapi.testclient import TestClient
import pytest as pt
from src.app import app
from src.modules.storage import memory
from src.modules.course_attempt.schema import Status

client = TestClient(app)

DEPARTMENT_COURSE_PREREQUISITES: dict[int, list[tuple[int, ...]]] = {
    4: [(3,)],                    # CS-109 requires CS-108
    10: [(4,)],                   # CS-208 requires CS-109
    11: [(10,)],                  # CS-209 requires CS-208
    12: [(2,)],                   # CS-215 requires CS-110
    13: [(2,)],                   # CS-217 requires CS-110
    14: [(7,)],                   # CS-225 requires CS-120
    15: [(1, 8)],                 # CS-240 requires CS-100 OR CS-150
    16: [(1, 8)],                 # CS-252 requires CS-100 OR CS-150
    17: [(1, 8)],                 # CS-255 requires CS-100 OR CS-150
    19: [(5, 13)],                # CS-335 requires CS-118 OR CS-217
    20: [(18, 15, 17)],           # CS-340 requires CS-280 OR CS-240 OR CS-255
    21: [(15, 17)],               # CS-345 requires CS-240 OR CS-255
    22: [(15, 17), (5, 9)],       # CS-360 requires {CS-240 OR CS-255} AND {CS-118 OR CS-180}
    23: [(5, 18), (15,)],         # CS-380 requires {CS-118 OR CS-280} AND CS-240
}


def clear_memory():
    memory.users.clear()
    memory.courses.clear()
    memory.departments.clear()
    memory.universities.clear()
    memory.course_attempts.clear()
    memory.course_prerequisite_groups.clear()
    memory.course_prerequisites.clear()
    memory.course_suggested.clear()


def seed_university():
    memory.universities.append({"id": 1, "name": "University of Crete", "website_url": None})


def seed_department():
    seed_university()
    memory.departments.append({"id": 1, "name": "Computer Science", "university_id": 1})


def seed_course():
    seed_department()
    memory.courses.append({
        "id": 1,
        "department_id": 1,
        "code": "CS-225",
        "name": "Computer Organization",
        "ects": 8
    })


def seed_two_courses():
    seed_course()
    memory.courses.append({
        "id": 2,
        "department_id": 1,
        "code": "CS-240",
        "name": "Data Structures",
        "ects": 6
    })


def seed_user():
    seed_department()
    memory.users.append({
        "id": 1,
        "username": "spiros",
        "email": "spiros@example.com",
        "password_hash": "fakehash",
        "department_id": 1
    })


def seed_courses():
    seed_department()
    courses = [
        {
            "id": 1,
            "department_id": 1,
            "code": "CS-100",
            "name": "Introduction to Computer Science",
            "ects": 8
        },
        {
            "id": 2,
            "department_id": 1,
            "code": "CS-110",
            "name": "Calculus I",
            "ects": 8
        },
        {
            "id": 3,
            "department_id": 1,
            "code": "CS-108",
            "name": "English I",
            "ects": 4
        },
        {
            "id": 4,
            "department_id": 1,
            "code": "CS-109",
            "name": "English II",
            "ects": 4
        },
        {
            "id": 5,
            "department_id": 1,
            "code": "CS-118",
            "name": "Discrete Mathematics",
            "ects": 6
        },
        {
            "id": 6,
            "department_id": 1,
            "code": "CS-119",
            "name": "Linear Algebra",
            "ects": 6
        },
        {
            "id": 7,
            "department_id": 1,
            "code": "CS-120",
            "name": "Digital Design",
            "ects": 8
        },
        {
            "id": 8,
            "department_id": 1,
            "code": "CS-150",
            "name": "Programming",
            "ects": 8
        },
        {
            "id": 9,
            "department_id": 1,
            "code": "CS-180",
            "name": "Logic",
            "ects": 6
        },
        {
            "id": 10,
            "department_id": 1,
            "code": "CS-208",
            "name": "English III",
            "ects": 4
        },
        {
            "id": 11,
            "department_id": 1,
            "code": "CS-209",
            "name": "English IV",
            "ects": 4
        },
        {
            "id": 12,
            "department_id": 1,
            "code": "CS-215",
            "name": "Applied Mathematics for Engineers",
            "ects": 8
        },
        {
            "id": 13,
            "department_id": 1,
            "code": "CS-217",
            "name": "Probability",
            "ects": 6
        },
        {
            "id": 14,
            "department_id": 1,
            "code": "CS-225",
            "name": "Computer Organization",
            "ects": 8
        },
        {
            "id": 15,
            "department_id": 1,
            "code": "CS-240",
            "name": "Data Structures",
            "ects": 8
        },
        {
            "id": 16,
            "department_id": 1,
            "code": "CS-252",
            "name": "Object-Oriented Programming",
            "ects": 8
        },
        {
            "id": 17,
            "department_id": 1,
            "code": "CS-255",
            "name": "Software Technology Laboratory",
            "ects": 6
        },
        {
            "id": 18,
            "department_id": 1,
            "code": "CS-280",
            "name": "Theory of Computation",
            "ects": 6
        },
        {
            "id": 19,
            "department_id": 1,
            "code": "CS-335",
            "name": "Computer Networks",
            "ects": 6
        },
        {
            "id": 20,
            "department_id": 1,
            "code": "CS-340",
            "name": "Languages and Compilers",
            "ects": 8
        },
        {
            "id": 21,
            "department_id": 1,
            "code": "CS-345",
            "name": "Operating Systems",
            "ects": 8
        },
        {
            "id": 22,
            "department_id": 1,
            "code": "CS-360",
            "name": "Files and Databases",
            "ects": 8
        },
        {
            "id": 23,
            "department_id": 1,
            "code": "CS-380",
            "name": "Algorithms and Complexity",
            "ects": 8
        },
    ]

    existing_codes = {course["code"] for course in memory.courses}
    for course in courses:
        if course["code"] not in existing_codes:
            memory.courses.append(course)

def seed_department_course_prerequisites():
    existing_group_ids = {group["id"] for group in memory.course_prerequisite_groups}
    next_group_id = max(existing_group_ids, default=0) + 1
    next_prereq_id = max(
        (prereq["id"] for prereq in memory.course_prerequisites),
        default=0,
    ) + 1

    for course_id, or_groups in DEPARTMENT_COURSE_PREREQUISITES.items():
        for or_group in or_groups:
            already_exists = any(
                group["course_id"] == course_id
                and set(or_group) == {
                    prereq["prerequisite_course_id"]
                    for prereq in memory.course_prerequisites
                    if prereq["group_id"] == group["id"]
                }
                for group in memory.course_prerequisite_groups
            )
            if already_exists:
                continue

            group = {"id": next_group_id, "course_id": course_id}
            memory.course_prerequisite_groups.append(group)

            for prereq_course_id in or_group:
                prereq = {
                    "id": next_prereq_id,
                    "prerequisite_course_id": prereq_course_id,
                    "group_id": next_group_id,
                }
                memory.course_prerequisites.append(prereq)
                next_prereq_id += 1

            next_group_id += 1

USER_COURSE_ATTEMPTS = {
    "english_1_only": [
        {
            "id": 1,
            "course_id": 3,
            "user_id": 1,
            "status": Status.passed.value,
            "grade": 8.0,
            "course_period": 0,
            "semester": 1,
            "academic_year": 2026,
            "attempt_number": 1
        },
    ],
    "no_passed_courses": [],
    "cs240_prerequisites": [
        {
            "id": 1,
            "course_id": 1,
            "user_id": 1,
            "status": Status.passed.value,
            "grade": 8.0,
            "course_period": 0,
            "semester": 1,
            "academic_year": 2026,
            "attempt_number": 1
        },
        {
            "id": 2,
            "course_id": 8,
            "user_id": 1,
            "status": Status.passed.value,
            "grade": 8.0,
            "course_period": 0,
            "semester": 1,
            "academic_year": 2026,
            "attempt_number": 1
        },
    ],
    "cs110_passed": [
        {
            "id": 1,
            "course_id": 2,
            "user_id": 1,
            "status": Status.passed.value,
            "grade": 8.0,
            "course_period": 0,
            "semester": 1,
            "academic_year": 2026,
            "attempt_number": 1
        },
    ],
    "all_courses": [
        {
            "id": course_id,
            "course_id": course_id,
            "user_id": 1,
            "status": Status.passed.value,
            "grade": 8.0,
            "course_period": 0,
            "semester": 1,
            "academic_year": 2026,
            "attempt_number": 1
        }
        for course_id in range(1, 24)
    ]
}

def seed_course_prerequisites():
    seed_courses()
    seed_department_course_prerequisites()

def seed_user_passed_courses():
    seed_course_prerequisites()
    seed_user()


def seed_user_course_attempts(attempts_key: str):
    seed_course_prerequisites()
    seed_user()

    for attempt in USER_COURSE_ATTEMPTS[attempts_key]:
        memory.course_attempts.append(attempt.copy())

@pt.fixture
def auth_headers():
    memory.departments.append({"id": 999, "name": "Auth Test Department", "university_id": 999})
    client.post("/users/", json={
        "id": 999, "username": "testadmin", "email": "test@admin.com",
        "password": "testpass123", "department_id": 999
    })
    response = client.post("/auth/token", data={
        "username": "testadmin", "password": "testpass123", "grant_type": "password"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
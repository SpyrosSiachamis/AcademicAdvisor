from fastapi.testclient import TestClient

from src.app import app
from src.modules.storage import memory
from src.modules.course_attempt.schema import Status

client = TestClient(app)

DEPARTMENT_COURSE_PREREQUISITES: dict[str, tuple[str, ...]] = {
    "CS-109": ("CS-108",),
    "CS-208": ("CS-109",),
    "CS-209": ("CS-208",),
    "CS-215": ("CS-110",),
    "CS-217": ("CS-110",),
    "CS-225": ("CS-120",),
    "CS-240": ("CS-100", "CS-150"),
    "CS-252": ("CS-100", "CS-150"),
    "CS-255": ("CS-150", "CS-100"),
    "CS-335": ("CS-118", "CS-217"),
    "CS-340": ("CS-280", "CS-240", "CS-255"),
    "CS-345": ("CS-240", "CS-255"),
    "CS-360": ("CS-240", "CS-255", "CS-118", "CS-180"),
    "CS-380": ("CS-118", "CS-280", "CS-240"),
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
    courses_by_code = {course["code"]: course for course in memory.courses}

    existing_group_ids = {group["id"] for group in memory.course_prerequisite_groups}
    existing_prereq_ids = {prereq["id"] for prereq in memory.course_prerequisites}

    next_group_id = max(existing_group_ids, default=0) + 1
    next_prereq_id = max(existing_prereq_ids, default=0) + 1

    for course_code, prerequisite_codes in DEPARTMENT_COURSE_PREREQUISITES.items():
        course = courses_by_code.get(course_code)
        if course is None:
            continue

        for prerequisite_code in prerequisite_codes:
            prerequisite_course = courses_by_code.get(prerequisite_code)
            if prerequisite_course is None:
                continue

            already_exists = any(
                group["course_id"] == course["id"]
                and any(
                    prereq["group_id"] == group["id"]
                    and prereq["prerequisite_course_id"] == prerequisite_course["id"]
                    for prereq in memory.course_prerequisites
                )
                for group in memory.course_prerequisite_groups
            )
            if already_exists:
                continue

            group = {"id": next_group_id, "course_id": course["id"]}
            memory.course_prerequisite_groups.append(group)

            prereq = {
                "id": next_prereq_id,
                "prerequisite_course_id": prerequisite_course["id"],
                "group_id": next_group_id,
            }
            memory.course_prerequisites.append(prereq)

            next_group_id += 1
            next_prereq_id += 1

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

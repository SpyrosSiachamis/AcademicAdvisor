from fastapi.testclient import TestClient
from src.app import app
from src.modules.storage import memory

client = TestClient(app)

# Adj_lists for the prerequisite graph
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


def seed_department_course_prerequisites():
    courses_by_code = {course["code"]: course for course in memory.courses}

    existing_pairs = {
        (prerequisite["course_id"], prerequisite["prerequisite_course_id"])
        for prerequisite in memory.course_prerequisites
    }

    next_id = max(
        (prerequisite["id"] for prerequisite in memory.course_prerequisites),
        default=0,
    ) + 1

    for course_code, prerequisite_codes in DEPARTMENT_COURSE_PREREQUISITES.items():
        course = courses_by_code.get(course_code)
        if course is None:
            continue

        for prerequisite_code in prerequisite_codes:
            prerequisite_course = courses_by_code.get(prerequisite_code)
            if prerequisite_course is None:
                continue

            pair = (course["id"], prerequisite_course["id"])
            if pair in existing_pairs:
                continue

            prerequisite = {
                "id": next_id,
                "course_id": course["id"],
                "prerequisite_course_id": prerequisite_course["id"],
            }
            memory.course_prerequisites.append(prerequisite)
            existing_pairs.add(pair)
            next_id += 1

def setup_function():
    memory.users.clear()
    memory.courses.clear()
    memory.departments.clear()
    memory.universities.clear()
    memory.course_attempts.clear()
    memory.course_prerequisites.clear()
    memory.course_suggested.clear()

def seed_university():
    memory.universities.append({"id": 1, "name": "University of Crete", "website_url": None})


def seed_department():
    seed_university()
    memory.departments.append({"id": 1, "name": "Computer Science", "university_id": 1})


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

def seed_course_prerequisites():
    seed_courses()
    seed_department_course_prerequisites()

def test_seeded_courses():
    seed_courses()
    response = client.get("/courses")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert data["message"] == "Retrieved all courses"
    assert "courses" in data

    courses = data["courses"]
    assert isinstance(courses, list)
    assert len(courses) == 23
    course_codes = {course["code"] for course in courses}
    assert "CS-100" in course_codes
    assert "CS-110" in course_codes
    assert "CS-225" in course_codes
    course_ids = {course["id"] for course in courses}
    assert len(course_ids) == 23
    assert min(course_ids) == 1
    assert max(course_ids) == 23

def test_english_ii_has_english_i_as_prerequisite():
    seed_course_prerequisites()
    response = client.get("/courses")
    assert response.status_code == 200
    courses = response.json()["courses"]

    response = client.get("/course-prerequisites/")
    assert response.status_code == 200
    prerequisites = response.json()["prerequisites"]
    assert len(prerequisites) == 26

    english_2_prerequisite = next(
        prerequisite for prerequisite in prerequisites
        if prerequisite["course_id"] == 4
    )
    preq_id = english_2_prerequisite["prerequisite_course_id"]
    course_id = english_2_prerequisite["course_id"]
    course_ids = {course["id"] for course in courses}
    english_1 = english_2 = None
    for course in courses:
        if(course["id"] == preq_id):
            english_1 = course
        elif(course["id"] == course_id):
            english_2 = course
    assert (course_id in course_ids) and (preq_id in course_ids)
    assert english_1 is not None
    assert english_2 is not None
    assert english_1["name"] == "English I"
    assert english_2["name"] == "English II"

def test_seed_course_prerequisites_is_idempotent():
    seed_course_prerequisites()
    seed_course_prerequisites()
    assert len(memory.course_prerequisites) == 26
    pairs = {
        (prerequisite["course_id"], prerequisite["prerequisite_course_id"])
        for prerequisite in memory.course_prerequisites
    }
    assert len(pairs) == 26
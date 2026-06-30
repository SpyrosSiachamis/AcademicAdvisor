from src.modules.storage import memory

from .conftest import clear_memory, client, seed_department, seed_two_courses, seed_courses

def setup_function():
    clear_memory()


def test_department_missing_university_rejected():
    response = client.post("/department/add", json={
        "id": 1,
        "name": "Computer Science",
        "university_id": 999
    })

    assert response.status_code in (404, 409)


def test_department_duplicate_id_rejected():
    seed_department()

    response = client.post("/department/add", json={
        "id": 1,
        "name": "Physics",
        "university_id": 1
    })

    assert response.status_code == 409


def test_department_same_name_same_university_rejected():
    seed_department()

    response = client.post("/department/add", json={
        "id": 2,
        "name": "Computer Science",
        "university_id": 1
    })

    assert response.status_code == 409


def test_course_get_missing_returns_404():
    response = client.get("/courses/999")

    assert response.status_code == 404


def test_course_delete_missing_returns_404():
    response = client.delete("/courses/999")

    assert response.status_code == 404


def test_course_attempt_missing_user_or_course_rejected():
    response = client.post("/attempt/add", json={
        "id": 1,
        "course_id": 999,
        "user_id": 999,
        "status": 2,
        "grade": 8.5,
        "course_period": 0,
        "semester": 5,
        "academic_year": 2026,
        "attempt_number": 1
    })

    assert response.status_code in (404, 409)


def test_course_prerequisite_created_with_existing_courses():
    seed_two_courses()

    response = client.post("/course-prerequisites/", json={
        "id": 1,
        "course_id": 2,
        "prerequisite_course_id": 1
    })

    assert response.status_code == 200
    assert response.json()["prerequisite"]["course_id"] == 2


def test_course_prerequisite_duplicate_pair_rejected():
    seed_two_courses()
    memory.course_prerequisites.append({
        "id": 1,
        "course_id": 2,
        "prerequisite_course_id": 1
    })

    response = client.post("/course-prerequisites/", json={
        "id": 2,
        "course_id": 2,
        "prerequisite_course_id": 1
    })

    assert response.status_code == 409


def test_course_prerequisite_missing_course_rejected():
    response = client.post("/course-prerequisites/", json={
        "id": 1,
        "course_id": 2,
        "prerequisite_course_id": 1
    })

    assert response.status_code == 409


def test_course_suggested_created_with_existing_courses():
    seed_two_courses()

    response = client.post("/course-suggested/", json={
        "id": 1,
        "course_id": 1,
        "suggested_course_id": 2
    })

    assert response.status_code == 200
    assert response.json()["suggested"]["suggested_course_id"] == 2


def test_course_suggested_duplicate_pair_rejected():
    seed_two_courses()
    memory.course_suggested.append({
        "id": 1,
        "course_id": 1,
        "suggested_course_id": 2
    })

    response = client.post("/course-suggested/", json={
        "id": 2,
        "course_id": 1,
        "suggested_course_id": 2
    })

    assert response.status_code == 409


def test_course_suggested_missing_course_rejected():
    response = client.post("/course-suggested/", json={
        "id": 1,
        "course_id": 1,
        "suggested_course_id": 2
    })

    assert response.status_code == 409

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

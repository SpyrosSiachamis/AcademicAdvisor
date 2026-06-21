from fastapi.testclient import TestClient

from src.app import app
from src.modules.storage import memory


client = TestClient(app)


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

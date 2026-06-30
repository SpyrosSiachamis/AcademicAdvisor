from src.modules.storage import memory

from .conftest import clear_memory, client, seed_course_prerequisites, seed_courses


def setup_function():
    clear_memory()

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

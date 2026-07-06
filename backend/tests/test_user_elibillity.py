from src.modules.storage import memory

from .conftest import clear_memory, client, seed_course_prerequisites, seed_user_course_attempts
from src.modules.eligibility.service import evaluate_prerequisite_rule
from src.modules.eligibility.router import get_course_eligibility
from src.modules.graph.builder import build_department_prerequisite_adj_list
from src.modules.graph.service import get_passed_courses,get_course_prerequisites
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

def test_user_course_attempts():
    seed_user_course_attempts("no_passed_courses")
    assert len(memory.course_attempts) == 0
    seed_user_course_attempts("cs240_prerequisites")
    assert len(memory.course_attempts) == 2
    


def test_prerequisite_eligibility_no_rules():
    result = evaluate_prerequisite_rule([], {3,2})
    assert(result["eligible"])


def test_prerequisite_eligibility_englishII():
    result = evaluate_prerequisite_rule([[1]], {3,2,1})
    assert(result["eligible"])

def test_prerequisite_no_eligibility_englishII():
    result = evaluate_prerequisite_rule([[1]], {3,2})
    assert(not result["eligible"])

def test_prerequisite_cs100_or_cs150_rule_not_eligible():
    result = evaluate_prerequisite_rule([[1,8]], {3,2})
    assert not result["eligible"]

def test_prerequisite_cs100_or_cs150_rule_eligible():
    result = evaluate_prerequisite_rule([[1,8]], {3,8})
    assert(result["eligible"])

def test_prerequisite_cs100_and_cs150_rule_eligible():
    result = evaluate_prerequisite_rule([[1],[8]], {1,3,8})
    assert(result["eligible"])

def test_prerequisite_cs100_and_cs150_rule_not_eligible():
    result = evaluate_prerequisite_rule([[1],[8]], {8,2})
    assert(not result["eligible"])

def test_prerequisite_cs100_and_cs150_rule_not_eligible_no_passed_courses():
    result = evaluate_prerequisite_rule([[1],[8]], set())
    assert(not result["eligible"])

def test_prerequisite_empty_or_group():
    result = evaluate_prerequisite_rule([[]], set())
    assert(not result["eligible"])

def test_prerequisite_empty_and_groups():
    result = evaluate_prerequisite_rule([[],[]], set())
    assert(not result["eligible"])

def test_user_eligibility_cs240_true():
    seed_user_course_attempts("cs240_prerequisites")
    result = get_course_eligibility(1,15)
    assert result["eligible"]


def test_user_eligibility_cs240_false():
    seed_user_course_attempts("cs110_passed")
    result = get_course_eligibility(1,15)
    assert not result["eligible"]

def test_user_eligibility_cs215_true():
    seed_user_course_attempts("cs110_passed")
    result = get_course_eligibility(1,12)
    assert result["eligible"]

def test_user_eligibility_cs215_false():
    seed_user_course_attempts("cs240_prerequisites")
    result = get_course_eligibility(1,12)
    assert not result["eligible"]

# def test_adj_lists():
#     seed_user_course_attempts("cs240_prerequisites")
#     print()
#     print(build_department_prerequisite_adj_list())

def test_get_passed_courses():
    seed_user_course_attempts("cs240_prerequisites")
    assert len(get_passed_courses(1)) == 2

def test_get_passed_courses_no_courses():
    seed_user_course_attempts("no_passed_courses")
    assert len(get_passed_courses(1)) == 0

def test_unable_to_take_cs240():
    seed_user_course_attempts("no_passed_courses")
    result = get_course_eligibility(1,12)
    assert not result["eligible"]

def test_course_preqs():
    seed_user_course_attempts("no_passed_courses")
    print()
    print(get_course_prerequisites(22))
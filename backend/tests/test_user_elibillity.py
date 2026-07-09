from src.modules.storage import memory
from .conftest import clear_memory, client, seed_course_prerequisites, seed_user_course_attempts
from src.modules.eligibility.service import evaluate_prerequisite_rule
from src.modules.eligibility.router import get_course_eligibility
from src.modules.graph.service import get_passed_courses, get_all_course_eligibilities, get_course_prerequisites
import pytest

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

    groups_for_english_2 = [
        group for group in memory.course_prerequisite_groups
        if group["course_id"] == 4
    ]
    assert len(groups_for_english_2) == 1
    group_id = groups_for_english_2[0]["id"]

    english_2_prereqs = [
        prereq for prereq in prerequisites
        if prereq["group_id"] == group_id
    ]
    assert len(english_2_prereqs) == 1
    preq_id = english_2_prereqs[0]["prerequisite_course_id"]

    course_ids = {course["id"] for course in courses}
    english_1 = english_2 = None
    for course in courses:
        if(course["id"] == preq_id):
            english_1 = course
        elif(course["id"] == 4):
            english_2 = course
    assert (4 in course_ids) and (preq_id in course_ids)
    assert english_1 is not None
    assert english_2 is not None
    assert english_1["name"] == "English I"
    assert english_2["name"] == "English II"


def test_seed_course_prerequisites_is_idempotent():
    seed_course_prerequisites()
    seed_course_prerequisites()
    assert len(memory.course_prerequisites) == 26
    assert len(memory.course_prerequisite_groups) == 16

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

def test_unable_to_take_cs360():
    seed_user_course_attempts("no_passed_courses")
    result = get_course_eligibility(1,22)
    assert not result["eligible"]

# run tests with -s param for result here
def test_all_course_eligibilities_no_passed():
    seed_user_course_attempts("no_passed_courses")
    results = get_all_course_eligibilities(1)
    truths = []
    for course in memory.courses:
        course_id: int = course['id']
        if results[course_id]['eligible'] == True:
            truths.append(results[course_id])
    assert(len(truths) == 9)

def test_get_course_prerequisites_unknown_id():
    seed_user_course_attempts("no_passed_courses")
    with pytest.raises(ValueError):
        get_course_prerequisites(24)
    results = get_course_prerequisites(23)

def test_all_course_eligibilities():
    seed_user_course_attempts("all_courses")
    results = get_all_course_eligibilities(1)
    truths = []
    for course in memory.courses:
        course_id: int = course['id']
        if results[course_id]['eligible'] == True:
            truths.append(results[course_id]["eligible"])
    assert(len(truths) == 23)
    assert all(v["eligible"] for v in results.values())

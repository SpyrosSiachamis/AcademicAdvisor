from ..storage.memory import course_prerequisites
from ..storage.memory import courses
from ..courses.service import get_all_course_ids
from collections import defaultdict
def build_department_prerequisite_adj_list() -> dict[int, list[int]]:
    #format: { course: [<course prereqs>]}
    adj_list: dict[int, list[int]] = defaultdict(list)
    all_courses = get_all_course_ids()
    if all_courses:
        for course_id in all_courses:
            adj_list.setdefault(course_id, [])

    for prerequisite in course_prerequisites:
        course_id = prerequisite["course_id"]
        prerequisite_course_id = prerequisite["prerequisite_course_id"]
        if prerequisite_course_id in adj_list[course_id]:
            continue
        adj_list[course_id].append(prerequisite_course_id)
    return dict(adj_list)
from ..storage.memory import course_prerequisite_groups, course_prerequisites
from ..courses.service import get_all_course_ids
from collections import defaultdict

def build_department_prerequisite_adj_list() -> dict[int, list[list[int]]]:
    group_to_course: dict[int, int] = {}
    for group in course_prerequisite_groups:
        group_to_course[group["id"]] = group["course_id"]

    groups_by_course: dict[int, dict[int, list[int]]] = defaultdict(dict)
    for prerequisite in course_prerequisites:
        group_id = prerequisite["group_id"]
        course_id = group_to_course.get(group_id)
        if course_id is None:
            continue
        if group_id not in groups_by_course[course_id]:
            groups_by_course[course_id][group_id] = []
        groups_by_course[course_id][group_id].append(prerequisite["prerequisite_course_id"])

    adj_list: dict[int, list[list[int]]] = {}
    all_courses = get_all_course_ids()
    if all_courses:
        for course_id in all_courses:
            adj_list.setdefault(course_id, [])

    for course_id, groups in groups_by_course.items():
        adj_list[course_id] = list(groups.values())

    return adj_list

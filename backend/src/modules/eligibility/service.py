def evaluate_prerequisite_rule(course_preq_rules: list[list[int]], passed_courses: set[int]) -> dict:
    missing_groups: list[list[int]] = []
    if(not course_preq_rules):
        return {
            "eligible": True,
        }
    eligible = True
    for and_group in course_preq_rules:
        eligible = False
        for course in and_group:
            if(course in passed_courses):
                eligible = True
                break
        if(not eligible):
            missing_groups.append(and_group)
    if(missing_groups):
        return {
            "eligible": False,
            "missing_groups": missing_groups
        }
    return {
        "eligible": True
    }
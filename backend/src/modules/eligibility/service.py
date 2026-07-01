def evaluate_prerequisite_rule(course_preq_rules: list[list[int]], passed_courses: set[int]) -> dict:
    missing_groups: list[list[str]] = []
    if(not course_preq_rules):
        return {
            "eligible": True,
        }
    groups: list[list] =[]
    for group in course_preq_rules:
        groups.append(group)
    eligible = True
    for and_group in groups:
        eligible = False
        for course in and_group:
            if(course in passed_courses):
                eligible = True
                continue
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
    
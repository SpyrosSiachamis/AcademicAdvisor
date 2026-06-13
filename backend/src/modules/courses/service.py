from .schema import Course

courses: list[dict] = []

def create_course(course: Course):
    course_data = course.model_dump()
    courses.append(course_data)
    return course_data


def get_courses():
    return courses
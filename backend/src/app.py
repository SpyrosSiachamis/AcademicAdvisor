from fastapi import FastAPI
from .modules.courses.router import router as courses_router
from .modules.users.router import router as users_router
from .modules.course_attempt.router import router as attempt_router
from .modules.university.router import router as uni_router
from .modules.department.router import router as dep_router
from .modules.course_categories.router import router as course_categories_router
from .modules.course_category_assignments.router import router as course_category_assignments_router
from .modules.course_ratings.router import router as course_ratings_router
from .modules.course_tag_assignments.router import router as course_tag_assignments_router
from .modules.course_prerequisite_groups.router import router as course_prerequisite_groups_router
from .modules.course_prerequisites.router import router as course_prerequisites_router
from .modules.course_suggested.router import router as course_suggested_router
from .modules.department_courses.router import router as department_courses_router
from .modules.tags.router import router as tags_router
from .modules.eligibility.router import router as eligibility_router

app = FastAPI()

@app.get("/")
def welcome_message():
    return {"message": "Hello!"}

app.include_router(courses_router)
app.include_router(users_router)
app.include_router(attempt_router)
app.include_router(uni_router)
app.include_router(dep_router)
app.include_router(course_categories_router)
app.include_router(course_category_assignments_router)
app.include_router(course_ratings_router)
app.include_router(course_tag_assignments_router)
app.include_router(course_prerequisite_groups_router)
app.include_router(course_prerequisites_router)
app.include_router(course_suggested_router)
app.include_router(department_courses_router)
app.include_router(tags_router)
app.include_router(eligibility_router)

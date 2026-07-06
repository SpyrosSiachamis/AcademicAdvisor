from fastapi import APIRouter, HTTPException

from .schema import CoursePrerequisiteGroup, CoursePrerequisiteGroupUpdate
from .service import create_course_prerequisite_group, delete_course_prerequisite_group, get_course_prerequisite_group, get_course_prerequisite_groups, update_course_prerequisite_group


router = APIRouter(prefix="/course-prerequisite-groups", tags=["course prerequisite groups"])


@router.post("/")
async def add_course_prerequisite_group(group: CoursePrerequisiteGroup):
    result = create_course_prerequisite_group(group)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate group or missing course")
    return {"message": "Course prerequisite group created successfully", "group": result}


@router.get("/")
async def list_course_prerequisite_groups():
    return {"message": "Retrieved all course prerequisite groups", "groups": get_course_prerequisite_groups()}


@router.get("/{group_id}")
async def get_course_prerequisite_group_by_id(group_id: int):
    result = get_course_prerequisite_group(group_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Course prerequisite group not found")
    return {"message": "Course prerequisite group found", "group": result}


@router.put("/{group_id}")
async def update_course_prerequisite_group_by_id(group_id: int, group_update: CoursePrerequisiteGroupUpdate):
    result = update_course_prerequisite_group(group_id, group_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Group not found or missing course")
    return {"message": "Course prerequisite group updated successfully", "group": result}


@router.delete("/{group_id}")
async def delete_course_prerequisite_group_by_id(group_id: int):
    result = delete_course_prerequisite_group(group_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course prerequisite group not found")
    return {"message": "Course prerequisite group deleted successfully"}

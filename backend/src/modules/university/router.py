from fastapi import APIRouter, HTTPException, Depends
from .schema import University, UniversityUpdate
from typing import Any
from .service import create_university, get_all_universities, get_university, update_university, delete_university
from ..auth.dependencies import get_current_user
router = APIRouter(prefix="/university", tags=["university"])

@router.post('/')
async def create_university_route(university: University, current_user: dict = Depends(get_current_user)):
    return await add_university(university)

@router.post('/add')
async def add_university(university: University, current_user: dict = Depends(get_current_user)):
    university_data: dict[str, Any] = university.model_dump(mode="json")
    result = create_university(university_data)
    if(result is None):
        raise HTTPException(status_code=409, detail="Duplicate University Found")
    return{
        "message": "University Created Successfully",
        "created_uni": result
    }

@router.get('/')
async def get_universities():
    available_universities = get_all_universities()
    return{
        "message": "Retrieved all universities",
        "universities": available_universities
    }

@router.get("/{university_id}")
async def get_university_by_id(university_id: int):
    result = get_university(university_id)
    if(result is None):
        raise HTTPException(status_code=404, detail="University not found")
    return {
        "message": "Successfully found university",
        "university": result
    }

@router.put("/{university_id}")
async def update_university_by_id(university_id: int, university_update: UniversityUpdate, current_user: dict = Depends(get_current_user)):
    result = update_university(university_id, university_update)
    if(result is None):
        raise HTTPException(status_code=404, detail="University not found or duplicate name")
    return {
        "message": "University updated successfully",
        "university": result
    }

@router.delete("/{university_id}")
async def delete_university_by_id(university_id: int, current_user: dict = Depends(get_current_user)):
    deleted_university = delete_university(university_id)
    if(not deleted_university):
        raise HTTPException(status_code=404, detail="University not found")
    return{
        "message": "University deleted successfully"
    }

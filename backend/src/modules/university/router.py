from fastapi import APIRouter, HTTPException
from .schema import University
from typing import Any
from .service import create_university, get_all_universities, get_university, delete_university
router = APIRouter(prefix="/university", tags=["university"])

@router.post('/add')
async def add_university(university: University):
    university_data: dict[str, Any] = university.model_dump()
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

@router.delete("/{university_id}")
async def delete_university_by_id(university_id: int):
    deleted_university = delete_university(university_id)
    if(not deleted_university):
        raise HTTPException(status_code=404, detail="University not found")
    return{
        "message": "University deleted successfully"
    }

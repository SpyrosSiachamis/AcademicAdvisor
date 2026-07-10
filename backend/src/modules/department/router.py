from fastapi import APIRouter, HTTPException, Depends
from .schema import DepartmentCreate, DepartmentRead, DepartmentUpdate
from .service import create_department, get_departments, fetch_department, update_department, delete_department
from ..auth.dependencies import get_current_user
router = APIRouter(prefix='/department', tags=['department'])

@router.post('/')
async def add_department(department: DepartmentCreate, current_user: dict = Depends(get_current_user)):
    department_data = department.model_dump(mode="json")
    result: DepartmentRead | None = create_department(department_data)
    if (result is None):
        raise HTTPException(status_code=409, detail=f"Department with id: {department_data.get('id')} failed to be created")
    return{
        "message": f"Added department with name: {result.model_dump().get('name')} successfully",
        "created_department": result.model_dump()
    }

@router.get('/')
async def list_departments():
    return {
        "message": "Retrieved all departments",
        "departments": get_departments()
    }

@router.get('/{id}')
async def get_department(id: int):
    result: DepartmentRead | None = fetch_department(id)
    if(result is None):
        raise HTTPException(status_code=404, detail=f"Department with id: {id} not found")
    return{
        "message": f"Department with id {id} found",
        "department": result
    }

@router.put('/{id}')
async def update_department_by_id(id: int, department_update: DepartmentUpdate, current_user: dict = Depends(get_current_user)):
    result: DepartmentRead | None = update_department(id, department_update)
    if(result is None):
        raise HTTPException(status_code=404, detail=f"Department with id: {id} not found, duplicate department, or missing university")
    return{
        "message": f"Department with id {id} updated successfully",
        "department": result.model_dump()
    }

@router.delete('/{id}')
async def remove_department(id: int, current_user: dict = Depends(get_current_user)):
    result: bool = delete_department(id)
    if(not result):
        raise HTTPException(status_code=404, detail=f"Department with id: {id} not found")
    return{
        "message": f"Department with id {id} deleted successfully"
    }

from fastapi import APIRouter,HTTPException
from .schema import DepartmentCreate, DepartmentRead
from .service import create_department, fetch_department, delete_department
router = APIRouter(prefix='/department', tags=['department'])

@router.post('/add')
async def add_department(department: DepartmentCreate):
    department_data = department.model_dump()
    result: DepartmentRead | None = create_department(department_data)
    if (result is None):
        raise HTTPException(status_code=409, detail=f"Department with id: {department_data.get('id')} failed to be created")
    return{
        "message": f"Added department with name: {result.model_dump().get('name')} successfully",
        "created_department": result.model_dump()
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

@router.delete('/{id}')
async def remove_department(id: int):
    result: bool = delete_department(id)
    if(not result):
        raise HTTPException(status_code=404, detail=f"Department with id: {id} not found")
    return{
        "message": f"Department with id {id} deleted successfully"
    }
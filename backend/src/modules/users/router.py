from fastapi import APIRouter, HTTPException
from .schema import UserCreate,UserRead
from .services import create_user, get_user, delete_user
router = APIRouter(prefix="/users", tags=["users"])

@router.post('/create')
async def add_user(user: UserCreate):
    created_user = create_user(user)
    if created_user is None:
        raise HTTPException(status_code=409, detail="Duplicate User")
    return{
        "message": "User Created",
        "created_user": created_user
    }

@router.get('/{user_id}')
async def get_user_by_id(user_id: int):
    result = get_user(user_id)
    if(result is None):
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} does not exist")
    return {
        "message": "User found",
        "user": result
    }

@router.delete('/{user_id}')
async def delete_user_by_id(user_id: int):
    result = delete_user(user_id)
    if(result is False):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return {
        "message": f"User with id {user_id} successfully deleted"
    }
from fastapi import APIRouter, HTTPException
from .schema import UserCreate, UserUpdate
from .services import create_user, get_users, get_user, update_user, delete_user
router = APIRouter(prefix="/users", tags=["users"])

@router.post('/')
async def create_user_route(user: UserCreate):
    return await add_user(user)

@router.post('/create')
async def add_user(user: UserCreate):
    created_user = create_user(user)
    if created_user is None:
        raise HTTPException(status_code=409, detail="Duplicate user or missing department")
    return{
        "message": "User Created",
        "created_user": created_user
    }

@router.get('/')
async def list_users():
    return {
        "message": "Retrieved all users",
        "users": get_users()
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

@router.put('/{user_id}')
async def update_user_by_id(user_id: int, user_update: UserUpdate):
    result = update_user(user_id, user_update)
    if result is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found, duplicate user, or missing department")
    return {
        "message": f"User with id {user_id} successfully updated",
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

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from .schema import UserCreate, UserUpdate
from .services import create_user, get_users, get_user, update_user, delete_user
# from ..auth.dependencies import get_current_user
from typing import Annotated
from .exceptions import (
    DuplicateUserError,
    InvalidDepartmentError,
    UserNotFoundError,
    UserDeleteError,
)
router = APIRouter(prefix="/users", tags=["users"])

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_user(user: UserCreate):
    try:
        created_user = create_user(user)
    except InvalidDepartmentError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DuplicateUserError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
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

# @router.get('/current-user')
# async def get_cur_user(user: Annotated[str,Depends(get_current_user)]):
#     return user

@router.get('/{user_id}')
async def get_user_by_id(user_id: int):
    try:
        result = get_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {
        "message": "User found",
        "user": result
    }

@router.put('/{user_id}')
async def update_user_by_id(user_id: int, user_update: UserUpdate):
    try:
        result = update_user(user_id, user_update)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidDepartmentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicateUserError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return {
        "message": f"User with id {user_id} successfully updated",
        "user": result
    }

@router.delete('/{user_id}')
async def delete_user_by_id(user_id: int):
    try:
        delete_user(user_id)
    except UserDeleteError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {
        "message": f"User with id {user_id} successfully deleted"
    }
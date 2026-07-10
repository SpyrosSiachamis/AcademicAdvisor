from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated, Any
from .security import SECRET_KEY, ALGORITHM, oauth2_scheme, create_access_token
from jose import jwt, JWTError
from starlette import status
from .schema import Token
from fastapi.security import OAuth2PasswordRequestForm
from ..users.schema import UserRead
from .services import authenticate_user
from datetime import timedelta
from .exceptions import UserIncorrectPasswordError
from ..users.services import get_user
from ..users.exceptions import UserNotFoundError
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user: dict[str,Any] = authenticate_user(form_data.username, form_data.password)
    except UserIncorrectPasswordError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    access_token = create_access_token(form_data.username,user["id"], timedelta(minutes=15))
    return {
        "access_token": access_token, "token_type": "bearer"
    }

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return get_user(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
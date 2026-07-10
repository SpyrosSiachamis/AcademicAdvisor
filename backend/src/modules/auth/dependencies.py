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
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user: dict[str,Any] = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(form_data.username,user["id"], timedelta(20))
    return {
        "access_token": access_token, "token_type": "bearer"
    }


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     try:
#         payload = jwt.decode(token)
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
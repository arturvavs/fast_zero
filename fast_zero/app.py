from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.routers import  users
from fast_zero.schemas import Message, Token
from fast_zero.security import create_access_token, verify_password

app = FastAPI()
app.include_router(users.router)
#app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá FastAPI'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Email ou senha incorretos.'
        )

    access_token = create_access_token(data_payload={'sub': user.username})
    print(access_token)
    return {'access_token': access_token, 'token_type': 'Bearer'}

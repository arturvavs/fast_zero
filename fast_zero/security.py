from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from zoneinfo import ZoneInfo

from fast_zero.database import Session, get_session
from fast_zero.models import User

pwd_context = PasswordHash.recommended()  # Contexto de encriptação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACESS_TOKEN_EXPIRE_MINUTES = 5


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data_payload: dict):
    #to_encode = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )

    data_payload.update({'exp': expire})
    encoded_jwt = jwt.encode(data_payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não foi possível autenticar o usuário',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        print('entrou try')
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print('entrou payload')
        username = payload.get('sub')
        print(payload)
        if not username:
            print('sem payload')
            raise credentials_exception
    except PyJWTError:
        print('PyJWTError')
        raise credentials_exception
    user_db = session.scalar(select(User).where(User.username == username))
    return user_db

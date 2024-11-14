from http import HTTPStatus

from fastapi import FastAPI, HTTPException

# from sqlalchemy import create_engine
from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

# engine = create_engine('postgresql://postgres:2HX65AhhiJCMXfTt@pointedly-ideal-satyr.data-1.use1.tembo.io:5432/postgres')
app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá FastAPI'}


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
# status_code=HTTPStatus.CREATE serve para retornar uma mensagem HTTP de 'Created' caso a requisição de post seja retornada corretamente
# response_model=UserPublic retorna o modelo UserPublic (sem senha) criada no schemas.py
# dessa forma a validação será através do UserSchema, mas o retorno será conforme atributos do UserPublic
def create_user(user: UserSchema):
    # user: UserSchema, define que o schema que deverá ser enviado para o servidor será o mesmo do UserSchema (username, email, password)
    # Para iniciar o ID com 1, pegamos o tamanho da lista (0) e somamos +1
    user_with_id = UserDB(
        id=len(database) + 1, **user.model_dump()
    )  # aqui digo que meu user_with_id será 1
    # **user.model_dump() pega todos os campos de UserPublic e o transforma em dicionário passando chave:valor dos atributos para UserDB
    database.append(user_with_id)
    return user_with_id

@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {'users': database}

@app.put('/users/{user_id}', response_model=UserPublic)  # Passa o userID como parâmetro de rota e retorna o esquema de UserPublic (id,username,email)
def update_user(user_id: int, user: UserSchema):  # Passa o userID como parâmetro e utiliza o UserSchema pra sofrer o update
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id

    return user_with_id

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    del database[user_id - 1]

    return {'message': 'User deleted!'}

@app.get('/users/{user_id}',response_model=UserPublic, status_code=HTTPStatus.OK)
def get_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    
    return database[user_id - 1]
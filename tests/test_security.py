import jwt

from fast_zero.security import ALGORITHM, SECRET_KEY, create_acess_token


def test_jwt():
    data = {'sub': 'teste@teste.com'}
    token = create_acess_token(data)
    decoded_result = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded_result['sub'] == data['sub']
    assert decoded_result['exp']

from http import HTTPStatus


def test_read_root_ok(client):
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá FastAPI'}


def test_create_user(client):
    response = client.post(  # Act
        '/users/',
        json={
            'username': 'arturvavs',
            'password': '123456',
            'email': 'arturavs@email.com',
        },
    )
    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == {
        'username': 'arturvavs',
        'email': 'arturavs@email.com',
        'id': 1,
    }  # Assert


def test_read_users(client):
    response = client.get('/users/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {  # Assert
        'users': [
            {
                'username': 'arturvavs',
                'email': 'arturavs@email.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'password': '123141',
            'username': 'arturvavs_update',
            'email': 'arturavs_update@email.com',
            'id': 1,
        },
    )
    if response.status_code == HTTPStatus.NOT_FOUND:
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'User not found'}

    if response.status_code == HTTPStatus.OK:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'username': 'arturvavs_update',
            'email': 'arturavs_update@email.com',
            'id': 1,
        }


def test_delete_user(client):
    response = client.delete('/users/2')
    if response.status_code == HTTPStatus.NOT_FOUND:
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'User not found'}
    if response.status_code == HTTPStatus.OK:
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'User deleted!'}

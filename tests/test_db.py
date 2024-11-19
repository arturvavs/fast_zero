from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='arturvavs1', password='password', email='artur1@email.com')
    session.add(user)
    session.commit()
    session.refresh(user)
    result = session.scalar(
        select(User).where(User.id == 1)
    )  # Scalar retorna um registro do banco de dados em formato de Objeto Python
    assert user.id == 1
    assert result.username == 'arturvavs1'

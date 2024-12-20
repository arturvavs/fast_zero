import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:'
    )  # 'sqlite:///:memory:' Cria um DB localmente em memoria que ficará disponível enquanto durar o teste
    table_registry.metadata.create_all(engine)

    # gerencimento de contexto
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)

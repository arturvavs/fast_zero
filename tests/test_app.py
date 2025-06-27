from fastapi.testclient import TestClient
from fast_zero.app import app


def test_read_root():
    """
    Teste AAA
        - Arrange
        - Act
        - Assert
    """
    # Arrange - Testa o quê ?
    client = TestClient(app)

    # Act - Executa o teste
    response = client.get('/')

    # Assert - Espera a devida resposta (1=1)
    assert response.json() == {'message': 'Olá Mundo!'}

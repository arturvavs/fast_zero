from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
# Mapped Dataclass é uma estrutura de Python, chamada Dataclass
# DATACLASS é uma classe de Dados do Python, na qual não possui métodos, apenas Atributos
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True
    )  # mapped_column é um método que atribui características como 'PK', 'Unique'... de um atributos do BD
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    # Mapped faz o mapeamento dos atributos no Python aos atributos do BD

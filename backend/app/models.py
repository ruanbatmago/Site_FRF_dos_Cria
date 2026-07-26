from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


CategoriaObjeto = Literal[
    "cozinha",
    "banheiro",
    "quarto",
    "sala",
    "limpeza",
    "decoracao",
    "eletrodomestico",
    "movel",
    "improvisado",
    "amaldicoado",
    "outro"
]

class ObjetoCriacao(BaseModel):
    autor: str = Field(
        min_length = 2,
        max_length = 50
    )

    nome: str = Field(
        min_length = 3,
        max_length = 100
    )

    descricao: str = Field(
        min_length = 3,
        max_length = 500
    )

    categoria: CategoriaObjeto

    imagem_url: HttpUrl


class ObjetoAtualizado(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    descricao: str | None = Field(
        default=None,
        min_length=3,
        max_length=500
    )

    categoria: str | None = None

    imagem_url: HttpUrl | None = None


class ObjetoResposta(BaseModel):
    id: int
    autor: str
    nome: str
    descricao: str
    categoria: CategoriaObjeto
    imagem_url: HttpUrl
    curtidas: int


class MensagemCriacao(BaseModel):
    autor: str = Field(min_length=2, max_length=50)
    conteudo: str = Field(min_length=1, max_length=1000)


class MensagemAtualizacao(BaseModel):
    autor: str | None = Field(default=None, min_length=2, max_length=50)
    conteudo: str | None = Field(default=None, min_length=1, max_length=1000)


class MensagemResposta(BaseModel):
    id: int
    autor: str
    conteudo: str
    criado_em: datetime
    atualizado_em: datetime

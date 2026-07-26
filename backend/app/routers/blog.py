from fastapi import APIRouter, HTTPException, Query, status

from .. import database
from ..models import MensagemAtualizacao, MensagemCriacao, MensagemResposta

router = APIRouter(prefix="/mensagens", tags=["blog"])


@router.get("", response_model=list[MensagemResposta])
def listar_mensagens(
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return database.list_mensagens(limit, offset)


@router.get("/{mensagem_id}", response_model=MensagemResposta)
def buscar_mensagem(mensagem_id: int):
    mensagem = database.get_mensagem(mensagem_id)
    if mensagem is None:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return mensagem


@router.post("", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
def criar_mensagem(mensagem: MensagemCriacao):
    return database.create_mensagem(mensagem)


@router.patch("/{mensagem_id}", response_model=MensagemResposta)
def atualizar_mensagem(mensagem_id: int, dados: MensagemAtualizacao):
    mensagem = database.update_mensagem(mensagem_id, dados)
    if mensagem is None:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return mensagem


@router.delete("/{mensagem_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_mensagem(mensagem_id: int):
    if not database.delete_mensagem(mensagem_id):
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")

from fastapi import APIRouter, HTTPException, Query, status

from .. import database
from ..models import ObjetoAtualizado, ObjetoCriacao, ObjetoResposta

router = APIRouter(prefix="/objetos", tags=["objetos"])


@router.get("", response_model=list[ObjetoResposta])
def listar_objetos(
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return database.list_objetos(limit, offset)


@router.get("/categorias", response_model=list[str])
def listar_categorias():
    return database.get_categorias()


@router.get("/{objeto_id}", response_model=ObjetoResposta)
def buscar_objeto(objeto_id: int):
    objeto = database.get_objeto(objeto_id)
    if objeto is None:
        raise HTTPException(status_code=404, detail="Objeto não encontrado")
    return objeto


@router.post("", response_model=ObjetoResposta, status_code=status.HTTP_201_CREATED)
def criar_objeto(objeto: ObjetoCriacao):
    return database.create_objeto(objeto)


@router.patch("/{objeto_id}", response_model=ObjetoResposta)
def atualizar_objeto(objeto_id: int, dados: ObjetoAtualizado):
    objeto = database.update_objeto(objeto_id, dados)
    if objeto is None:
        raise HTTPException(status_code=404, detail="Objeto não encontrado")
    return objeto


@router.post("/{objeto_id}/curtir", response_model=ObjetoResposta)
def curtir_objeto(objeto_id: int):
    objeto = database.like_objeto(objeto_id)
    if objeto is None:
        raise HTTPException(status_code=404, detail="Objeto não encontrado")
    return objeto


@router.delete("/{objeto_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_objeto(objeto_id: int):
    if not database.delete_objeto(objeto_id):
        raise HTTPException(status_code=404, detail="Objeto não encontrado")

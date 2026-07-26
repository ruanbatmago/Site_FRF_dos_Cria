from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .models import CategoriaObjeto, ObjetoAtualizado, ObjetoCriacao, ObjetoResposta

DB_FILE = Path(__file__).resolve().parent / "dados.db"


def get_connection(path: Path | None = None) -> sqlite3.Connection:
    db_path = DB_FILE if path is None else path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(path: Path | None = None) -> None:
    """Create the database schema if it does not exist."""
    with get_connection(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS objetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                imagem_url TEXT NOT NULL,
                curtidas INTEGER NOT NULL DEFAULT 0,
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL
            )
            """
        )
        connection.commit()


def _row_to_obj(row: sqlite3.Row) -> ObjetoResposta:
    return ObjetoResposta(
        id=row["id"],
        autor=row["autor"],
        nome=row["nome"],
        descricao=row["descricao"],
        categoria=row["categoria"],
        imagem_url=row["imagem_url"],
        curtidas=row["curtidas"],
    )


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def list_objetos(limit: int = 100, offset: int = 0) -> list[ObjetoResposta]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM objetos ORDER BY criado_em DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
    return [_row_to_obj(row) for row in rows]


def get_objeto(objeto_id: int) -> ObjetoResposta | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM objetos WHERE id = ?", (objeto_id,)
        ).fetchone()
    return _row_to_obj(row) if row is not None else None


def create_objeto(objeto: ObjetoCriacao) -> ObjetoResposta:
    created_at = _now_iso()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO objetos (autor, nome, descricao, categoria, imagem_url, curtidas, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
            """,
            (
                objeto.autor,
                objeto.nome,
                objeto.descricao,
                objeto.categoria,
                str(objeto.imagem_url),
                created_at,
                created_at,
            ),
        )
        connection.commit()
        object_id = cursor.lastrowid
    return get_objeto(object_id)


def update_objeto(objeto_id: int, dados: ObjetoAtualizado) -> ObjetoResposta | None:
    existing = get_objeto(objeto_id)
    if existing is None:
        return None

    updates: dict[str, object] = {}
    if dados.nome is not None:
        updates["nome"] = dados.nome
    if dados.descricao is not None:
        updates["descricao"] = dados.descricao
    if dados.categoria is not None:
        updates["categoria"] = dados.categoria
    if dados.imagem_url is not None:
        updates["imagem_url"] = str(dados.imagem_url)

    if not updates:
        return existing

    updates["atualizado_em"] = _now_iso()
    set_clause = ", ".join(f"{key} = ?" for key in updates)
    values: list[object] = list(updates.values())
    values.append(objeto_id)

    with get_connection() as connection:
        connection.execute(
            f"UPDATE objetos SET {set_clause} WHERE id = ?", tuple(values)
        )
        connection.commit()

    return get_objeto(objeto_id)


def delete_objeto(objeto_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM objetos WHERE id = ?", (objeto_id,))
        connection.commit()
    return cursor.rowcount > 0


def like_objeto(objeto_id: int) -> ObjetoResposta | None:
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE objetos SET curtidas = curtidas + 1, atualizado_em = ? WHERE id = ?",
            (_now_iso(), objeto_id),
        )
        connection.commit()
        if cursor.rowcount == 0:
            return None
    return get_objeto(objeto_id)


def get_categorias() -> list[CategoriaObjeto]:
    return list(CategoriaObjeto.__args__)

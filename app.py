from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime

from database import criar_banco, DATABASE_NAME


app = FastAPI(
    title="API Histórico de Endereços",
    description="API responsável por armazenar e consultar endereços pesquisados.",
    version="1.0.0"
)

criar_banco()


class Endereco(BaseModel):
    cep: str
    logradouro: str = ""
    bairro: str = ""
    cidade: str = ""
    uf: str = ""


@app.get("/")
def inicio():
    return {"mensagem": "API Histórico de Endereços funcionando!"}


@app.get("/historico")
def listar_historico():
    conexao = sqlite3.connect(DATABASE_NAME)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM enderecos")
    registros = cursor.fetchall()

    conexao.close()

    return [dict(registro) for registro in registros]


@app.get("/historico/{id}")
def buscar_endereco(id: int):
    conexao = sqlite3.connect(DATABASE_NAME)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM enderecos WHERE id = ?",
        (id,)
    )

    registro = cursor.fetchone()
    conexao.close()

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Endereço não encontrado"
        )

    return dict(registro)


@app.post("/historico")
def adicionar_endereco(endereco: Endereco):
    conexao = sqlite3.connect(DATABASE_NAME)
    cursor = conexao.cursor()

    data_consulta = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO enderecos
        (cep, logradouro, bairro, cidade, uf, data_consulta)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        endereco.cep,
        endereco.logradouro,
        endereco.bairro,
        endereco.cidade,
        endereco.uf,
        data_consulta
    ))

    conexao.commit()
    id_criado = cursor.lastrowid
    conexao.close()

    return {
        "mensagem": "Endereço salvo com sucesso",
        "id": id_criado
    }


@app.put("/historico/{id}")
def atualizar_endereco(id: int, endereco: Endereco):
    conexao = sqlite3.connect(DATABASE_NAME)
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE enderecos
        SET cep = ?, logradouro = ?, bairro = ?, cidade = ?, uf = ?
        WHERE id = ?
    """, (
        endereco.cep,
        endereco.logradouro,
        endereco.bairro,
        endereco.cidade,
        endereco.uf,
        id
    ))

    conexao.commit()

    if cursor.rowcount == 0:
        conexao.close()
        raise HTTPException(
            status_code=404,
            detail="Endereço não encontrado"
        )

    conexao.close()

    return {"mensagem": "Endereço atualizado com sucesso"}


@app.delete("/historico/{id}")
def excluir_endereco(id: int):
    conexao = sqlite3.connect(DATABASE_NAME)
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM enderecos WHERE id = ?",
        (id,)
    )

    conexao.commit()

    if cursor.rowcount == 0:
        conexao.close()
        raise HTTPException(
            status_code=404,
            detail="Endereço não encontrado"
        )

    conexao.close()

    return {"mensagem": "Endereço excluído com sucesso"}
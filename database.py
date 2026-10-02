import sqlite3
import os

DATABASE_NAME = os.getenv("DATABASE_NAME", "enderecos.db")


def criar_banco():
    conexao = sqlite3.connect(DATABASE_NAME)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enderecos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cep TEXT NOT NULL,
            logradouro TEXT,
            bairro TEXT,
            cidade TEXT,
            uf TEXT,
            data_consulta TEXT
        )
    """)

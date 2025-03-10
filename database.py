import psycopg2
import bcrypt
from psycopg2 import sql
import os

# Função para conectar ao banco de dados
# def conectar():
#     conn = psycopg2.connect(
#         host='ep-plain-rain-a8zx9490-pooler.eastus2.azure.neon.tech',
#         database='db_test_2',
#         user='db_test_2_owner',
#         password='npg_WmZ6ax9QnRcI',
#         port='5432'
#     )
#     return conn

def conectar():
    conn = psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT")
    )
    return conn


# Função para criar a tabela de usuários
def criar_tabela_usuario():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            telefone TEXT,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Função para inserir um novo usuário
def inserir_usuario(nome, usuario, telefone, email, senha):
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, usuario, telefone, email, senha)
        VALUES (%s, %s, %s, %s, %s)
    ''', (nome, usuario, telefone, email, senha_hash.decode('utf-8')))
    conn.commit()
    cursor.close()
    conn.close()

# Função para verificar o login
def verificar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT senha FROM usuarios WHERE usuario = %s', (usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado:
        return bcrypt.checkpw(senha.encode('utf-8'), resultado[0].encode('utf-8'))
    return False
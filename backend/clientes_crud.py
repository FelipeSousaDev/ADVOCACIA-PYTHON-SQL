import pyodbc
from .database import get_db_connection

class Cliente:
    def __init__(self, nome, telefone, email, cpf,  id=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf


    def __repr__(self):
        return f"Cliente(ID={self.id}, NOME='{self.nome}', CPF = '{self.cpf}')"

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.nome} | CPF: {self.cpf} | Tel: {self.telefone} | Email: {self.email}"

#FUNÇÃO CREATE
def create_cliente(cliente_obj):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO CLIENTES (NOME, TELEFONE, EMAIL, CPF) VALUES (?, ?, ?, ?)",
                cliente_obj.nome, cliente_obj.telefone, cliente_obj.email, cliente_obj.cpf
            )
            conn.commit()
            print(f"INFO: Cliente {cliente_obj.nome} inserido com sucesso!")
            return True
        except pyodbc.Error as ex:
            print(f"ERRO: Erro ao inserir cliente: {ex}")
            return False
        finally:
            conn.close()
    return False

# FUNÇÃO READ
def get_all_clientes():
    conn = get_db_connection()
    clientes = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ID, NOME, CPF, TELEFONE, EMAIL FROM CLIENTES")
            rows = cursor.fetchall()

            for row in rows:
                cliente = Cliente(id=row.ID, nome=row.NOME, cpf=row.CPF, telefone=row.TELEFONE, email=row.EMAIL)
                clientes.append(cliente)
        except pyodbc.Error as ex:
            print(f"ERRO: Erro ao buscar cliente: {ex}")
        finally:
            conn.close()
    return clientes

#FUNÇÃO UPDATE
def update_cliente(cliente_obj):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE CLIENTES SET NOME=?, TELEFONE=?, EMAIL=?, CPF=? WHERE ID=?",
                cliente_obj.nome, cliente_obj.telefone, cliente_obj.email, cliente_obj.cpf, cliente_obj.id
            )
            conn.commit()
            print(f"INFO: Cliente ID {cliente_obj.id} atualizado com sucesso!")
            return True
        except pyodbc.Error as ex:
            print(f"ERRO: Erro ao inserir cliente: {ex}")
            return False
        finally:
            conn.close()
    return False

#FUNÇÃO DELETE
def delete_cliente(cliente_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CLIENTES WHERE ID=?", cliente_id)
            conn.commit()
            print(f"INFO: Cliente ID {cliente_id} excluido com sucesso!")
            return True
        except pyodbc.Error as ex:
            print(f"ERRO: Erro ao excluir cliente: {ex}")
            return False
        finally:
            conn.close()
    return False
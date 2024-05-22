from fastapi import APIRouter, Depends, HTTPException
import mysql.connector
from connection.connection import get_connection
from models.User import Usuario
from Auth.auth import get_current_user

router = APIRouter()

@router.get("/usuarios")
async def get_usuarios(current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios"
    try:
        cursor.execute(query)
        usuarios = cursor.fetchall()
        return usuarios
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al obtener los usuarios")
    finally:
        cursor.close()

@router.get("/usuarios/{id}")
async def get_usuario(id: int, current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE id = %s"
    try:
        cursor.execute(query, (id,))
        usuario = cursor.fetchone()
        return usuario
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al obtener el usuario")
    finally:
        cursor.close()

@router.post("/usuarios")
async def create_usuario(usuario: Usuario, current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (usuario.nombre, usuario.correo, usuario.contrasena))
        connection.commit()
        return {"message": "Usuario creado correctamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al crear el usuario")
    finally:
        cursor.close()

@router.put("/usuarios/{id}")
async def update_usuario(id: int, usuario: Usuario, current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE usuarios SET nombre = %s, correo = %s, contrasena = %s WHERE id = %s"
    try:
        cursor.execute(query, (usuario.nombre, usuario.correo, usuario.contrasena, id))
        connection.commit()
        return {"message": "Usuario actualizado correctamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al actualizar el usuario")
    finally:
        cursor.close()

@router.delete("/usuarios/{id}")
async def delete_usuario(id: int, current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM usuarios WHERE id = %s"
    try:
        cursor.execute(query, (id,))
        connection.commit()
        return {"message": "Usuario eliminado correctamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al eliminar el usuario")
    finally:
        cursor.close()

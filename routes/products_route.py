from fastapi import APIRouter, Depends, HTTPException
import mysql.connector
from connection.connection import get_connection
from models.Products import Producto
from models.User import Usuario
from Auth.auth import get_current_user


router = APIRouter()

@router.get("/productos")
async def get_productos(current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM productos"
    try:
        cursor.execute(query)
        productos = cursor.fetchall()
        return productos
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al obtener los productos")
    finally:
        cursor.close()

@router.get("/productos/{id}")
async def get_producto(id: int, current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM productos WHERE id = %s"
    try:
        cursor.execute(query, (id,))
        producto = cursor.fetchone()
        return producto
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al obtener el producto")
    finally:
        cursor.close()

@router.post("/productos")
async def create_producto(producto: Producto, current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (producto.nombre, producto.descripcion, producto.precio, producto.stock))
        connection.commit()
        return {"message": "Producto creado correctamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al crear el producto")
    finally:
        cursor.close()

@router.put("/productos/{id}")
async def update_producto(id: int, producto: Producto, current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s WHERE id = %s"
    try:
        cursor.execute(query, (producto.nombre, producto.descripcion, producto.precio, producto.stock, id))
        connection.commit()
        return {"message": "Producto actualizado correctamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al actualizar el producto")
    finally:
        cursor.close()

@router.delete("/productos/{id}")
async def delete_producto(id: int, current_user: Usuario = Depends(get_current_user)):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM productos WHERE id = %s"
    try:
        cursor.execute(query, (id,))
        connection.commit()
        return {"message": "Producto eliminado correctamente"}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=500, detail="Error al eliminar el producto")
    finally:
        cursor.close()

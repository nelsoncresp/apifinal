from pydantic import BaseModel

class Producto(BaseModel):
    nombre: str
    descripcion: str = None
    precio: float
    stock: int
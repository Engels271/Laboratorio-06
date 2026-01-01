import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def agregar_producto(nombre, precio, stock, categoria, imagen):
  app_tables.productos.add_row(
    nombre=nombre,
    precio=precio,
    stock=stock,
    categoria=categoria,
    imagen=imagen
  )

@anvil.server.callable
def obtener_productos():
  return app_tables.productos.search()

@anvil.server.callable
def actualizar_producto(producto_id, nombre, precio, stock, categoria, imagen=None):
  """
    Actualiza un producto dado su ID
    """
  producto = app_tables.productos.get_by_id(producto_id)
  if producto:
    producto['nombre'] = nombre
    producto['precio'] = precio
    producto['stock'] = stock
    producto['categoria'] = categoria
    if imagen:
      producto['imagen'] = imagen

@anvil.server.callable
def eliminar_producto(producto_id):
  producto = app_tables.productos.get_by_id(producto_id)
  if producto:
    producto.delete()

  

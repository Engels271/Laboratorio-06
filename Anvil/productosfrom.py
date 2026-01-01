from ._anvil_designer import productosformTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables


class productosform(productosformTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Variable para guardar el producto que se está editando
    self.producto_actual = None

    # Cargar productos en el RepeatingPanel
    self.refrescar_productos()

    # Configurar evento del RepeatingPanel para edición
    self.repeating_panel_1.set_event_handler(
      'x-editar-producto',
      self.editar_producto
    )

    # 🔹 Configurar evento 'x-refresh' para que el panel se recargue automáticamente
    self.repeating_panel_1.set_event_handler(
      'x-refresh',
      lambda **event_args: self.refrescar_productos()
    )

  def refrescar_productos(self):
    """Carga los productos desde la tabla en el RepeatingPanel"""
    self.repeating_panel_1.items = app_tables.productos.search()

  def editar_producto(self, producto, **event_args):
    """Llenar los campos con los datos del producto para editar"""
    self.producto_actual = producto
    self.txt_nombre.text = producto['nombre']
    self.txt_precio.text = str(producto['precio'])
    self.txt_stock.text = str(producto['stock'])
    self.txt_categoria.text = producto['categoria']
    # Cambiar texto del botón a GUARDAR
    self.button_1.text = "GUARDAR"

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """Agregar un producto nuevo o guardar cambios de edición"""
    nombre = self.txt_nombre.text
    precio = float(self.txt_precio.text)
    stock = int(self.txt_stock.text)
    categoria = self.txt_categoria.text
    archivo = self.file_loader.file

    if self.producto_actual:
      # Editar producto existente usando la función del servidor
      anvil.server.call(
        'actualizar_producto',
        self.producto_actual.get_id(),  # Pasar ID del producto
        nombre,
        precio,
        stock,
        categoria,
        archivo
      )
      self.producto_actual = None
      # Volver a cambiar el botón a AGREGAR
      self.button_1.text = "AGREGAR"
    else:
      # Agregar producto nuevo llamando al servidor
      anvil.server.call(
        'agregar_producto',
        nombre,
        precio,
        stock,
        categoria,
        archivo
      )

      # Limpiar campos y refrescar lista
    self.txt_nombre.text = ""
    self.txt_precio.text = ""
    self.txt_stock.text = ""
    self.txt_categoria.text = ""
    self.file_loader.clear()
    self.refrescar_productos()

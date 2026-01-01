from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Inicializar componentes
    self.init_components(**properties)

  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    """Eliminar producto al presionar el botón eliminar con confirmación"""
    # Mostrar confirmación antes de eliminar
    if confirm(f"¿Estás seguro de eliminar el producto '{self.item['nombre']}'?"):
      # Llamar al servidor usando el ID del producto
      anvil.server.call('eliminar_producto', self.item.get_id())
      # Pedir al RepeatingPanel que se refresque
      self.parent.raise_event('x-refresh')

  @handle("button_1", "click")
  def btn_editar_click(self, **event_args):
    """Editar producto al presionar el botón editar"""
    # Llamar al método editar del formulario principal
    get_open_form().editar_producto(self.item)
    # Disparar evento al RepeatingPanel si quiere capturarlo
    self.raise_event(
      'x-editar-producto',
      producto=self.item
    )

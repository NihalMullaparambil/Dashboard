from ._anvil_designer import status_card_halfTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# import matplotlib.pyplot as plt

class status_card_half(status_card_halfTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # self.heading_label.text = 


  @property
  def card_name(self):
    print(f"Getting card_name: {self._card_name}")
    return self._card_name
    
  @property
  def current_value_pro(self):
    print(f"Getting current_value_pro: {self._current_value_pro}")
    return self._current_value_pro
  
  @property
  def total_value_pro(self):
    print(f"Getting total_value_pro: {self._total_value_pro}")
    return self._total_value_pro
  
  @property
  def peak_value_pro(self):
    print(f"Getting peak_value_pro: {self._peak_value_pro}")
    return self._peak_value_pro

  @card_name.setter
  def card_name(self, value):
    print(f"Setting card_name: {value}")
    self._card_name = value
    self.heading_label.text = value

  @current_value_pro.setter
  def current_value_pro(self, value):
    print(f"Getting current_value: {value}")
    self._current_value_pro = value
    self.current_value.text = value
  
  @total_value_pro.setter
  def total_value_pro(self, value):
    print(f"Getting total_value: {value}")
    self._total_value_pro = value
    self.total_value.text = value

  @peak_value_pro.setter
  def peak_value_pro(self, value):
    print(f"Getting total_value: {value}")
    self._peak_value_pro = value
    self.peak_value.text = value
  

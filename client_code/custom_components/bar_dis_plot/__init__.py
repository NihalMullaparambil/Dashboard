from ._anvil_designer import bar_dis_plotTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# import matplotlib.pyplot as plt

class bar_dis_plot(bar_dis_plotTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # self.heading_label.text =


  @property
  def title(self):
    print(f"Getting title: {self._title}")
    return self._title

  @property
  def title_show(self):
    print(f"Getting title_show: {self._title_show}")
    return self._title_show

  @property
  def fig_height(self):
    # print(f"Getting fig_height: {self._fig_height}")
    return self._fig_height
  
  @property
  def fig_data(self):
    # print(f"Getting fig_data: {self._fig_data}")
    return self._fig_data

  @property
  def fig_layout(self):
    # print(f"Getting fig_layout: {self._fig_layout}")
    return self._fig_layout

# 
# SETTER STARTS FROM HERE
# 

  @title_show.setter
  def title_show(self, value):
    print(f"Setting title_show: {value}")
    self._title_show = value
    self.label_1.visible = value
  
  @title.setter
  def title(self, value):
    print(f"Setting title: {value}")
    self._title = value
    self.label_1.text = value

  @fig_height.setter
  def fig_height(self, value):
    # print(f"Setting fig_height: {value}")
    self._fig_height = value
    self.plot_1.height = value
    
  @fig_layout.setter
  def fig_layout(self, value):
    # print(f"Setting fig_layout: {value}")
    self._fig_layout = value
    self.plot_1.layout = value

  @fig_data.setter
  def fig_data(self, value):
    # print(f"Setting fig_layout: {value}")
    self._fig_data = value
    self.plot_1.data = value


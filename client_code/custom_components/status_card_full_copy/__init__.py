from ._anvil_designer import status_card_full_copyTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from ... import Global
# import matplotlib.pyplot as plt


class status_card_full_copy(status_card_full_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    today_date = datetime.now().date()
    self.set_all_date_limits(today_date)

  # plot_visibility
  @property
  def plot_visibility(self):
    print(f"Getting plot_visibility: {self._plot_visibility}")
    return self._plot_visibility

  @property
  def card_name(self):
    print(f"Getting card_name: {self._card_name}")
    return self._card_name

  @property
  def average_value_pro(self):
    print(f"Getting average_value_pro: {self._average_value_pro}")
    return self._average_value_pro

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

  @average_value_pro.setter
  def average_value_pro(self, value):
    print(f"Getting average_value: {value}")
    self._average_value_pro = value
    self.average_value.text = value

  @plot_visibility.setter
  def plot_visibility(self, value):
    print(f"Getting plot_visibility: {value}")
    self._plot_visibility = value
    self.container_plot.visible = value

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("button_click")

  def set_all_date_limits(self, today_date):
    lower_date = datetime(
      today_date.year - Global.no_years_back, today_date.month, today_date.day
    ).date()
    self.date_picker_from.max_date = today_date
    self.date_picker_from.min_date = lower_date
    self.date_picker_to.max_date = today_date
    self.date_picker_to.min_date = lower_date

  def date_picker_from_change(self, **event_args):
    self.date_picker_to.min_date = self.date_picker_from.date

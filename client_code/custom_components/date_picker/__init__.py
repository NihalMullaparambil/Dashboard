from ._anvil_designer import date_pickerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from ... import Global

class date_picker(date_pickerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    today_date = datetime.now().date()
    self.set_all_date_limits(today_date) 


  def date_picker_from_change(self, **event_args):
    self.date_picker_to.min_date=self.date_picker_from.date

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('button_click')

  def set_all_date_limits(self, today_date):
    lower_date = datetime(today_date.year - Global.no_years_back, today_date.month, today_date.day).date()    
    self.date_picker_from.max_date = today_date
    self.date_picker_from.min_date = lower_date
    self.date_picker_to.max_date = today_date
    self.date_picker_to.min_date = lower_date
from ._anvil_designer import comparisonsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
from ..signin import signin
from ..project_selection import project_selection
from .. import Global

class comparisons(comparisonsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    print("\n\t homepage ")
    self.drop_down_measurand.include_placeholder = False
    self.drop_down_measurand.selected_value = Global.measurands_list[0]
    #measurand list into the dropdown
    self.drop_down_measurand.items= list(map(str, Global.measurands_list))

    #adding buttons dynamically to nav bar according to project selected and correlation_nav_bar variable
    for i in Global.correlation_nav_bar[Global.project_type]["button_names"] :
      if i == 'Measurements and Forecasts' :
        dynamic_button = Button(text = f"{i}",font_size = 18, align = "left", foreground="#d09c44")
      else :
        dynamic_button = Button(text = f"{i}",font_size = 18, align = "left")
      self.column_panel_buttons.add_component(dynamic_button)
      self.column_panel_buttons.idea_card = dynamic_button

      dynamic_button.add_event_handler('click', self.button_click(i))
      # Any code you write here will run before the form opens.


 #functions to add event click handler to dynamic buttons (according again to correlation_nav_bar)
  def button_click(self, i):
    def inner_click_func( **event_args):
      open_form(Global.correlation_nav_bar[Global.project_type]["page_names"]
              [Global.correlation_nav_bar[Global.project_type]["button_names"].index(i)])
      print("the button was pressed:",i)
    return inner_click_func

  #homepage button (can serve to reload homepage graph)
  def button_homepage_click(self, **event_args):
    open_form(Global.correlation_type_page[Global.project_type])

  #storing measurand selected and loading measurands pages

  #logout button
  def logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    Global.token = 0
    open_form('signin')

#project selection button
  def button_projectselection_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('project_selection')

  #once the timestep is selected, replot the graph accordingly




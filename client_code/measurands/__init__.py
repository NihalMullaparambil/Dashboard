from ._anvil_designer import measurandsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
from ..homepage import homepage
from ..signin import signin
from .. import Global

class measurands(measurandsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #title of the page set according to measurand selected
    self.label_2.text = Global.measurand

  #measurand dropdown
    self.drop_down_1.include_placeholder = True
    self.drop_down_1.placeholder = ""
    self.drop_down_1.selected_value = None
    self.drop_down_1.items= Global.measurands_list

  #timestep dropdown options according to global var
    self.timestep.items = Global.timestep
    #initial timestep
    timestep = 120

  #calculation of good initial amount of values that should be taken from http req
    initial_number_of_points = anvil.server.call("getInitialNumberOfPoints",Global.username, Global.password, Global.project_name, Global.token)

    #graph  info
    data, layout = anvil.server.call("plotMeasurandGraph",Global.measurand,Global.token,Global.project_id,initial_number_of_points,((initial_number_of_points/2)+40),timestep)
    self.plot_3.data = data
    self.plot_3.layout = layout


    #creating dynamic buttons
    for i in Global.correlation_nav_bar[Global.project_type]["button_names"] :
      dynamic_button = Button(text = f"{i}",font_size = 18, align = "left")
      self.column_panel_buttons.add_component(dynamic_button)
      self.column_panel_buttons.idea_card = dynamic_button

      dynamic_button.add_event_handler('click', self.button_click(i))

  #create click event handler - each button has its own page to direct
  def button_click(self, i):
    def inner_click_func( **event_args):
      open_form(Global.correlation_nav_bar[Global.project_type]["page_names"]
              [Global.correlation_nav_bar[Global.project_type]["button_names"].index(i)])
      print("the button was pressed:",i)
    return inner_click_func



  def signout_click(self, **event_args):
    """This method is called when the button is clicked"""
    signin.login_token = 0
    open_form('signin')

  def drop_down_1_change(self, **event_args):
    Global.measurand = self.drop_down_1.selected_value
    open_form('measurands')
    """This method is called when an item is selected"""

  def button_homepage_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form(Global.correlation_type_page[Global.project_type])

  def button_projectselection_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('project_selection')

  #timestep and graphs is replotted
  def timestep_change(self, **event_args):
    """This method is called when an item is selected"""
    #originally a string, convert to int
    timestep = int(self.timestep.selected_value)
    layout = self.plot_3.layout
    layout['xaxis']['dtick'] = timestep*60*1000 #dtick time is set in miliseconds
    self.plot_3.layout = layout

  def timescale_change(self, **event_args):
    """This method is called when an item is selected"""

    #if time scale implemented, a mechanism of using the data from the initial plot can be implemented.
    #that would reduce the data requests in some cases: if initialnumberofpoints > TimescalePointsMeasurand()
    # and what only would be necessary is the reduction (or "cut") of the original "self.plot_3.data" above,
    # to the desired timescale
    pass













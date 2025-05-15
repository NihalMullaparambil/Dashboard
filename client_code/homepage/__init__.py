from ._anvil_designer import homepageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
from ..signin import signin
from ..project_selection import project_selection
from .. import Global

class homepage(homepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    print("\n\t homepage ")
    self.drop_down_measurand.include_placeholder = False
    self.drop_down_measurand.selected_value = Global.measurands_list[0]
    # measurand list into the dropdown
    self.drop_down_measurand.items= list(map(str, Global.measurands_list)) 
    anvil.server.call("doInitialDataFetch", Global.token, Global.project_id, Global.measurands_list, Global.userid)

    print('\n plotMeasurandGraph2 \n')
    plot1 = anvil.server.call("plotMeasurandGraph2", Global.token, Global.project_id, Global.measurands_list[0])
    self.plot_1.data = plot1['Data']
    self.plot_1.layout = plot1['Layout']

    # adding buttons dynamically to nav bar according to project selected and correlation_nav_bar variable
    for i in Global.correlation_nav_bar[Global.project_type]["button_names"] :
      dynamic_button = Button(text = f"{i}",font_size = 18, align = "left")
      self.column_panel_buttons.add_component(dynamic_button)
      self.column_panel_buttons.idea_card = dynamic_button

      dynamic_button.add_event_handler('click', self.button_click(i))
      print(i) 
      # Any code you write here will run before the form opens.

  # def button_homepage_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   pass

  # def timestep_change(self, **event_args):
  #   """This method is called when an item is selected"""
  #   pass

 # functions to add event click handler to dynamic buttons (according again to correlation_nav_bar)
  def button_click(self, i):
    def inner_click_func( **event_args):
      open_form(Global.correlation_nav_bar[Global.project_type]["page_names"]
              [Global.correlation_nav_bar[Global.project_type]["button_names"].index(i)])
      print("the button was pressed:",i)
    return inner_click_func

# homepage button (can serve to reload homepage graph)
  def button_homepage_click(self, **event_args):
    open_form(Global.correlation_type_page[Global.project_type])

# storing measurand selected and loading measurands pages
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    Global.measurand = self.drop_down_1.selected_value
    open_form('measurands')

# logout button
  def logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    Global.token = 0
    open_form('signin')

# project selection button
  def button_projectselection_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('project_selection')

  def timescale_change(self, **event_args):
    """This method is called when an item is selected"""

      #if time scale implemented, a mechanism of using the data from the initial plot can be implemented.
      #that would reduce the data requests in some cases: if initialnumberofpoints > TimescalepointsHomepage()
      # and what only would be necessary is the reduction (or "cut") of the original "self.plot_1.data" above,
      # to the desired timescale
    pass

# once the timestep is selected, replot the graph accordingly
  def timestep_change(self, **event_args):
    #since timestep is only a layout feature, no need to call the function plot again
    # only changing the plot1.layout is enough and faster
    timestep = int(self.timestep.selected_value)
    layout = self.plot_1.layout
    layout['xaxis']['dtick'] = timestep*60*1000
    self.plot_1.layout = layout




  def button_homepage_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    open_form(Global.correlation_type_page[Global.project_type])

  def change_credentials_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('homepage1_copy')

  def drop_down_measurand_change(self, **event_args):
    """This method is called when an item is selected"""
    selected_measurand = self.drop_down_measurand.selected_value
    plot1 = anvil.server.call("plotMeasurandGraph2", Global.token, Global.project_id, selected_measurand)
    self.plot_1.data = plot1['Data']
    self.plot_1.layout = plot1['Layout']
    pass



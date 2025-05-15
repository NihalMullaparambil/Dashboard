from ._anvil_designer import homepage_PVTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
from ..signin import signin
from ..project_selection import project_selection
from .. import Global
from datetime import datetime

class homepage_PV(homepage_PVTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print("\n\t homepage_PV ")
    today_date = datetime.now().date()

    self.pv_production = "pv_production"
    self.e_demand = "e_demand" 

    anvil.server.call("doInitialDataFetch", Global.token, Global.project_id, Global.measurands_list, Global.userid)    

    print('\n Plot - PV production Overview')
    X_axis = "date"
    Y_axis = self.pv_production
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, today_date, today_date)
    self.pv_production_plot.layout = plot_temp['Layout']   
    self.pv_production_plot.data = plot_temp['Data']

    print('\n Plot - Demand')
    X_axis = "date"
    Y_axis = self.e_demand
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, today_date, today_date)
    self.e_demand_plot.layout = plot_temp['Layout']   
    self.e_demand_plot.data = plot_temp['Data']

    
    # New changes
    # print('\n PV real vs forcast plot')
    # today_date = datetime.now().date()
    # plot_temp = anvil.server.call("plotGenerator", Global.project_id, "pv_production", today_date)    
    # current_layout = plot_temp['Layout']
    # updated_layout = dict(current_layout)  # Convert to a regular dictionary if it's not already
    # updated_layout['showlegend'] = Global.show_legends    
    # self.pv_plot.data = plot_temp['Data']
    # self.pv_plot.layout = updated_layout
    # self.button_1.text = "Hide Legend" if Global.show_legends else "Show Legend"

    # adding buttons dynamically to nav bar according to project selected and correlation_nav_bar variable
    for i in Global.correlation_nav_bar[Global.project_type]["button_names"] :
      dynamic_button = Button(text = f"{i}",font_size = 18, align = "left")
      self.column_panel_buttons.add_component(dynamic_button)
      self.column_panel_buttons.idea_card = dynamic_button
      dynamic_button.add_event_handler('click', self.button_click(i))
      print(i)

    
  def status_card_full_1_button_click(self, **event_args):
    from_date = self.status_card_full_1.date_picker_from.date
    to_date = self.status_card_full_1.date_picker_to.date#
    if from_date is None or to_date is None:
      alert("Please select the dates ........!")
    else :
      print('\n Plot - PV production Overview from {0} to {1}'.format(from_date, to_date))
      X_axis = "date"
      Y_axis = self.pv_production
      plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, from_date, to_date)
      self.pv_production_plot.layout = plot_temp['Layout']   
      self.pv_production_plot.data = plot_temp['Data']
  
      print('\n Plot - Demand')
      X_axis = "date"
      Y_axis = self.e_demand
      plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, from_date, to_date)
      self.e_demand_plot.layout = plot_temp['Layout']   
      self.e_demand_plot.data = plot_temp['Data']
    


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

# logout button
  def logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    Global.token = 0
    open_form('signin')

# project selection button
  def button_projectselection_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('project_selection')

  def pv_production_plot_legends_click(self, **event_args):
    show_legends = not self.pv_production_plot.layout.showlegend
    current_layout = self.pv_production_plot.layout
    updated_layout = dict(current_layout)  # Convert to a regular dictionary if it's not already
    updated_layout['showlegend'] = show_legends
    self.pv_production_plot.layout = updated_layout
    self.pv_production_plot_legends.text = "Hide Legend" if show_legends else "Show Legend"

  def e_demand_plot_legends_click(self, **event_args):
    show_legends = not self.e_demand_plot.layout.showlegend
    current_layout = self.e_demand_plot.layout
    updated_layout = dict(current_layout)  # Convert to a regular dictionary if it's not already
    updated_layout['showlegend'] = show_legends
    self.e_demand_plot.layout = updated_layout
    self.e_demand_plot_legends.text = "Hide Legend" if show_legends else "Show Legend"


    



 
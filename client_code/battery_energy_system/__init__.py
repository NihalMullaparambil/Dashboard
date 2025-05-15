from ._anvil_designer import battery_energy_systemTemplate
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

class battery_energy_system(battery_energy_systemTemplate):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print("\n\t Page - Battery Energy System")
    today_date = datetime.now().date()
    
    # Declare all the variables here
    self.charge = "P_ESS_charge"
    self.discharge = "P_ESS_discharge" 
    self.state_of_charge = "SOC"

    print('\n Plot - Power Dynamics Over Time: Charge')
    X_axis = "date"
    Y_axis = self.charge
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, today_date, today_date) 
    print("TEST \n\n ")
    print(X_axis, Y_axis, type(today_date), today_date)
    self.power_charge_time_plot.data = plot_temp['Data']
    self.power_charge_time_plot.layout = plot_temp['Layout']
    
    print('\n Plot - Power Dynamics Over Time: Discharge')
    X_axis = "date"
    Y_axis = self.discharge
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, today_date, today_date)
    self.power_discharge_time_plot.layout = plot_temp['Layout']   
    self.power_discharge_time_plot.data = plot_temp['Data']
    
    print('\n Plot - Energy Storage and Usage Over Time')
    X_axis = "date"
    Y_axis = self.state_of_charge
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, today_date, today_date)
    self.energy_stored.layout = plot_temp['Layout']   
    self.energy_stored.data = plot_temp['Data']
  
    # sankey 
    print('\n Plot - Discharge Sankey')
    labels = ["P_ESS_discharge", "P_ESS_Con", "P_ESS_PEG"]
    source = [0, 0] # Node indices
    target = [1, 2]   # Node indices
    measurandCategoryType = "Power_Util_Real "
    plot_temp = anvil.server.call("sankeyGenerator", Global.project_id, source, target, labels, measurandCategoryType, today_date, today_date)
    self.discharge_sankey.data = plot_temp['Data']
    self.discharge_sankey.layout = plot_temp['Layout']

    labels = ["P_ESS_charge", "P_PV_ESS", "P_PEG_ESS"]
    source = [1, 2]  # Node indices
    target = [0, 0]  # Node indices
    measurandCategoryType = "Power_Util_Real "
    plot_temp = anvil.server.call("sankeyGenerator", Global.project_id, source, target, labels, measurandCategoryType, today_date, today_date)
    self.charge_sankey.data = plot_temp['Data']
    self.charge_sankey.layout = plot_temp['Layout']

    # adding buttons dynamically to nav bar according to project selected and correlation_nav_bar variable
    for i in Global.correlation_nav_bar[Global.project_type]["button_names"] :
      dynamic_button = Button(text = f"{i}",font_size = 18, align = "left")
      self.column_panel_buttons.add_component(dynamic_button)
      self.column_panel_buttons.idea_card = dynamic_button
      dynamic_button.add_event_handler('click', self.button_click(i))
      print(i)



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


  def charge_plot_legends_click(self, **event_args):
    show_legends = not self.power_charge_time_plot.layout.showlegend
    current_layout = self.power_charge_time_plot.layout
    updated_layout = dict(current_layout)  # Convert to a regular dictionary if it's not already
    updated_layout['showlegend'] = show_legends
    self.power_charge_time_plot.layout = updated_layout
    self.charge_plot_legends.text = "Hide Legend" if show_legends else "Show Legend"

  def discharge_plot_legends_click(self, **event_args):
    Global.show_legends = not Global.show_legends 
    current_layout = self.power_discharge_time_plot.layout
    updated_layout = dict(current_layout)  # Convert to a regular dictionary if it's not already
    updated_layout['showlegend'] = Global.show_legends
    self.power_discharge_time_plot.layout = updated_layout
    self.discharge_plot_legends.text = "Hide Legend" if Global.show_legends else "Show Legend"

  def energy_stored_legends_click(self, **event_args):
    Global.show_legends = not Global.show_legends 
    current_layout = self.energy_stored.layout
    updated_layout = dict(current_layout)  # Convert to a regular dictionary if it's not already
    updated_layout['showlegend'] = Global.show_legends
    self.energy_stored.layout = updated_layout
    self.energy_stored_legends.text = "Hide Legend" if Global.show_legends else "Show Legend"

  def generate_click(self, **event_args):
    from_date = self.status_card_full_1.date_picker_from.date
    to_date = self.status_card_full_1.date_picker_to.date
    if from_date is None or to_date is None: 
      alert("Please select the dates ........!")
      return
    print('Selected dates are {0} to {1}'.format(from_date, to_date))
    
    print('\n Change Plot - Power Dynamics Over Time: Charge')
    
    X_axis = "date"
    Y_axis = self.charge
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, from_date, to_date)    
    self.power_charge_time_plot.layout = plot_temp['Layout']   
    self.power_charge_time_plot.data = plot_temp['Data']
    
    print('\n Change Plot - Power Dynamics Over Time: Discharge')
    X_axis = "date"
    Y_axis = self.discharge
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, from_date, to_date)
    self.power_discharge_time_plot.layout = plot_temp['Layout']   
    self.power_discharge_time_plot.data = plot_temp['Data']
    
    print('\n Change Plot - Energy Storage and Usage Over Time')
    X_axis = "date"
    Y_axis = self.state_of_charge
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, from_date, to_date)
    self.energy_stored.layout = plot_temp['Layout']   
    self.energy_stored.data = plot_temp['Data']
  
    # sankey 
    labels = ["P_ESS_discharge", "P_ESS_Con", "P_ESS_PEG"]
    source = [0, 0] # Node indices
    target = [1, 2]   # Node indices
    measurandCategoryType = "Power_Util_Real "
    plot_temp = anvil.server.call("sankeyGenerator", Global.project_id, source, target, labels, measurandCategoryType, from_date, to_date)
    self.discharge_sankey.data = plot_temp['Data']
    self.discharge_sankey.layout = plot_temp['Layout']

    labels = ["P_ESS_charge", "P_PV_ESS", "P_PEG_ESS"]
    source = [1, 2]  # Node indices
    target = [0, 0]  # Node indices
    measurandCategoryType = "Power_Util_Real "
    plot_temp = anvil.server.call("sankeyGenerator", Global.project_id, source, target, labels, measurandCategoryType, from_date, to_date)
    self.charge_sankey.data = plot_temp['Data']
    self.charge_sankey.layout = plot_temp['Layout']

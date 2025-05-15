from ._anvil_designer import consumerTemplate
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
from ..custom_components.status_card_full import status_card_full

class consumer(consumerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print("\n\t Consumer page ")
    
    # Declare all the variables here
    self.e_demand = "e_demand"
    
    # adding buttons dynamically to nav bar according to project selected and correlation_nav_bar variable
    for i in Global.correlation_nav_bar[Global.project_type]["button_names"] :
      dynamic_button = Button(text = f"{i}",font_size = 18, align = "left")
      self.column_panel_buttons.add_component(dynamic_button)
      self.column_panel_buttons.idea_card = dynamic_button
      dynamic_button.add_event_handler('click', self.button_click(i))
      print(i)
    
    # print('\n PV real vs forcast plot')
    # plot_temp = anvil.server.call("horizontalPercentageBarPlotGenrator")
    # self.bar_dis_plot_1.fig_data = plot_temp['data']
    # self.bar_dis_plot_1.fig_layout = plot_temp['layout']

    labels = ["Con", "P_PV_Con", "P_ESS_Con", "P_PEG_Con"]
    target = [0, 0, 0] # Node indices
    source = [1, 2, 3]   # Node indices
    measurandCategoryType = "Power_Util_Real "
    today_date = datetime.now().date()
    plot_temp = anvil.server.call("sankeyGenerator", Global.project_id, source, target, labels, measurandCategoryType, today_date, today_date)
    self.bar_dis_plot_3.fig_data = plot_temp['Data']
    self.bar_dis_plot_3.fig_layout = plot_temp['Layout']

    print('\n Plot - Consumer E_demand')
    X_axis = "date"
    Y_axis = self.e_demand
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, today_date, today_date)
    self.e_demand_plot.data = plot_temp['Data']
    self.e_demand_plot.layout = plot_temp['Layout'] 
    
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

  def generate_click(self, **event_args):

    from_date = self.date_picker_1.date_picker_from.date
    to_date = self.date_picker_1.date_picker_to.date
    
    labels = ["Con", "P_PV_Con", "P_ESS_Con", "P_PEG_Con"]
    target = [0, 0, 0] # Node indices
    source = [1, 2, 3]   # Node indices
    measurandCategoryType = "Power_Util_Real "
    today_date = datetime.now().date()
    plot_temp = anvil.server.call("sankeyGenerator", Global.project_id, source, target, labels, measurandCategoryType, from_date, to_date)
    self.bar_dis_plot_3.fig_data = plot_temp['Data']
    self.bar_dis_plot_3.fig_layout = plot_temp['Layout']

    print('\n Plot - Consumer E_demand')
    X_axis = "date"
    Y_axis = self.e_demand
    plot_temp = anvil.server.call("plotGenerator3", Global.project_id, X_axis, Y_axis, from_date, to_date)
    self.e_demand_plot.data = plot_temp['Data']
    self.e_demand_plot.layout = plot_temp['Layout'] 
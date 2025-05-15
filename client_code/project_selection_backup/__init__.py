from ._anvil_designer import project_selection_backupTemplate
from anvil import *
import anvil.server
from ..signin import signin
from .. import Global



class project_selection_backup(project_selection_backupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #load all the projects the user has access to (according to username inserted at "Signin")
    self.drop_down_1.items = anvil.server.call("getUserProjects",Global.username,Global.password)
    

    # Any code you write here will run before the form opens.

#project selection dropdown changed
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""

    project = self.drop_down_1.selected_value
    #stores the project selected in Global var and gets id and type with functions
    Global.project_name = project
    Global.project_id = anvil.server.call("getProjectid",Global.username, Global.password,Global.project_name)
    Global.project_type = anvil.server.call('getProjectType',Global.username, Global.password,Global.project_name)

  #open the corresponding homepage to the project selected (determined by "correlation_type_page" global variable)
    open_form(Global.correlation_type_page[Global.project_type])  


  #signin button
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    Global.token = 0
    open_form('signin')



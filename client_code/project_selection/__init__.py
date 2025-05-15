from ._anvil_designer import project_selectionTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..signin import signin
from .. import Global

class project_selection(project_selectionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #load all the projects the user has access to (according to username inserted at "Signin")
    print("\n\t Project_selection")
    # self.drop_down_1.items = anvil.server.call('getListOfProjects',Global.projects_Json)
    self.drop_down_1.items = [""] + [info['projectName'] for info in Global.projects_data]
    # Any code you write here will run before the form opens.

#project selection dropdown changed
  def drop_down_1_change(self, **event_args):
    project = self.drop_down_1.selected_value
    #stores the project selected in Global var and gets id and type with functions
    Global.project_name = project
    try :
      target_project = next((project for project in Global.projects_data if project['projectName'] == Global.project_name), None)
      print("Global.target_project - {0} \n {1}".format(type(target_project), target_project) )
      print("Global.target_project - {0}".format(target_project['projectCategoryName']) )
      
      if target_project:
        Global.project_id = target_project['projectId']
        Global.project_type = target_project['projectCategoryName']
        Global.measurands_list = target_project['measurands']
    except Exception as e:
      print(f"An unexpected error occurred while accessing data from projects_Json: {e}")      
  #open the corresponding homepage to the project selected (determined by "correlation_type_page" global variable)
    print("Global.project_type - {0}".format(Global.project_type) )
    open_form(Global.correlation_type_page[Global.project_type])  


  #signin button
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    Global.token = 0
    open_form('signin')
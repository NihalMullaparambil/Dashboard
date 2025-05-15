from ._anvil_designer import signinTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Global #importing all global variables

class signin(signinTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.login_token=0
    # anvil.server.session["n_rings"] = 1
    # Any code you write here will run before the form opens.
  def text_box_2_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box and press sign in button"""
    if(self.email.text == '' or self.password.text == ''):
      alert("E-mail and/or password is empty!")
    else:
      #getting the username and password from textboxes 
      Global.useremail = self.email.text
      Global.password = self.password.text
      #authentication process
      try:
          temp_data = anvil.server.call('getUserData',Global.useremail,Global.password)
          # Global.token, Global.user_data = anvil.server.call('getUserToken',Global.username,Global.password)
          print("user_data - ")
          Global.token = temp_data['access_token']
          Global.username = temp_data['customer']['name']
          Global.projects_data = temp_data['projects']
          Global.userid = temp_data['customer']['customerId']
          print("Projects: ",Global.projects_Json)
          print("token: ",Global.token)
          if Global.token != '' and Global.projects_data == '':
            alert("This account has no projects associated with it ! ")
          else :
            open_form("project_selection")          
      #if getUsertoken returns error probably means mistyping of the user      
      except:
          if Global.token == '':
            alert("E-mail and/or password incorrect!")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('update_signin')


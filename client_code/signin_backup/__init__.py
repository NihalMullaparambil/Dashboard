from ._anvil_designer import signin_backupTemplate
from anvil import *
import anvil.server
from .. import Global #importing all global variables



#each page of anvil is considered/built on a class
class signin_backup(signin_backupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.login_token=0
    # Any code you write here will run before the form opens.


  #function run when the user press enter after writing at "text_box_2" - name of textbox according to the name defined at the anvil website 
  def text_box_2_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""

    #getting the username and password from textboxes 
    Global.username = self.email.text
    Global.password = self.password.text

    #authentication process
    try:
        Global.token = anvil.server.call('getUserToken',Global.username,Global.password)
        print("token: ",Global.token)
        open_form("project_selection")
        
    #if getUsertoken returns error probably means mistyping of the user      
    except:
        if Global.token == '':
          alert("E-mail and/or password incorrect!")

  #signin button - alternative to pressing enter (same process)
  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    Global.username = self.email.text
    Global.password = self.password.text
    #same process above
    try:
        Global.token = anvil.server.call('getUserToken',Global.username,Global.password)
        print("token é: ",Global.token)
        Global.headers = {'Authorization': Global.token}
        open_form('project_selection')

        
    except:
        if Global.token == '':
          alert("E-mail and/or password incorrect!")
    pass

    #change credentials button
  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('update_signin')


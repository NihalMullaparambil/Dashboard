from ._anvil_designer import update_signin2Template
from anvil import *
import anvil.server
from .. import Global

class update_signin2(update_signin2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  # update credentials button
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    Global.username = self.email.text
    Global.password = self.password.text

    #variable to guarantee that the user has correctly inserted current credentials
    login = 0
    try:
        #signin process
        Global.token = anvil.server.call('getUserToken',Global.username,Global.password)
        print("token é: ",Global.token)
        Global.headers = {'Authorization': Global.token}
        userid = anvil.server.call('getUserId',Global.username,Global.password)
        #change variable if success
        login = 1
        
            
    except:
        if Global.token == '':
          alert("E-mail and/or password incorrect!")
    
    #stores new credentials inserted
    newusername = self.newemail.text
    newpassword = self.newpassword.text

    #check var
    if login==1:
      #call function to change credentials if inserted ones
      anvil.server.call('updateCustomer',newusername, newpassword, userid, Global.token)
      alert("Credentials updated successfully!")
      open_form('signin')


  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('signin')




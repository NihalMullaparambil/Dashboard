from ._anvil_designer import mapboxTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import mapboxgl
import anvil.js
import anvil.http

class mapbox(mapboxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    #I defined my access token in the __init__
    mapboxgl.accessToken = "pk.eyJ1Ijoic3VkaGFudmFiaGF0IiwiYSI6ImNscXhvZTY5OTBnODMyanBjdGlrZHZhNXcifQ.8ahjraPbjvx1dbiT6pdPgA" 

    #put the map in the spacer 
    self.mapbox = mapboxgl.Map({'container': anvil.js.get_dom_node(self.spacer_1), 
                                'style': 'mapbox://styles/mapbox/streets-v11', #use the standard Mapbox style
                                'center': [8.676924706195404, 49.860528992311956], #center on Darmstadt
                                'zoom': 18})
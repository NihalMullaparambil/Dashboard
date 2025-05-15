import anvil.server
# This is a Global module.
# You can define global variables here, and use them from any form. Don't forget to  "from .. import Global" in each file.
#

projects_Json=''

show_legends = False

no_years_back = 2

projects_data=''

project_data_Json =''

project_name = ''

project_id =''

project_type = ''

measurand = ''

measurands_list = ''

token = ''

headers = {}

username = ""

userid = ""

useremail =''

password = ""

timescale = []

timestep = ["360","180","120","60","30","15","10","5"]

#The  website structure says that each project type should have its own homepage.
# Here each project type is associated in a dict with the respective name of the homepage it should lead to.
#For example the project type "normalprojects" has the homepage named "homepage"
correlation_type_page =  {"normalprojects":'homepage',"abnormal projects":'homepage',"dashBoardTest":'homepage',"pvTestProject":'homepage_PV'}


# Likewise, each project type has its own buttons at the navigation bar, here defined
# by the button name and the respective page it should lead to, at the same position in
# the "page_names" list. for example for the normalprojects type, the button named "Comparisons"
# when presssed will lead to the comparisons form.
# MAXIMUM of 26 characters allowed While updating the button names 
# Page names can have any number of character

correlation_nav_bar = {"normalprojects":{"button_names":["Measurements and Forecasts","Efficiency"],
                                         "page_names":["comparisons","efficiency"]
                                        },
                       "abnormal projects":{"button_names":["Measurements and Forecasts","Efficiency","Production vs E-demand"],
                                            "page_names":["comparisons","efficiency","production_VS_E_demand"]
                                           },
                       "dashBoardTest":{"button_names":["Measurements and Forecasts","Efficiency","Temparature"],
                                            "page_names":["comparisons","efficiency","temparature"]
                                           },
                       "pvTestProject":{"button_names":["Battery Energy System","Consumer"],
                                            "page_names":["battery_energy_system","consumer"]
                                           }
                      }

#
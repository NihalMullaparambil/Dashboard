import anvil
import anvil.server
import numpy as np
import requests
import pandas as pd
import time
import plotly.express as px
import json
import re
from datetime import datetime, timezone
from datetime import timedelta
import plotly.graph_objects as go
from anvil.tables import app_tables

DEBUG = True
dataTimeOut = 3000
dataTimeOut = pd.to_timedelta(dataTimeOut, unit='m')
plot_past_duration = 12
plot_future_duration = 2

# # get uplink connection - wait for anvil server in other docker to be online
# i = 0
# while i < 10:
#     try:
#         i = i+1
#         time.sleep(5)
#         print(i)              #"uplinkkey_folivora", url="ws://dashboard:3030/_/uplink"
#         anvil.server.connect("uplinkkey_folivora",  url="ws://dashboard:3030/_/uplink")
#     except:
#         pass

# local hosting:
# anvil.server.connect("uplinkkey_folivora",  url="ws://localhost:3030/_/uplink")

# When connecting to web ui
anvil.server.connect("server_MTAXBAH2SKW7WM3WC4URKYNJ-25E2YYZ4OKDD7TAH")

# get url from database
url = 'https://something'

# get database using link
# database = requests.get(url)

# use username and password to get all important info about the respective user
@anvil.server.callable
def getUserData(username,password):
  api_url = 'https://api.folivoraenergy.com/api/customers/login'
  login = {

   "email": username,

   "password": password}
  ds = ''
  while ds == '':
    try:
        ds = requests.post(api_url, json=login)
        break
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"
        time.sleep(5)
        continue
  # store json from GET
  if DEBUG:
      print("\n\t getUserData")
      print(ds.json())
  if ds.status_code == 400:
      print("\n\t UserName or password is wrong")
      raise Exception("Sorry,UserName or password is wrong")
  clearProjectTimeOutData()
  ds = ds.json()
  return ds

def clearProjectTimeOutData():
    # check for outdated data
    if DEBUG:
        print("\n\t clearProjectTimeOutData")
    for row in app_tables.projectdata.search():
        timeStamp = row["timeStamp"].replace(tzinfo=None)
        print("ROW - {0} \t time - {1}\ttime diff - {2}".format(row, timeStamp, (pd.Timestamp.now() - timeStamp)))
        if((pd.Timestamp.now() - timeStamp) > dataTimeOut):
            print("DELETED ROW - {0}".format(row))
            row.delete()

def Initial_Number_of_points(token, measurand_list):

  if DEBUG:
        print("\n\t Initial_Number_of_points ")
  number_of_points = 0
  api_url = f'https://api.folivoraenergy.com/api/listmeasurands'
  string_access_key = 'Bearer ' + token
  headers = {"Authorization": string_access_key}
  ds = ''
  while ds == '':
      try:
          ds = requests.get(api_url, headers=headers)
          break
      except requests.exceptions.ConnectionError:
          requests.status_code = "Connection refused"
          time.sleep(5)
          continue
  ds = ds.json()
  df = pd.json_normalize(ds, max_level=1)
  for measurand_id in measurand_list:
    measurand_id = int(measurand_id)
    resolution = df.loc[df["measurandId"] == measurand_id, 'resolution'].iloc[0]
    # The resolution is in seconds so int(48*60*60/resolution)
    number_of_points = int(48*60*60/resolution) + number_of_points
    # print('\nmeasurand_id \t\t- {0} \nmeasurand Resol \t- {1} \nnumber_of_points \t- {2}'.format(measurand_id,resolution,number_of_points))
  return number_of_points

def checkIfDataAlreadyExsist(projectid, userid):
    if DEBUG:
        print("\n\t checkIfDataAlreadyExsist ")
    selected_row = app_tables.projectdata.get(projectId=projectid)
    if selected_row != None:
        timeStamp = selected_row["timeStamp"].replace(tzinfo=None)
        if ((pd.Timestamp.now() - timeStamp) < dataTimeOut):
            return True
    return False

@anvil.server.callable
def doInitialDataFetch(token, projectid, measurands_list, userid):
    if DEBUG:
        print("\n\t doInitialDataFetch ")
    if checkIfDataAlreadyExsist(projectid, userid):
        return 1
    initial_number_of_points = Initial_Number_of_points(token, measurands_list)
    df = getProjectData(token, projectid, initial_number_of_points)
    df = dfto48hdata(df)
    data_JSON = df.to_json()
    app_tables.projectdata.add_row(
        timeStamp=pd.Timestamp.now(),
        projectId=projectid,
        userId=userid,
        measurands_list=measurands_list,
        access_token=token,
        data=data_JSON
    )
    return 1




#with project id and number of points to be caught, call http request
@anvil.server.callable
def getProjectData(token,projectid,number_of_points):
  if DEBUG:
      print('\n\t getProjectData')
  api_url = f'https://api.folivoraenergy.com/api/getprojectdata?id={projectid}&limit={number_of_points}'
  string_access_key = 'Bearer ' + token
  headers = {"Authorization": string_access_key}
  ds = ''
  while ds == '':  
    try:
        ds = requests.get(api_url, headers=headers)
        break
    except requests.exceptions.ConnectionError:        
        requests.status_code = "Connection refused"
        time.sleep(5)
        continue

  #store json from GET
  ds = ds.json()
  #convert the list into a df
  df = pd.json_normalize(ds,max_level=2, record_path="data",meta = ["projectCategoryName"])
  df['roundedTimestamp'] = pd.to_datetime(df['roundedTimestamp'])
  return df

#simple mechanism to say wheter the dataframe (usually filtered for the desired measurement) is
# as long as it should be (reference: measurand_number_of_points)
def enoughData(df,measurand_number_of_points):
   if len(df)<measurand_number_of_points:
      return False
   else:
      return True


#function to plot the measurand graphs
def dfto48hdata(df):
  if DEBUG:
      print('\n\t dfto48hdata')

  last_entry_time = df['roundedTimestamp'].agg([max])

  # Extract the single value from last_entry_time
  last_entry_time = last_entry_time.iloc[0]

  # Calculate the time 48 hours ago
  time_48_hours_ago = last_entry_time - timedelta(hours=48)
  # Filter the DataFrame to include only the last 48 hours
  filtered_df = df[df['roundedTimestamp'] >= time_48_hours_ago]

  filtered_df=filtered_df.reset_index(drop=True)
  return(filtered_df)


@anvil.server.callable
def plotMeasurandGraph2(token, projectid, measurand_id):
  if DEBUG:
      print('\n\t plotMeasurandGraph2')
  # Hard coded value of 500
  number_of_points = 500
  # df = getProjectData(token, projectid, number_of_points)
  try:
      for row in app_tables.projectdata.search():
          if (row["projectId"] == projectid):
              df_json = row["data"]
              df = pd.read_json(df_json)
  except Exception as e:
        print('EXCEPTION - {0}'.format(e))
  # convert the string value to integer
  measurand_id = int(measurand_id)
  df_filtered = df.loc[df["measurandId"] == measurand_id]
  # Create a Plotly figure
  graph = px.line(df_filtered, x='roundedTimestamp', y='value', title=f"Measurand {measurand_id}")

  graph.update_xaxes(showgrid=True, ticks='inside')

  graph.update_layout(
      xaxis=dict(
          rangeselector=dict(
              buttons=list([
                  dict(count=15, label="Last 15 minutes", step="minute", stepmode="backward"),
                  dict(count=30, label="30 minutes", step="minute", stepmode="backward"),
                  dict(count=1, label="Last hour", step="hour", stepmode="backward"),
                  dict(count=3, label="3 hours", step="hour", stepmode="backward"),
                  dict(count=12, label="12 hours", step="hour", stepmode="backward"),
                  dict(count=1, label="24 hours", step="day", stepmode="backward"),
                  dict(count=2, label="48 hours", step="day", stepmode="backward"),
                  # dict(step="all")
              ])
          ),
          rangeslider=dict(
              visible=True
          ),
          type="date"
      )
  )
  # graph.show()
  graph = graph.to_json()
  data = json.loads(graph)['data']
  layout = json.loads(graph)['layout']
  return_dic = {'Data': data, 'Layout': layout}
  # print('\n Data', data)
  # print('\n layout ', layout)
  return return_dic

def calculate_area_under_curve(data):
    x = [datetime.fromisoformat(date.replace("Z", "+00:00")) for date in data["x"]]
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    x_numeric = np.array([(date - epoch).total_seconds() for date in x])
    dx = np.diff(x_numeric)
    y_values = np.array(data["y"])
    avg_heights = 0.5 * (y_values[:-1] + y_values[1:])
    area = np.sum(dx * avg_heights)
    # converting ws to wh
    area = round(area / 3600, 2)
    return area
@anvil.server.callable
def plotGenerator(projectid, plotname, date):
    df = None
    date = str(date)
    selected_date = pd.to_datetime(date)
    if DEBUG:
        print('\n\t plotGenerator')
    # Plot generator supports all plots according to column defined in the project_param database
    print("plotname - {0}".format(plotname))
    print("projectId - {0}".format(projectid))
    # try:
    #     for row in app_tables.project_param.search():
    #         if (row["projectId"] == projectid):
    #             expression = row[plotname]
    # except Exception as e:
    #   print('EXCEPTION - {0}'.format(e))
    # words = re.findall(r'\b\w+\b', expression)
    try:
        for row in app_tables.projectdata.search():
            if (row["projectId"] == projectid):
                df_json = row["data"]
                df = pd.read_json(df_json)
    except Exception as e:
        print('EXCEPTION - {0}'.format(e))
    # Filtering for required Measurand
    condition = df['measurand'] == plotname
    filtered_df = df[condition].reset_index(drop=True)
    # print(filtered_df)

    # The following code is used to mimick the behavior that it is live
    # selected_date_data = filtered_df.copy()
    # selected_date_data['timestamp'] = pd.to_datetime(selected_date_data['timestamp'], unit='ms')
    # time_part = selected_date_data['timestamp'].dt.strftime('%H:%M:%S')
    # selected_date_data['timestamp'] = pd.to_datetime(date + ' ' + time_part)
    # previous_date_data = selected_date_data.copy()
    # previous_date_data['timestamp'] = previous_date_data['timestamp'] - pd.DateOffset(days=1)
    # next_date_data = selected_date_data.copy()
    # next_date_data['timestamp'] = next_date_data['timestamp'] + pd.DateOffset(days=1)
    # filtered_df = pd.concat([previous_date_data, selected_date_data, next_date_data]).reset_index(drop=True)
    # current_datetime = datetime.now()
    # if current_datetime.date() == selected_date.date():
    #   start_timestamp = current_datetime - timedelta(hours=plot_past_duration)
    #   end_timestamp = current_datetime + timedelta(hours=plot_future_duration)
    #   filtered_df = filtered_df[(filtered_df["timestamp"] >= start_timestamp) & (filtered_df["timestamp"] <= end_timestamp)]
    #   filtered_df = filtered_df[~((filtered_df["timestamp"] > current_datetime) & (filtered_df["measurandCategoryType"] == 'PV_real'))]
    # else:
    #   start_timestamp = selected_date
    #   end_timestamp = selected_date + timedelta(hours=24)
    #   filtered_df = filtered_df[(filtered_df["timestamp"] >= start_timestamp) & (filtered_df["timestamp"] <= end_timestamp)]



    fig = px.line(filtered_df, x='roundedTimestamp', y='value', color='measurandCategoryType')
    # last_pv_real = filtered_df[filtered_df['measurandCategoryType'] == 'PV_real'].iloc[-1]
    # # Hide the legend
    # fig.update_layout(showlegend=False)
    # # Add a scatter plot point to highlight the last 'PV_real' entry
    # fig.add_scatter(x=[last_pv_real['timestamp']], y=[last_pv_real['value']], mode='markers',
    #                 marker=dict(color='red', size=5), showlegend=False)

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    # finding area under curve
    # for trace in fig["data"]:
    #     if trace["type"] == "scatter" and trace["mode"] == "lines" and trace['legendgroup'] == 'PV_real':
    #         area = calculate_area_under_curve(trace)
    #         print(f"Area under curve '{trace['name']}': {area}")
    # graph = fig.to_json()
    # print(graph)

    data = fig['data']
    layout = fig['layout']
    return_dic = {'Data': data, 'Layout': layout}
    # print("\n")
    # print("\n layout \n {0}".format(layout['showlegend']))
    return return_dic

@anvil.server.callable
def plotGenerator2(projectid, plotname, from_date, to_date):
    if DEBUG:
        print('\n\t plotGenerator2')
    words = None
    expression = None
    # from_date = str(from_date)
    # to_date = str(to_date)

    # date = str(date)
    # selected_date = pd.to_datetime(date)

    # Plot generator supports all plots according to column defined in the project_param database
    print("plotname - {0}".format(plotname))
    print("projectId - {0}".format(projectid))
    try:
        for row in app_tables.project_param.search():
            if (row["projectId"] == projectid):
                expression = row[plotname]
    except Exception as e:
      print('EXCEPTION - {0}'.format(e))
    words = re.findall(r'\b\w+\b', expression) # each words is a measurands
    try:
        for row in app_tables.projectdata.search():
            if (row["projectId"] == projectid):
                df_json = row["data"]
                df = pd.read_json(df_json)
    except Exception as e:
        print('EXCEPTION - {0}'.format(e))
    print("words - {0}".format(words))
    # Filtering for required Measurand
    filtered_df = df[df['measurand'].isin(words)].reset_index(drop=True)

    # Temporary work, should be removed when we have real data.
    # Filling the same data for the selected period.

    filtered_df = fill_data(filtered_df, from_date, to_date)
    print(filtered_df.to_json())

    fig = px.line(filtered_df, x='timestamp', y='value', color='measurandCategoryType')
    last_pv_real = filtered_df[filtered_df['measurandCategoryType'] == 'PV_real'].iloc[-1]
    # Hide the legend
    fig.update_layout(showlegend=False)
    # Add a scatter plot point to highlight the last 'PV_real' entry
    fig.add_scatter(x=[last_pv_real['timestamp']], y=[last_pv_real['value']], mode='markers',
                    marker=dict(color='red', size=5), showlegend=False)

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    data = fig['data']
    layout = fig['layout']
    return_dic = {'Data': data, 'Layout': layout}
    # print("\n")
    # print("\n layout \n {0}".format(layout['showlegend']))
    return return_dic
    # return 1


@anvil.server.callable
def sankeyGenerator(projectid, source, target, labels, measurandCategoryType, from_date, to_date):
    if DEBUG:
        print('\n\t sankeyGenerator')
    try:
        for row in app_tables.projectdata.search():
            if (row["projectId"] == projectid):
                df_json = row["data"]
                df = pd.read_json(df_json)
    except Exception as e:
        print('EXCEPTION - {0}'.format(e))
    filtered_df = df[df['measurand'].isin(labels)].reset_index(drop=True)
    if from_date != to_date:
        filtered_df = fill_data(filtered_df, from_date, to_date)
    sums_by_measurand = []
    # Loop through each label (measurand) and calculate the sum for it
    for label in labels:
        filtered_df2 = filtered_df[(filtered_df['measurand'] == label) & (filtered_df['measurandCategoryType'] == measurandCategoryType)]
        sum_of_values = filtered_df2['value'].sum()
        sums_by_measurand.append(sum_of_values)
    # print(sums_by_measurand)
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=source,
            target=target,
            value=sums_by_measurand
        )))
    # Set the title and layout
    fig.update_layout(title_text='Sankey Diagram Example', font_size=10)
    data = fig['data']

    layout = fig['layout']
    return_dic = {'Data': data, 'Layout': layout}
    # print("\n")
    # print("\n layout \n {0}".format(layout['showlegend']))
    return return_dic



def fill_data(df, start_date, end_date):
    print("\n \t fill_data")
    print('start_date - {0} \t type - {1} \nend_date - {2} \t\t type - {3}'.format(start_date, type(start_date), end_date, type(end_date)))
    df_new = pd.DataFrame()
    current_date = start_date
    while current_date <= end_date:
        # Perform any action with current_date
        # For example, printing the date
        # print(current_date.strftime("%Y-%m-%d"))
        selected_date_data = df.copy()
        selected_date_data['roundedTimestamp'] = pd.to_datetime(selected_date_data['roundedTimestamp'], unit='ms')
        time_part = selected_date_data['roundedTimestamp'].dt.strftime('%H:%M:%S')
        selected_date_data['roundedTimestamp'] = pd.to_datetime(str(current_date) + ' ' + time_part)
        df_new = pd.concat([df_new, selected_date_data]).reset_index(drop=True)

        # Increment the date by one day
        current_date += timedelta(days=1)
    return df_new

@anvil.server.callable
def plotGenerator3(projectid,X_axis, Y_axis,  from_date, to_date):
    if DEBUG:
        print('\n\t plotGenerator3')
    words = None
    df = None
    words = re.findall(r'\b\w+\b', Y_axis)
    # Plot generator supports all plots according to column defined in the project_param database
    print("projectId - {0}".format(projectid))
    try:
        for row in app_tables.projectdata.search():
            if (row["projectId"] == projectid):
                df_json = row["data"]
                df = pd.read_json(df_json)
    except Exception as e:
        print('EXCEPTION - {0}'.format(e))
    print("words - {0}".format(words))
    # Filtering for required Measurand
    print("check")
    filtered_df = df[df['measurand'].isin(words)].reset_index(drop=True)

    # Temporary work, should be removed when we have real data.
    # Filling the same data for the selected period.

    filtered_df = fill_data(filtered_df, from_date, to_date)
    # print(filtered_df.to_json())
    filtered_df['line_type'] = df['measurandCategoryType'].map({'Power_Util_Real': 'Continuous', 'Power_Util_Forcast': 'Dotted', 'PV_real': 'Continuous', 'PV_forcast': 'Dotted'})

    # fig = px.line(filtered_df, x='roundedTimestamp', y='value', color='measurandCategoryType')
    fig = px.line(filtered_df, x='roundedTimestamp', y='value', line_dash='line_type')

    # Hide the legend
    fig.update_layout(showlegend=False)
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    data = fig['data']
    layout = fig['layout']
    return_dic = {'Data': data, 'Layout': layout}
    return return_dic



@anvil.server.callable
def updateCustomer(newemail, newpassword, userid, token):
  #change project1 here for generic project selected
  api_url = f'http://135.125.247.241:8080/api/updatecustomer/{userid}'
  update_login = {

   "email": newemail,
    "name": str(userid),
   "password": newpassword

   }
  string_access_key = 'Bearer ' + token
  headers = {"Authorization": string_access_key}
  ds = ''
  while ds == '':
    try:
        ds = requests.put(api_url, json=update_login, headers=headers )
        break
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"
        time.sleep(5)
        continue

  #store json from GET
  ds = ds.json()
  df = pd.json_normalize(ds, max_level=1)
  return




# @anvil.server.callable
# def plotMeasurandGraph(measurand,token,projectid,number_of_points,measurand_number_of_points,timestep):
#   #get plotting points
#   df = filterData(measurand,token,projectid,number_of_points)
#   testtimestep = timestep
#   #if df above is not long enough, return the same function but with bigger number_of_points
#   #  to be caught at the filterData func, until it's big enough and this "if" is not False anymore
#   if enoughData(df,measurand_number_of_points)==False:
#       new_number_of_points = int(1.5*number_of_points)
#       return plotMeasurandGraph(measurand,token,projectid,new_number_of_points,measurand_number_of_points,testtimestep)
#       #after df is long enough, cut the df to only the last n measurand_number_of_points
#   df = df.tail(measurand_number_of_points)
#   graph = px.line(df,x = df["roundedTimestamp"], y = df["value"], title= f"{measurand}", line_shape='vh')
#                                                     #dtick must be passed in miliseconds (timestep is in minutes)
#   graph.update_xaxes(showgrid=True,ticks='inside', dtick= (timestep)*60*1000)
#   graph.update_layout(autosize=False, width=550, height= 1200)
#   graph.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor = 'rgba(0,0,0,0)' )
#   #buttons selecting graph time scale to be shown and slider just below the graph
#   graph.update_layout(
#     xaxis=dict(
#         rangeselector=dict(
#             buttons=list([
#                dict(count=15,
#                      label="Last 15 minutes",
#                      step="minute",
#                      stepmode="backward"),
#                 dict(count=30,
#                      label="30 minutes",
#                      step="minute",
#                      stepmode="backward"),
#                 dict(count=1,
#                      label="Last hour",
#                      step="hour",
#                      stepmode="backward"),
#                 dict(count=3,
#                      label="3 hours",
#                      step="hour",
#                      stepmode="backward"),
#                 dict(count=12,
#                      label="12 hours",
#                      step="hour",
#                      stepmode="backward"),
#                 dict(count=1,
#                      label="24 hours",
#                      step="day",
#                      stepmode="backward"),
#                 dict(count=2,
#                      label="48 hours",
#                      step="day",
#                      stepmode="backward"),
#                 #dict(step="all")
#             ])
#         ),
#         rangeslider=dict(
#             visible=True
#         ),
#         type="date"
#     )
# )
#
#   #anvil doesnt accept plotly type data, therefore conversion to json is needed
#   graph = graph.to_json()
#   data = json.loads(graph)['data']
#   layout = json.loads(graph)['layout']
#
#   return data,layout
#using http request to update

#allows the getMeasurandsInfo to know which of the measurands returned by http "listmeasurands"
# are actually part of the project selected
@anvil.server.callable
def getMeasurandsIds(username,password,projectname):
  df = getUserData(username,password)
  measurands_list = []
  df_filtered = df.loc[df["projectName"]==projectname]
  for i in df_filtered["measurands"]:
     for j in i:
        measurands_list.append(str(j))
  return measurands_list


@anvil.server.callable
def getMeasurandsInfo(username, password, projectname, token):
  api_url = f'https://api.folivoraenergy.com/api/listmeasurands'
  string_access_key = 'Bearer ' + token
  headers = {"Authorization": string_access_key}
  ds = ''
  while ds == '':
    try:
        ds = requests.get(api_url, headers=headers)
        break
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"
        time.sleep(5)
        continue

  #store json from GET
  ds = ds.json()
  #convert the list into a df
  df = pd.json_normalize(ds,max_level=1)
  #list of measurands ids of the project
  measurands_project = getMeasurandsIds(username, password, projectname)
  # loop to filter the df to get only the info of the desired measurands
  for i in measurands_project:
    df = df.drop(df[df.measurandId==i].index)
  return df

#function to get the proportion of the measurands of a project 
# allowing to do math operations to determine for example the number of
#points the getProjectData should get. Returns the proportion of each measurands considering the whole
#that means, if the proportion is 0.33, that means 33% of the data points returned from getProjectData
#will be from that measurand
@anvil.server.callable
def getMeasurandsProportion(username, password, projectname, token):
   measurands_project =  getUserData(username,password)
   #filter to only the project selected
   measurands_project = measurands_project.loc[measurands_project["projectName"]==projectname]
   measurands_project = measurands_project["measurands"].values[0]

   df = getMeasurandsInfo(username, password, projectname, token)
   #filter the df, returning only the lines with "measurandId" that are contained at "measurands_project"
   df = df[df["measurandId"].isin(measurands_project)]
   #gets the bigger res as a reference point (measurand less frequent)
   max_resolution = max(df["resolution"])
   proportions = []
   for i in df["resolution"]:
      #how many times more frequent the measurand i is compared to max_res measurand
      proportions.append(max_resolution/int(i))
   #sum of all values, allows us to get the whole
   sum_proportions = sum(proportions)
   fractioned_proportions = []
   for i in proportions:
      #finally, compared to the whole, how much the measurand i represents
      fractioned_proportions.append(i/sum_proportions)
   #adding the columns "measurand_proportions" to the dataframe
   df["measurand_proportion"] = fractioned_proportions
   return df


#function that determines a minimal number of points, so that every measurand
#(even the less frequent ones) get enough data so it can plot the last 12 hours of measurement
#initially made for the homepage graph
@anvil.server.callable
def getInitialNumberOfPoints(username, password, projectname, token):
   df = getMeasurandsProportion(username, password, projectname, token)
   #proportion of less frequent
   min_proportion = min(df["measurand_proportion"])
   #resolution of less frequent
   resolution = max(df["resolution"])
   #e.g, if proportion 1/3, then 3, meaning for each 3 points got from getProjectData, 1 represents the less frequent measurand
   inverted_min_proportion = (min_proportion)**-1
                                            #3600 for resolution in seconds
   initial_number = inverted_min_proportion*(3600/resolution)*12 #12 hours
   return initial_number

#returns the number of points needed to be requested to getProjectData of a desired Measurand, based on its proportion among the other
@anvil.server.callable
def getMeasurandNumberOfPoints(username, password, projectname, token, measurand, number_of_points):
   df = getMeasurandsProportion(username, password, projectname, token)
   #filter df
   df_filtered = df.loc[df["measurandName"]==measurand]
   #get value from the df
   proportion = df_filtered["measurand_proportion"].values[0]
   #same reason as presented in "getInitialNumberofPoints"
   inverted_proportion = proportion**-1
   number = number_of_points*inverted_proportion 
   return number


#------------------------------------------ATTENTION: FUNCTIONS BELOW NOT FULLY TESTED AND IMPLEMENTED TO THE WEBSITE --------------------------------#


#functions (TimescalePointsHomepage/Measurands()) to determine how many points will be needed from the http request GET data, based on the time scale selected.
#The logic here is based on the one used at "getInitialNumberofPoints()" to get at least the last 12 hours of every measurand
# adapted to the situation and measurand required 
def TimescalePointsHomepage(username, password, projectname, token,timescale): #timescale in hours
   df = getMeasurandsProportion(username, password, projectname, token)
   #proportion of less frequent
   min_proportion = min(df["measurand_proportion"])
   #resolution of less frequent
   resolution = max(df["resolution"])
   #e.g, if proportion 1/3, then 3, meaning for each 3 points got from getProjectData, 1 represents the less frequent measurand
   inverted_min_proportion = (min_proportion)**-1
                                            #3600 for measurand resolution in seconds
   number_of_points = inverted_min_proportion*(3600/resolution)*timescale 
   return int(number_of_points)


def TimescalePointsMeasurand(username, password, projectname, token,timescale,measurand): #timescale in hours
   df = getMeasurandsProportion(username, password, projectname, token)
   print(df)
   #proportion of desired measurand
   measurand_proportion = df.loc[df['measurandName'] == measurand, 'measurand_proportion'].iloc[0]
   #resolution of desired measurand
   resolution = df.loc[df['measurandName'] == measurand, 'resolution'].iloc[0]
   #e.g, if proportion 1/3, then 3, meaning for each 3 points got from getProjectData, 1 represents the measurand
   inverted_measurand_proportion = (measurand_proportion)**-1
                                            #3600 for resolution in seconds
   number_of_points = inverted_measurand_proportion*(3600/resolution)*timescale 
   return int(number_of_points)

def clear_data_table(table_name):
    table = getattr(app_tables, table_name)
    table.delete_all_rows()

@anvil.server.callable
def getMeasurands(username, password, projectname, token):
    df = getUserData(username, password)
    # measurand id list initiated
    measurands_list = []
    # filter to project selected
    df_filtered = df.loc[df["projectName"] == projectname]
    for i in df_filtered["measurands"]:
        for j in i:
            measurands_list.append(str(j))
    # http request list measurands
    api_url = f'https://api.folivoraenergy.com/api/listmeasurands'
    string_access_key = 'Bearer ' + token
    headers = {"Authorization": string_access_key}
    ds = ''
    while ds == '':
        try:
            ds = requests.get(api_url, headers=headers)
            break
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"
            time.sleep(5)
            continue

    # store json from GET
    ds = ds.json()
    # dataframe with all measurands info
    df1 = pd.json_normalize(ds, max_level=1)
    # convert type of data from Series (panda stuff, not accepted by anvil) to string
    df1["measurandId"] = (df1["measurandId"]).astype(str)
    measurands_names = []
    # measurands ids
    for i in measurands_list:
        name = df1[df1["measurandId"] == i]
        # value of "measurandName" column
        measurands_names.append(name["measurandName"].values[0])
    return measurands_names


anvil.server.wait_forever()

import pandas as  pd
import webbrowser
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output

import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
project_name = None

def load_data(dataset_name):
    dataset_name = dataset_name
    global df
    df = pd.read_csv(dataset_name)
    
    # month dropdown
    month={
        "January":1,
        "February":2,
        "March":3,
        "April":4,
        "May":5,
        "June":6,
        "July":7,
        "August":8,
        "September":9,
        "October":10,
        "November":11,
        "December":12
        }
    
    global month_list
    month_list=[{'label':key,'value':values} for key,values in month.items()]
    
    global region_list
    temp_list = sorted(df['region_txt'].unique().tolist())
    region_list = [ {'label':str(i),'value':str(i)} for i in temp_list]
  
    global attack_type_list
    temp_list = df['attacktype1_txt'].unique().tolist()
    attack_type_list = [ {'label':str(i),'value':str(i)} for i in temp_list]
    
    global year_list
    year_list = sorted(df['iyear'].unique().tolist())
    
    global year_dict
    year_dict = { str(year):str(year) for year in year_list}
    
    print(df.head())

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8030')

def create_app_ui():
    main_layout = html.Div(
        [
          dbc.Row(
              [
                 dbc.Col(
                      html.H1(id='main_title',children='Terrorism Analysis with Insights',className="main-title"),
                      md=8
                     ),
                 
                 dbc.Col(
                      dcc.Tabs(id="tabs-heading", value='world',parent_className="custom-tabs", className="custom-tabs-container",children=[
                          dcc.Tab(label='World', value='world',className="custom-tab",selected_className='custom-tab--selected'),
                          dcc.Tab(label='India', value='india',className="custom-tab",selected_className='custom-tab--selected'),
                          ]),
                      md=4
                     ),
              ],className="remove-margin"
              ),
       
        html.Div(id='tabs-content')
        ],
        className="main-div"
        )
    return main_layout


@app.callback(
    Output('tabs-content','children'), 
    [
     Input('tabs-heading','value')
     ]
    )
def render_tab_content(tab):
    print(tab,"====TAB")
    if tab=='world':
        load_data('global_terror.csv')
       
        return html.Div(
        [
  
             dbc.Row(
             [
                dbc.Col(
                    [
                     html.H6("Month",className="dropdown-heading"),
                     dcc.Dropdown(
                         id='month-dropdown',
                         options=month_list,
                         multi = True,
                         placeholder ='Select Month',
                          className="dropdown-custom"
                         )],
                    md=3
                    ),
                dbc.Col(
                    [
                     html.H6("Date",className="dropdown-heading"),   
                     dcc.Dropdown(
                         id='date-dropdown',
                         placeholder ='Select Date',
                         multi = True,
                          className="dropdown-custom"
                         )],
                    md=3
                    ),
                dbc.Col(
                    [
                      html.H6("Region",className="dropdown-heading"),  
                      dcc.Dropdown(
                          id='region-dropdown',
                          options=region_list,
                          multi = True,
                          placeholder ='Select Region',
                           className="dropdown-custom"
                          )],
                    md=3
                    ),
                dbc.Col(
                    [
                    html.H6("Country",className="dropdown-heading"),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label':'All','value':'All'}],
                        multi = True,
                        placeholder ='Select Country',
                         className="dropdown-custom"
                        )],
                    md=3
                    ),
             ],className="remove-margin"
             ),
         
          html.Br(),
          html.Br(),
         
        dbc.Row(
            [
               dbc.Col(
                   [
                    html.H6("State",className="dropdown-heading"),   
                    dcc.Dropdown(
                        id='state-dropdown',
                        options=[{'label':'All','value':'All'}],
                        multi = True,
                        placeholder ='Select State',
                        className="dropdown-custom"
                        )],
                    md=3
                   ),
               dbc.Col(
                   [
                     html.H6("City",className="dropdown-heading"),
                     dcc.Dropdown(
                         id='city-dropdown',
                         options=[{'label':'All','value':'All'}],
                         multi = True,
                         placeholder ='Select City',
                         className="dropdown-custom"
                         )],
                     md=3
                   ),
               dbc.Col(
                   [
                   html.H6("Attack Type",className="dropdown-heading"),
                   dcc.Dropdown(
                       id='attacktype-dropdown',
                       options=attack_type_list,
                       multi = True,
                       placeholder ='Select Attack Type',
                        className="dropdown-custom"
                       )],
                   md=3
                   )
            
            ],className="remove-margin"
            ),        
         html.Br(),
        
         html.H5(id='year-title', children='Select the Year',className='year-title'),
         
          dcc.RangeSlider(
             id = 'year-slider',
             min = min(year_list),
             max = max(year_list),
             value= [min(year_list),max(year_list)],
             marks = year_dict
             ),
         
          html.Br(),
            
         dcc.Loading(dcc.Graph(id = 'graph-object',figure = go.Figure())), 
         
          dbc.Row(
              [
               
               dbc.Col(
                      dcc.Tabs(id="analysis-tabs", value='histogram',parent_className="custom-analysis-tabs", className="custom-analysis-tabs-container",children=[
                          dcc.Tab(label='Histogram', value='histogram',className="custom-tab",selected_className='custom-tab--selected'),
                          dcc.Tab(label='Pie Chart', value='piechart',className="custom-tab",selected_className='custom-tab--selected'),
                          dcc.Tab(label='Stacked Bar Chart', value='stackedbarchart',className="custom-tab",selected_className='custom-tab--selected'),
                          dcc.Tab(label='Animated Scatter Geo plot', value='animatedgeo',className="custom-tab",selected_className='custom-tab--selected',
                                   children=[
                                       dcc.Dropdown(
                                           id='attacktype-dropdown-analysis',
                                           options=attack_type_list,
                                           value='Bombing/Explosion',
                                           placeholder ='Select Attack Type',
                                           className="dropdown-custom",
                                             style={'width':'60%'}
                                           ),
                                      ]
                                  ),
                          dcc.Tab(label='Heat map', value='heatmap',className="custom-tab",selected_className='custom-tab--selected'),
                          ]),
                      md=12
                     ),
              ],className="remove-margin"),
          html.Div([
            dbc.Row([
                dbc.Col(
               [   
               
               dcc.Loading(dcc.Graph(id = 'analysis-graphs',figure = go.Figure()))],md=12
               )
                
                ])
            ])
        ],
        className="main-div"
        )
    #===============================INDIA=========================================#
    elif tab=="india":
       print("INDIA")
       load_data('india_terror.csv')
       global state_list_india
       temp_list = df['provstate'].unique().tolist()
       state_list_india = [ {'label':str(i),'value':str(i)} for i in temp_list]
       return html.Div(
        [
  
         dbc.Row(
             [
                dbc.Col(
                    [
                     html.H6("Month",className="dropdown-heading"),   
                     dcc.Dropdown(
                         id='month-dropdown-india',
                         options=month_list,
                         multi = True,
                         placeholder ='Select Month',
                          className="dropdown-custom"
                         )],
                    md=3
                    ),
                dbc.Col(
                    [
                     html.H6("Date",className="dropdown-heading"),
                     dcc.Dropdown(
                         id='date-dropdown-india',
                         placeholder ='Select Date',
                         multi = True,
                          className="dropdown-custom"
                         )],
                    md=3
                    ),
                dbc.Col(
                    [
                     html.H6("State",className="dropdown-heading"),
                    dcc.Dropdown(
                        id='state-dropdown-india',
                        options=state_list_india,
                        multi = True,
                        placeholder ='Select State',
                         className="dropdown-custom"
                        )],
                    md=3
                   ),
               dbc.Col(
                   [
                     html.H6("City",className="dropdown-heading"),
                     dcc.Dropdown(
                         id='city-dropdown-india',
                         options=[{'label':'All','value':'All'}],
                         multi = True,
                         placeholder ='Select City',
                          className="dropdown-custom"
                         )],
                     md=3
                   ),
                
             ],className="remove-margin"
             ),
         
          html.Br(),
          html.Br(),
         
        dbc.Row(
            [
               
               dbc.Col(
                   [
                     html.H6("Attack Type",className="dropdown-heading"),
                   dcc.Dropdown(
                       id='attacktype-dropdown-india',
                       options=attack_type_list,
                       multi = True,
                       placeholder ='Select Attack Type',
                        className="dropdown-custom"
                       )],
                   md=3
                   )
            
            ],className="remove-margin"
            ),        
         
        
         html.H5(id='year-title', children='Select the Year',className="year-title"),
         
          dcc.RangeSlider(
             id = 'year-slider-india',
             min = min(year_list),
             max = max(year_list),
             value= [min(year_list),max(year_list)],
             marks = year_dict
             
             ),
         
          html.Br(),
          
          dcc.Loading(dcc.Graph(id = 'graph-object-india',figure=go.Figure())), 
            dbc.Row(
              [
               
               dbc.Col(
                      dcc.Tabs(id="analysis-tabs-india", value='histogram',parent_className="custom-analysis-tabs", className="custom-analysis-tabs-container",children=[
                          dcc.Tab(label='Histogram', value='histogram',className="custom-tab",selected_className='custom-tab--selected'),
                          dcc.Tab(label='Pie Chart', value='piechart',className="custom-tab",selected_className='custom-tab--selected'),
                          dcc.Tab(label='Stacked Bar Chart', value='stackedbarchart',className="custom-tab",selected_className='custom-tab--selected'),
                          dcc.Tab(label='Animated Scatter Geo plot', value='animatedgeo',className="custom-tab",selected_className='custom-tab--selected',
                                  children=[
                                       dcc.Dropdown(
                                           id='attacktype-dropdown-analysis-india',
                                           options=attack_type_list,
                                           value='Bombing/Explosion',
                                           placeholder ='Select Attack Type',
                                           className="dropdown-custom",
                                           style={'width':'60%'}
                                           ),
                                      ]
                                  ),
                          dcc.Tab(label='Heat map', value='heatmap',className="custom-tab",selected_className='custom-tab--selected'),
                          ]),
                      md=12
                     ),
              ],className="remove-margin"),
         html.Div([
            dbc.Row([
                dbc.Col(
               [   
               
               dcc.Loading(dcc.Graph(id = 'analysis-graphs-india',figure = go.Figure()))],md=12
               )
                
                ])
            ])
        
        ],
        className="main-div"
        )


@app.callback(
    Output('graph-object','figure'),
    [
      Input('month-dropdown','value'),
      Input('date-dropdown','value'),
      Input('region-dropdown','value'),
      Input('country-dropdown','value'),
      Input('state-dropdown','value'),
      Input('city-dropdown','value'),
      Input('attacktype-dropdown','value'),
      Input('year-slider','value'),
     ]
    )
def update_app_ui(month_value,date_value,region_value,country_value,state_value,city_value,attack_value,year_value):
    
   
    # year filter
    year_range = range(year_value[0], year_value[1]+1)
    new_df = df[df["iyear"].isin(year_range)]
        
        # month_filter
    if month_value==[] or month_value is None:
        pass
    else:
        if date_value==[] or date_value is None:
            new_df = new_df[new_df["imonth"].isin(month_value)]
        else:
            new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        # region, country, state, city filter
    if region_value==[] or region_value is None:
        pass
    else:
        if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
        else:
            if state_value == [] or state_value is None:
                new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
            else:
                if city_value == [] or city_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
    if attack_value == [] or attack_value is None:
        pass
    else:
        new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]     
    
   
    figure = px.scatter_mapbox( new_df,
                               lat = "latitude",
                               lon = "longitude",
                               color= "attacktype1_txt",
                               hover_data = ["region_txt","country_txt","provstate","city","attacktype1_txt","nkill","iyear"],
                               zoom=1.2 ,
                               labels={"attacktype1_txt":"Attack Type"}
                              )
    
    figure.update_layout(mapbox_style="open-street-map",
                         autosize = True,
                         margin = dict(l=20, r=20, t=25, b=20),
                         
                         )
    figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })  
    
    return figure


@app.callback(
    Output('graph-object-india','figure'),
    [
      Input('month-dropdown-india','value'),
      Input('date-dropdown-india','value'),
      Input('state-dropdown-india','value'),
      Input('city-dropdown-india','value'),
      Input('attacktype-dropdown-india','value'),
      Input('year-slider-india','value'),
     ]
    )
def update_india_app_ui(month_value,date_value,state_value,city_value,attack_value,year_value):
    print("UPDATE INDIA")
    # year filter
    year_range = range(year_value[0],year_value[1]+1)
    new_df = df[df['iyear'].isin(year_range)]
    
    # month 
    if month_value!= [] and month_value!= None:
        new_df=new_df[new_df['imonth'].isin(month_value)]
        
    # date  
    if date_value!=[] and date_value!=None:
        new_df=new_df[new_df['iday'].isin(date_value)]
     
    # state
    if state_value != [] and state_value != None:
        new_df = new_df[new_df["provstate"].isin(state_value)]
    
    # city
    if city_value != [] and city_value !=None:
        new_df = new_df[new_df["city"].isin(city_value)]
    
    # attack type    
    if attack_value != [] and attack_value != None:
        new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]
    
   
    figure = px.scatter_mapbox( new_df,
                               lat = "latitude",
                               lon = "longitude",
                               color= "attacktype1_txt",
                               hover_data = ["provstate","city","attacktype1_txt","nkill","iyear"],
                               zoom=3,
                               labels={"attacktype1_txt":"Attack Type"}
                              )
    
    figure.update_layout(mapbox_style="open-street-map",
                         autosize = True,
                         margin = dict(l=20, r=20, t=25, b=20)
                         )
    
    figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
    
    return figure



@app.callback(
    Output('date-dropdown','options'),
    [
      Input('month-dropdown','value')
     ]
    
    )
def update_date(month_value):
 
    if month_value in [1,3,5,7,8,10,12]:
        return [{'label':m,'value':m} for m in range(1,32)]
    elif month_value in [4,6,9,11]:
        return [{'label':m,'value':m} for m in range(1,31)]
    elif month_value==2:
        return [{'label':m,'value':m} for m in range(1,30)]
    else:
        return []
    

@app.callback(
    
    Output('country-dropdown','options'), 
    [
     Input('region-dropdown','value')
     ]
    )
def set_country_options(region_value):
    if region_value!=None and region_value!=[]:
        return [{'label':str(i),'value':str(i)} for i in df[df['region_txt'].isin(region_value)]['country_txt'].unique().tolist()]
    
        
 
@app.callback(
    
     Output('state-dropdown','options'),
    [
      Input('country-dropdown','value'),
     ]
    ) 
def set_state_options(country_value):
        if country_value!=None and country_value!=[]:
            return [{'label':str(i),'value':str(i)} for i in df[df['country_txt'].isin(country_value)] ['provstate'].unique().tolist()]
        

@app.callback(
    Output('city-dropdown','options'),
    [
      Input('state-dropdown','value'),
     ]
    )
def set_city_options(state_value):
        if state_value!=None and state_value!=[]:
            return [{'label':str(i),'value':str(i)} for i in df[df['provstate'].isin(state_value)] ['city'].unique().tolist()]
        
    
# ==========================INDIA===========================#

@app.callback(
    Output('date-dropdown-india','options'),
    [
      Input('month-dropdown-india','value')
     ]
    
    )
def update_date_india(month_value):
 
    if month_value in [1,3,5,7,8,10,12]:
        return [{'label':m,'value':m} for m in range(1,32)]
    elif month_value in [4,6,9,11]:
        return [{'label':m,'value':m} for m in range(1,31)]
    elif month_value==2:
        return [{'label':m,'value':m} for m in range(1,30)]
    else:
        return []
            

@app.callback(
    Output('city-dropdown-india','options'),
    [
      Input('state-dropdown-india','value'),
     ]
    )
def set_india_city_options(state_value):
    if state_value!=None and state_value!=[]:
        return [{'label':str(i),'value':str(i)} for i in df[df['provstate'].isin(state_value)] ['city'].unique().tolist()]    


#============================analysis-tabs-world=======================#
@app.callback(
    Output('analysis-graphs', 'figure'),
    [
      Input('analysis-tabs','value'),
      Input('attacktype-dropdown-analysis','value')
     ]
    
    )
def render_analysis_tab_content(tab,attackvalue):
    print(attackvalue,"ATTACKVALUE")
    figure=go.Figure()
    if tab=='histogram': 
        figure =  px.histogram(df, y="attacktype1_txt",labels={'attacktype1_txt':'Attack Type'}).update_yaxes(categoryorder="total ascending")
        figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
        figure.update_layout(title={"text" : "Histogram of various attacks", 'x' : 0.5, 'y' : 0.93})
        
    elif tab=='piechart':
        figure = px.pie(df,"region_txt",color="region_txt" )
        figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
        figure.update_layout(title={"text" : "Concentration of various attack types in different regions", 'x' : 0.5, 'y' : 0.93})
        
    elif tab=='stackedbarchart':
       stacked_data = df.groupby("iyear")["attacktype1_txt"].value_counts().reset_index(name='count') 
       figure = px.bar(stacked_data, x="iyear", y="count", color="attacktype1_txt", barmode = 'stack',labels={'attacktype1_txt':'Attack Type'}) 
       figure.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                   title={"text" : "Stacked bar chart of year-wise attack types", 'x' : 0.5, 'y' : 0.93}
                                  )
       figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
       
    elif tab=='animatedgeo':
        n_df = df[df['attacktype1_txt']==attackvalue]
        """figure = px.scatter_mapbox(n_df,
                               lat = "latitude",
                               lon = "longitude",
                                color= "attacktype1_txt",
                               hover_data = ["provstate","city","attacktype1_txt","nkill","iyear"],
                               zoom=2.5,
                               labels={"attacktype1_txt":"Attack Type"},
                               animation_frame="iyear"
                              )
    
        figure.update_layout(mapbox_style="open-street-map",
                         autosize = True,
                         margin = dict(l=20, r=20, t=25, b=20)
                         )"""
        
        figure = px.scatter_geo(n_df, lat='latitude', lon='longitude',
                            hover_name="country_txt", hover_data=['iyear', 'city',"attacktype1_txt"],
                            labels={'iyear':'Year', 'city': 'City', 'latitude':'Latitude', 'longitude':'Longitude',"attacktype1_txt":"Attack Type"},
                            animation_frame="iyear", color = "attacktype1_txt",
                            projection="natural earth")
        figure.update_layout(autosize=True,
                                  margin=dict(l=20, r=20, t=50, b=20),
                                  title={"text" : "Year-wise Bombing/Explosion attacks"}
                                  )
        figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
        
        
    elif tab=="heatmap":
        n_df = df.groupby("attacktype1_txt")["nkill"].sum().reset_index(name="Fatalities")
        figure = ff.create_annotated_heatmap(n_df["Fatalities"].values.reshape(3,3), annotation_text=n_df["attacktype1_txt"].values.reshape(3,3), colorscale='tealgrn', hoverinfo='z', showscale=True)
        
        figure.update_layout(autosize=True,
                            title={"text" : "Heatmap of fatalities in various attacks", 'x' : 0.5, 'y' : 0.93},
                            font=dict(size=14),
                            )
        figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
    return figure
#==============================Analysis-tabs-India===============================#

@app.callback(
    Output('analysis-graphs-india', 'children'),
    [
      Input('analysis-tabs-india','value'),
      Input('attacktype-dropdown-analysis-india','value')
     ]
    
    )
def render_analysis_tab_content_india(tab,attackvalue):
    figure = go.Figure()
    if tab=='histogram': 
        figure =  px.histogram(df, y="attacktype1_txt",labels={'attacktype1_txt':'Attack Type'} ).update_yaxes(categoryorder="total ascending")
        figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
        figure.update_layout(title={"text" : "Histogram of various attacks", 'x' : 0.5, 'y' : 0.93})
        
    elif tab=='piechart':
        figure = px.pie(df,"attacktype1_txt",color="attacktype1_txt")
        figure.update_layout(title={"text" : "Contribution of various attack types using pie chart", 'x' : 0.5, 'y' : 0.93})
        figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
       
    elif tab=='stackedbarchart':
       stacked_data = df.groupby("iyear")["attacktype1_txt"].value_counts().reset_index(name='count') 
       figure = px.bar(stacked_data, x="iyear", y="count", color="attacktype1_txt", barmode = 'stack',labels={'attacktype1_txt':'Attack Type'}) 
       figure.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  title={"text" : "Stacked bar chart of year-wise attack types", 'x' : 0.5, 'y' : 0.93}
                                  )
       figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
      
    elif tab=='animatedgeo':
        n_df = df[df['attacktype1_txt']==attackvalue]
        """figure = px.scatter_mapbox(n_df,
                               lat = "latitude",
                               lon = "longitude",
                                color= "attacktype1_txt",
                               hover_data = ["provstate","city","attacktype1_txt","nkill","iyear"],
                               zoom=2.5,
                               labels={"attacktype1_txt":"Attack Type"},
                               animation_frame="iyear"
                              )
    
        figure.update_layout(mapbox_style="open-street-map",
                         autosize = True,
                         margin = dict(l=20, r=20, t=25, b=20)
                         )"""
        
        figure = px.scatter_geo(n_df, lat='latitude', lon='longitude',
                            hover_name="country_txt", hover_data=['iyear', 'city',"attacktype1_txt"],
                            labels={'iyear':'Year', 'city': 'City', 'latitude':'Latitude', 'longitude':'Longitude',"attacktype1_txt":"Attack Type"},
                            animation_frame="iyear", color = "attacktype1_txt",
                            projection="natural earth",scope="asia")
        figure.update_layout(autosize=True,
                                  margin=dict(l=20, r=20, t=50, b=20),
                                  title={"text" : "Year-wise Bombing/Explosion attacks"}
                                  )
        figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
        
        
    elif tab=="heatmap":
        n_df = df.groupby("attacktype1_txt")["nkill"].sum().reset_index(name="Fatalities")
        figure = ff.create_annotated_heatmap(n_df["Fatalities"].values.reshape(3,3), annotation_text=n_df["attacktype1_txt"].values.reshape(3,3), colorscale='tealgrn', hoverinfo='z', showscale=True)
        
        figure.update_layout(autosize=True,
                            title={"text" : "Heatmap of fatalities in various attacks", 'x' : 0.5, 'y' : 0.93},
                            font=dict(size=14),
                            )
        figure.update_layout({
            'plot_bgcolor': '#21314e',
            'paper_bgcolor': '#1b2a47',
            'font_color':"#ffffff"
                })
    return figure

def main():
    print("Welcome to Dash app...")
    load_data('global_terror.csv')
    
    open_browser()  
    
    # If you want to assign something to global variable inside a function, then we have to declare that variable as global.
    # If we are just reading, and not assigning then we don't have to declare global
    
    global project_name
    project_name = "Terrorism Analysis with Insights"
    
        
    global app
    app.title = project_name
    app.layout = create_app_ui()
    app.run_server(host='127.0.0.1',port=8030)
   
    
    print("This would be executed only after the server is down/stopped")
    
    # Reset all the global variables once the server stops
    df = None
    app = None
    project_name = None
    
if __name__ == '__main__' :
    main()
    
    
    
    
    
    
    
    
    
    
    
    
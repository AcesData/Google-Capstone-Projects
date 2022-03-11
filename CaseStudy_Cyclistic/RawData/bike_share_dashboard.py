# Read the library
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from datetime import datetime as dte
import datetime as dt
import plotly.graph_objects as go
from datetime import timedelta
import dash_bootstrap_components as dbc
import dash_table


# FUNCTION TO CONVERT SECONDS TO HH:MM:SS FORMAT
def converttimehhmmss(sec):
    hhmmss=str(timedelta(seconds=sec))
    return hhmmss

# FUNCTION TO READ RAW DATA
def read_data():
    df1=pd.read_csv('202004-divvy-tripdata.csv')
    # df=df1
    df2=pd.read_csv('202005-divvy-tripdata.csv')
    df3=pd.read_csv('202006-divvy-tripdata.csv')
    df4=pd.read_csv('202007-divvy-tripdata.csv')
    df5=pd.read_csv('202008-divvy-tripdata.csv')
    df6=pd.read_csv('202009-divvy-tripdata.csv')
    df7=pd.read_csv('202010-divvy-tripdata.csv')
    df8=pd.read_csv('202011-divvy-tripdata.csv')
    df9=pd.read_csv('202012-divvy-tripdata.csv')
    df10=pd.read_csv('202101-divvy-tripdata.csv')
    df11=pd.read_csv('202102-divvy-tripdata.csv')
    df12=pd.read_csv('202103-divvy-tripdata.csv')
    df=df1.append([df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12])
    
    return df
dff=read_data()

def df_cleaned(start_date,end_date):
    start = dte.strptime(start_date[:10], '%Y-%m-%d')
    end = dte.strptime(end_date[:10], '%Y-%m-%d')
    end=end+timedelta(1)
    ## DATA CLEANING
    # df=dff
    dff['started_at'] = pd.to_datetime(dff['started_at'])
    dffiltered =(dff['started_at']>=start) & (dff['started_at']<=end)
    
    df = dff.loc[dffiltered]
    
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    
    # Calculations for Length of ride LOR
    df['LOR']=df['ended_at']-df['started_at']
    
    df['LOR']=df['LOR'] / np.timedelta64(1, 's')
    
    df['Weekday']=df['started_at'].dt.dayofweek
    
    """REMOVE RECORDS HAVING NEGATIVE LENGTH OF RIDE"""
    df=df[df['LOR']>=0]
    
    """REMOVE NULL DATA"""
    df=df.dropna(how = 'all')
    
    return df


# Dash framework
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div(children=[
    html.H1(children='Case Study'),
    html.Div([
        html.Div([
            html.H2(children='''
        How does a bike-share navigate speedy success
    '''),
            ],className="eight columns"),
    html.Div([
        html.P('Select start and end dates:'),#Fiter button button for date range
        dcc.DatePickerRange(
            id='my_date_picker',
            day_size=60,
            display_format='Do MMM YYYY',
            min_date_allowed=dte(2020, 4, 1),
            max_date_allowed=dte(2021, 3, 31),
            end_date=dte(2021, 4, 1),
            start_date=dte(2020, 3, 31)
        )
        ],  style={'display':'inline-block','marginLeft':'5px'},
          className="four columns"),
        ],className="row"),
    html.Hr(),
    
        dcc.Loading(id='loading-component',fullscreen =True,
                                children=[html.Div(
                                    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(
                id='pie-graph',
                # figure=fig
    ),
                ],className="six columns"),
              html.Div([
                  html.Br(),
                      dash_table.DataTable(
            id='table',
            # columns=[{"name": i, "id": i} for i in df2.columns],
            # data=df2.to_dict('records'),
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'textAlign': 'justify'
            },
            style_cell_conditional=[{'if': {'column_id': c},
                                     'textAlign': 'left'} for c in ['Member/Casual Riders']],
        ),
        html.Hr(),],className="six columns"),
               html.Div(
                   id='markdown-text',className="six columns"),
            ],className="row"),
        html.Div([
            dcc.Graph(
        id='timeseres-graph',
        # figure=fig1
            ),
            ]),
        html.Div([
            dcc.Graph(
        id='days-bar-graph',
        # figure=fig2
            ),
            ]),
        html.Div([
            dcc.Graph(
        id='lor-bar-graph',
        # figure=fig3
        ),
            ]),
        html.Div([
            dcc.Graph(
        id='hour-bar-graph',
        # figure=fig3
        ),
            ]),
        html.Div([
            dcc.Graph(
        id='station-bar-graph',
        # figure=fig4
        )
            ]),
        html.Div([
            dcc.Graph(
        id='stationmap-bar-graph',
        # figure=fig4
        )
            ]),
        html.Div([
            dcc.Graph(
        id='stationmap-bar-graph1',
        # figure=fig4
        )
            ]),
        html.Div([
            dcc.Graph(
        id='rideabletype-bar-graph',
        # figure=fig4
        )
            ]),
        ])
        )])
])

# =============================================================================
# Callbacks for the application
# =============================================================================

@app.callback(
        [Output('pie-graph', 'figure'),
          Output('table', 'data'),
          Output('table', 'columns'),
          Output('markdown-text', 'children'),
          Output('timeseres-graph', 'figure'),
          Output('days-bar-graph', 'figure'),
          Output('lor-bar-graph', 'figure'),
          Output('hour-bar-graph', 'figure'),
          Output('station-bar-graph', 'figure'),
          Output('stationmap-bar-graph', 'figure'),
          Output('stationmap-bar-graph1', 'figure'),
          Output('rideabletype-bar-graph', 'figure')],
        [Input('my_date_picker', 'start_date'),
          Input('my_date_picker', 'end_date')])

def update_dashboard(start_date,end_date):
    df=df_cleaned(start_date,end_date)
    df['started_date']=df['started_at'].dt.strftime("%b %Y")
    df['ended_date']=df['ended_at'].dt.strftime("%b %Y")
    df['started_hour']=df['started_at'].dt.hour
    df['started_at']=df['started_at'].dt.date
    df=df.rename(columns = {'ride_id':'Total Rides','member_casual':'Member/Casual Riders', 'LOR':'Length of Ride'}, inplace = False)
    # A markwon text for bulletin points
    card = dcc.Markdown('''
    >* **Total {:,} Rides**
    >* **Mean Length of ride:      {}**
    >* **Mode Length of ride:      {}**
    >* **Max Length of ride:       {}**
    '''.format(df['Total Rides'].count(),converttimehhmmss(df['Length of Ride'].mean()),converttimehhmmss(df['Length of Ride'].mode().values[0]),converttimehhmmss(df['Length of Ride'].max())),
    style={"white-space": "pre"}
    )  
    df1=pd.DataFrame(df,columns=('Total Rides','Weekday','started_at','Member/Casual Riders', 'Length of Ride'))
    df1=df1.groupby(['Member/Casual Riders','started_at','Weekday'],as_index=False).agg({'Total Rides':'count','Length of Ride':'mean'})
    df1=df1.rename(columns = {'Total Rides':'Total Rides','Member/Casual Riders':'Member/Casual Riders', 'Length of Ride':'Length of Ride'}, inplace = False)
    
    # PIE CHART, TITLE='Total Members Vs Casual Riders'
    fig = px.pie(df1, values='Total Rides', names='Member/Casual Riders', title='Total Members Vs Casual Riders')
     # LINE CHART, Time series for total rides taken by casual riders and members
    fig1 = px.line(df1, x='started_at', y='Total Rides', color='Member/Casual Riders')
    
    # to add filers and range to the line chart
    fig1.update_layout(xaxis=dict(
        rangeselector=dict(
                buttons=list([
                    dict(count=1,
                          label="1m",
                          step="month",
                          stepmode="backward"),
                    dict(count=6,
                          label="6m",
                          step="month",
                          stepmode="backward"),
                    dict(count=1,
                          label="YTD",
                          step="year",
                          stepmode="todate"),
                    dict(count=1,
                          label="1y",
                          step="year",
                          stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ))
    df['Maximum Length of Ride']=df['Length of Ride']
    df2=pd.DataFrame(df,columns=('Total Rides','Member/Casual Riders', 'Length of Ride','Maximum Length of Ride'))
    df2=df2.groupby(['Member/Casual Riders'],as_index=False).agg({'Total Rides':'count','Length of Ride':'mean','Maximum Length of Ride':'max'})
    df2['Length of Ride']=(df2['Length of Ride'].apply(converttimehhmmss))
    df2['Maximum Length of Ride']=(df2['Maximum Length of Ride'].apply(converttimehhmmss))
    df2 = df2.rename(columns = {'Total Rides':'Total Rides','Member/Casual Riders':'Member/Casual Riders', 'Length of Ride':'Average Length of Ride'}, inplace = False)
    df2['Total Rides']=df2['Total Rides'].apply('{:,}'.format)
    
    df3=pd.DataFrame(df,columns=('Total Rides',"Weekday",'Member/Casual Riders', 'Length of Ride'))
    df3=df3.groupby(["Weekday",'Member/Casual Riders'],as_index=False).agg({'Total Rides':'count','Length of Ride':'mean'})
    df3['Weekday']=df3['Weekday'].replace([0,1,2,3,4,5,6],["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"])
    df3['Average Length of Ride in hrs']=df3['Length of Ride']/60
    # A bar chart for average length of ride by members and casual riders each weekday
    fig3 = px.bar(df3, x="Weekday", y="Average Length of Ride in hrs", color="Member/Casual Riders", title="Average Length of Ride each week day")
    
    # A bar chart for total rides by members and casual riders each weekday
    fig2 = px.bar(df3, x="Weekday", y="Total Rides", color="Member/Casual Riders", title="Total Members/Rider each day")
    
    startedhr_df=pd.DataFrame(df,columns=('Total Rides',"started_hour",'Member/Casual Riders'))
    startedhr_df=startedhr_df.groupby(["started_hour",'Member/Casual Riders'],as_index=False).agg({'Total Rides':'count'})
    # A bar chart for Top 10 busiest station
    fig_barplot = px.bar(startedhr_df, x="started_hour", y="Total Rides", color="Member/Casual Riders", title="Total Rides started",labels = {'started_hour':"Started Hour"})
    fig_barplot.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    fig_barplot.update_xaxes(tickvals=list(range(0,25)))
    
    
    
    df4=pd.DataFrame(df,columns=('Total Rides',"start_station_name",'Member/Casual Riders'))
    df4=df4.groupby(["start_station_name",'Member/Casual Riders'],as_index=False).agg({'Total Rides':'count'})
    df4 = df4.nlargest(11, "Total Rides")
    # A bar chart for Top 10 busiest station
    fig4 = px.bar(df4, x="start_station_name", y="Total Rides", color="Member/Casual Riders", title="Top 10 busiest station")
    fig4.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    
    df5=pd.DataFrame(df,columns=('Total Rides',"start_station_name","start_lat","start_lng",'Member/Casual Riders','started_date'))
    df5=df5.groupby(["start_lat","start_lng","start_station_name",'Member/Casual Riders','started_date'],as_index=False).agg({'Total Rides':'count'})
    df5['sort_started_date']=pd.to_datetime(df5['started_date'], format="%b %Y")
    df5=df5.sort_values(by=['sort_started_date'], ascending=True,ignore_index=True)
    fig5 = px.scatter_mapbox(df5, lat='start_lat',lon='start_lng', hover_name="start_station_name",color='Member/Casual Riders',zoom=10, height=600,animation_frame="started_date")
    fig5.update_layout(title = 'Geo Location of Riders from their start point', title_x=0.5,mapbox_style="open-street-map")
    
    df6=pd.DataFrame(df,columns=('Total Rides',"end_station_name","end_lat","end_lng",'Member/Casual Riders','ended_date'))
    df6=df6.dropna()
    df6=df6.groupby(["end_lat","end_lng","end_station_name",'Member/Casual Riders','ended_date'],as_index=False).agg({'Total Rides':'count'})
    df6['sort_ended_date']=pd.to_datetime(df6['ended_date'], format="%b %Y")
    df6=df6.sort_values(by=['sort_ended_date'], ascending=True,ignore_index=True)
    fig6 = px.scatter_mapbox(df6, lat='end_lat',lon='end_lng', hover_name="end_station_name",color='Member/Casual Riders',zoom=10, height=600,animation_frame="ended_date")
    fig6.update_layout(title = 'Geo Location of Riders from their end point', title_x=0.5,mapbox_style="open-street-map")
    
    df7=pd.DataFrame(df,columns=('Total Rides',"rideable_type",'Member/Casual Riders'))
    df7=df7.groupby(["rideable_type",'Member/Casual Riders'],as_index=False).agg({'Total Rides':'count'})
    fig7 = px.bar(df7, x="rideable_type", y="Total Rides",
             color='Member/Casual Riders', barmode='group',
             height=400)
    
    
    return fig,df2.to_dict('records'),[{"name": i, "id": i} for i in df2.columns],card,fig1,fig2,fig3,fig_barplot,fig4,fig5,fig6,fig7
                    
if __name__ == '__main__':
    app.run_server()
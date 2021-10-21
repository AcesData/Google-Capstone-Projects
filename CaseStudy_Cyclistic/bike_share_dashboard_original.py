# Read the library
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from datetime import timedelta
import dash_bootstrap_components as dbc
import dash_table


def converttimehhmmss(sec):
    hhmmss=str(timedelta(seconds=sec))
    return hhmmss

def read_data():
    df1=pd.read_csv('Docs/202004-divvy-tripdata.csv')
    df=df1
    # df2=pd.read_csv('Docs/202005-divvy-tripdata.csv')
    # df3=pd.read_csv('Docs/202006-divvy-tripdata.csv')
    # df4=pd.read_csv('Docs/202007-divvy-tripdata.csv')
    # df5=pd.read_csv('Docs/202008-divvy-tripdata.csv')
    # df6=pd.read_csv('Docs/202009-divvy-tripdata.csv')
    # df7=pd.read_csv('Docs/202010-divvy-tripdata.csv')
    # df8=pd.read_csv('Docs/202011-divvy-tripdata.csv')
    # df9=pd.read_csv('Docs/202012-divvy-tripdata.csv')
    # df10=pd.read_csv('Docs/202101-divvy-tripdata.csv')
    # df11=pd.read_csv('Docs/202102-divvy-tripdata.csv')
    # df12=pd.read_csv('Docs/6666666666666666666666666666666666666666666666666699999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999202103-divvy-tripdata.csv')
    # df=df1.append([df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12])
    return df

df=read_data()

df['started_at'] = pd.to_datetime(df['started_at'])

df['ended_at'] = pd.to_datetime(df['ended_at'])

# Calcluations for Length of ride LOR
df['LOR']=df['ended_at']-df['started_at']

df['LOR']=df['LOR'] / np.timedelta64(1, 's')

df['Weekday']=df['started_at'].dt.dayofweek
df=df[df['LOR']>=0]
df=df.dropna()

df['started_at']=df['started_at'].dt.date
df['count']=1

df=df.rename(columns = {'ride_id':'Total Rides','member_casual':'Member/Casual Riders', 'LOR':'Length of Ride'}, inplace = False)
df1=pd.DataFrame(df,columns=('Total Rides','Weekday','started_at','Member/Casual Riders', 'Length of Ride'))
df1=df1.groupby(['Member/Casual Riders','started_at','Weekday'],as_index=False).agg({'Total Rides':'count','Length of Ride':'mean'})
df1=df1.rename(columns = {'Total Rides':'Total Rides','Member/Casual Riders':'Member/Casual Riders', 'Length of Ride':'Length of Ride'}, inplace = False)
fig = px.pie(df1, values='Total Rides', names='Member/Casual Riders', title='Total Members Vs Casual Riders')
fig.show()

fig1 = px.line(df1, x='started_at', y='Total Rides', color='Member/Casual Riders')

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
fig1.show()



# card = dbc.Card(
#     dbc.ListGroup(
#         [
#             dbc.ListGroupItem("Mean Length of ride: {}".format(converttimehhmmss(df['Length of Ride'].mean()))),
#             dbc.ListGroupItem("Mode Length of ride: {}".format(converttimehhmmss(df['Length of Ride'].mode().values[0]))),
#             dbc.ListGroupItem("Max Length of ride: {}".format(converttimehhmmss(df['Length of Ride'].max()))),
#         ],
#         flush=True,
#     ),
#     style={"width": "auto"},
# )
card = dcc.Markdown('''
>* **Total {:,} Rides**
>* **Mean Length of ride:      {}**
>* **Mode Length of ride:      {}**
>* **Max Length of ride:       {}**
'''.format(df['Total Rides'].count(),converttimehhmmss(df['Length of Ride'].mean()),converttimehhmmss(df['Length of Ride'].mode().values[0]),converttimehhmmss(df['Length of Ride'].max())),
style={"white-space": "pre"}
)

df1=df1.groupby(['Member/Casual Riders','Weekday'],as_index=False).agg({'Total Rides':'sum','Length of Ride':'mean'})

df1['Weekday']=df1['Weekday'].replace([0,1,2,3,4,5,6],["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"])

fig2 = px.bar(df1, x="Weekday", y="Total Rides", color="Member/Casual Riders", title="Total Rides each day")



df['Maximum Length of Ride']=df['Length of Ride']

df2=pd.DataFrame(df,columns=('Total Rides','Member/Casual Riders', 'Length of Ride','Maximum Length of Ride'))
df2=df2.groupby(['Member/Casual Riders'],as_index=False).agg({'Total Rides':'count','Length of Ride':'mean','Maximum Length of Ride':'max'})
df2['Length of Ride']=(df2['Length of Ride'].apply(converttimehhmmss))
df2['Maximum Length of Ride']=(df2['Maximum Length of Ride'].apply(converttimehhmmss))
df2 = df2.rename(columns = {'Total Rides':'Total Rides','Member/Casual Riders':'Member/Casual Riders', 'Length of Ride':'Average Length of Ride'}, inplace = False)
df2['Total Rides']=df2['Total Rides'].apply('{:,}'.format)

df3=pd.DataFrame(df,columns=("Weekday",'Member/Casual Riders', 'Length of Ride'))
df3=df3.groupby(["Weekday",'Member/Casual Riders'],as_index=False).agg({'Length of Ride':'mean'})
df3['Weekday']=df3['Weekday'].replace([0,1,2,3,4,5,6],["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"])
df3['Average Length of Ride in hrs']=df3['Length of Ride']/60
fig3 = px.bar(df3, x="Weekday", y="Average Length of Ride in hrs", color="Member/Casual Riders", title="Average Length of Ride each week day <br><sup>Plot Subtitle</sup>",
              labels = {'Weekday':"Weekday<br><sup>Subtitle</sup>"})
              # 'Average Length of Ride in hrs':'count'})
# fig3.add_annotation(#x=4, y=4,
#             text="Text annotation without arrow",
#             showarrow=False,
#             yshift=10)


# Develop a Plotly Dash Application

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div(children=[
    html.H1(children='Case Study'),

    html.H2(children='''
        How does a bike-share navigate speedy success
    '''),
    html.Hr(),
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(
                id='example-graph',
                figure=fig
    ),
                ],className="six columns"),
             html.Div([
                 html.Br(),
                     dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df2.columns],
            data=df2.to_dict('records'),
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'textAlign': 'justify'
            },
        )],className="six columns"),
             html.Div([
                 html.Hr(),
             card
             ],className="six columns"),
            ],className="row"),
        dcc.Graph(
        id='timeseres-graph',
        figure=fig1
    ),
         dcc.Graph(
        id='days-bar-graph',
        figure=fig2
    ),
         dcc.Graph(
        id='lor-bar-graph',
        figure=fig3
    )
         ])
          # ],className='ten columns offset-by-one')
])

if __name__ == '__main__':
    app.run_server()
# df.shape
# Out[8]: (3489748, 13)
# df.isnull().sum()
# df.isnull().sum()*100/df.shape[0]

# Out[11]: 
# Total Rides                    0
# rideable_type              0
# started_at                 0
# ended_at                   0
# start_station_name    122175
# start_station_id      122801
# end_station_name      143242
# end_station_id        143703
# start_lat                  0
# start_lng                  0
# end_lat                 4738
# end_lng                 4738
# Member/Casual Riders              0
# dtype: int64
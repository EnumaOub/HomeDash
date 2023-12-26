from dashboard.index import app
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import text
import datetime

from dashboard.database.database import db_session, init_db, engine
from dashboard.functions.speed_internet import run_test
from dashboard.graph_param.plot_data import graph_param

run_test(1)

fig = go.Figure()




app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    dcc.Graph(figure=fig, 
            id='live-update-graph', 
            animate=True),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )

])



# Multiple components can update everytime interval gets fired.
@callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    with engine.connect() as db:
        con_data = pd.read_sql(text("""SELECT testtime, ul, dl FROM public.sp_con"""), db)
    con_data["testtime"] =  pd.to_datetime(con_data["testtime"])
    con_data["ul"] = con_data["ul"].astype(float).round(2) 
    con_data["dl"] = con_data["dl"].astype(float).round(2) 

    if n==0:
        fig.add_trace(go.Scatter(x=con_data["testtime"], y=con_data["ul"], 
                   name="Upload", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=con_data["testtime"], y=con_data["dl"], 
                    name="Download", mode="lines+markers"))
        fig.update_layout(
                title="Connection Speed",
                xaxis_title="Timestamp []",
                yaxis_title="Speed [MB/s]",
            )
        now = datetime.datetime.now()
        day_start = datetime.datetime(now.year,now.month,now.day)
        day_end = day_start + datetime.timedelta(hours=24)
        day_start = str(day_start.strftime('%Y-%m-%d'))
        day_end = str(day_end.strftime('%Y-%m-%d'))


        fig.update_xaxes(
            range=[day_start, day_end]
        )
        graph_param(fig, slider=True)
        return fig
    else:
        traces = list()
        traces.append(plotly.graph_objs.Scatter(
            x=con_data["testtime"], 
            y=con_data["ul"], 
            name="Upload", 
            mode="lines+markers"
            ))
        traces.append(plotly.graph_objs.Scatter(
            x=con_data["testtime"], 
            y=con_data["dl"], 
            name="Download", 
            mode="lines+markers"
            ))
        return {'data': traces}



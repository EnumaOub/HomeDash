from dashboard.index import app
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import text

from dashboard.database.database import db_session, init_db, engine
from dashboard.functions.speed_internet import run_test
from dashboard.graph_param.plot_data import graph_param

run_test(1)


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    dcc.Graph(id='live-update-graph'),
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

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=con_data["testtime"], y=con_data["ul"], 
                   name="Upload", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=con_data["testtime"], y=con_data["dl"], 
                   name="Download", mode="lines+markers"))
    
    fig.update_layout(
        title="Connection Speed",
        xaxis_title="Timestamp []",
        yaxis_title="Speed [MB/s]",
    )
    graph_param(fig, slider=True)

    return fig


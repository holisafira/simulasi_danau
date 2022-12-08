#import semua modules
import numpy as np
import dash
from dash import dcc, html, Output, Input, State
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# from main import *

#inisiasi aplikasi
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


#membaca file
sheet_inflow = "inflow"
sheet_outflow = "outflow"
url_inflow = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRsxRP6lGuCaWHEZ8Ouhgol0e5fLVTXaApbpb646oNyAI_KRmpZWSI14c7_iHZkn6FD_hrw7unb6ZRI/pub?output=csv&sheet={sheet_inflow}"
url_outflow = url="https://docs.google.com/spreadsheets/d/e/2PACX-1vTUJjwNCRuvaEYhPaXUyKnq47Dh11NuXAKwAnlPYjTPktm68yI3wweTKfZF4nPCofZsiFA6MtC1eUeY/pub?output=csv&sheet={sheet_outflow}"
df_inflow = pd.read_csv(url_inflow)
df_outflow = pd.read_csv(url_outflow)


#membangun komponen
header = html.H1("Aplikasi Simulasi Kapasitas Embung B ITERA", style={'textAlign': 'center', "height":"100 px", "background-color":"lightblue"})
subtitle = html.H5("Tugas Besar Kapita Selekta Matematika Komputasi (KELOMPOK 3)", style={'textAlign': 'center', "height":"3 px", "background-color":"pink"})
footer = html.Div([html.H1("Institut Teknologi Sumatera"),html.H5("Jl. Terusan Ryacudu, Way Huwi, Kec. Jati Agung, Kabupaten Lampung Selatan, Lampung 35365"), html.P("Zessica Nainggolan | Christina Jheovani| Ayumi Rima| Alviolita Br.Barus | Yanti Marito| Holi Safira| Jesika Ginting"), html.P("created @ 2022 by|072|")], style={'textAlign': 'center', "height":"3 px", "background-color":"lightblue"})
inflow_fig = go.FigureWidget()
inflow_fig.add_scatter(name='Inflow', x=df_inflow['Bulan'], y=df_inflow['Data-masuk'])
inflow_fig.layout.title = 'Plot Air Yang Masuk'

outflow_fig = go.FigureWidget()
outflow_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'], y=df_outflow['Data-keluar'])
outflow_fig.layout.title = 'Plot Air Yang Keluar'

simulation_fig = go.FigureWidget()
# simulation_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'], y=df_outflow['Data'])
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header, subtitle]),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=inflow_fig)]), 
                dbc.Col([dcc.Graph(figure=outflow_fig)])
            ]
            ),
        html.Div(
            [
                html.Button('Run', id='run-button', n_clicks=0)
            ],
            style = {'textAlign': 'center'}
        ), 
        html.Div(id='output-container-button', children='Klik run untuk menjalankan simulasi.', style = {'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='simulation-result', figure=simulation_fig)])
            ]
        )
    ]
    
)

#interaksi aplikasi
@app.callback(
    Output(component_id='simulation-result', component_property='figure'),
    Input('run-button', 'n_clicks')
)


def graph_update(n_clicks):
    # filtering based on the slide and dropdown selection
    if n_clicks >=1:
        #program numerik ---start----
        inout = df_inflow["Data-masuk"].values - df_outflow["Data-keluar"].values
        N = len(inout)
        u = np.zeros
        u0 = 1000
        u[0] = u0
        dt = 1

        #metode Euler
        for n in range(N-1):
            u[n + 1] = u[n] + dt*inout[n]
        #program numerik ---end----


        # the figure/plot created using the data filtered above 
        simulation_fig = go.FigureWidget()
        simulation_fig.add_scatter(name='Simulation', x=df_outflow['Bulan'], y=u)
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig
    else:
        simulation_fig = go.FigureWidget()
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig

    


#jalankan aplikasi
if __name__ == 'main':
    app.run_server()

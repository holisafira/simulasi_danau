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
air_masuk1 = "Chart Inflow"

air_keluar1 = "Chart Outflow "

url_inflow = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYoKHjEZXebGM5XmdFISl6HPF94Hzc2jmjPrZ5vezZKABR-zufsHl200oCIQ8YSimWAQ2YO3sveSx5/pub?output=csv&sheet={sheet_inflow}"
url_outflow = url="https://docs.google.com/spreadsheets/d/e/2PACX-1vSmeDzdp9GxDilIQfwBPfLXPnSn307C-YWVSrCIxSuAaW4R3bR0QbaAxg3SVEB69TJfxmvetzuOEj0y/pub?output=csv&sheet={sheet_outflow}"


df_masuk = pd.read_csv(url_inflow)
df_keluar = pd.read_csv(url_outflow)



#membangun komponen
header = html.H1("Aplikasi Simulasi Kapasitas Embung B ITERA", style={'textAlign': 'center', "height":"100 px", "background-color":"lightblue"})
subtitle = html.H5("Tugas Besar Kapita Selekta Matematika Komputasi (KELOMPOK 3)", style={'textAlign': 'center', "height":"3 px", "background-color":"pink"})
footer = html.Div([html.H1("Institut Teknologi Sumatera"),html.H5("Jl. Terusan Ryacudu, Way Huwi, Kec. Jati Agung, Kabupaten Lampung Selatan, Lampung 35365"), html.P("Zessica Nainggolan | Christina Jheovani| Ayumi Rima| Alviolita Br.Barus | Yanti Marito| Holi Safira| Jesika Ginting"), html.P("created @ 2022 by|072|")], style={'textAlign': 'center', "height":"3 px", "background-color":"lightblue"})

chart_masuk= go.FigureWidget()
chart_masuk.add_bar(name="Chart Inflow", x=df_masuk['Bulan'], y=df_masuk['Data-masuk'] )
chart_masuk.layout.title = 'Chart Inflow Embung B'

chart_keluar = go.FigureWidget()
chart_keluar.add_scatter(name="Outflow " , x=df_keluar['Bulan'], y=df_keluar['Data-keluar'])
chart_keluar.layout.title = 'Chart Outflow Embung B'

simulation_fig = go.FigureWidget()
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header, subtitle])  ,
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=chart_masuk)] ),
               
            ]
            ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=chart_keluar)]),
                
            ]
            ),
        html.Div(
            [
                dbc.Button('Run', color="primary",id='run-button', n_clicks=0)
            ],style = {'textAlign': 'center'})
        , 
        html.Div(id='output-container-button', children='Klik Run untuk menjalankan simulasi.', style = {'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='simulation-result', figure=simulation_fig)])
            ]
        ), footer
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
        inout1 =  (df_masuk['Data-masuk'].values - df_keluar['Data-keluar'].values)
        N = len(inout1)
        u = np.zeros(N)
        u0 = 19600
        u[0] = u0
        dt = 1

        #metode Euler
        for n in range(N-1):
            u[n + 1] = u[n] + dt*inout1[n] 
        #program numerik ---end----


        # the figure/plot created using the data filtered above 
        simulation_fig = go.FigureWidget()
        simulation_fig.add_scatter(name='Simulation', x=df_keluar['Bulan'], y=u)
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig
    else:
        simulation_fig = go.FigureWidget()
        simulation_fig.layout.title = 'Simulasi Kapasitas Embung B ITERA '

        return simulation_fig


#jalankan aplikasi
if __name__=='__main__':
    app.run_server(debug=True, port=2022)





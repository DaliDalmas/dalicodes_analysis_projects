import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import request

from app import server
from app import app


app.title='Digest Africa Analytics'
#server = app.server
# import all pages in the app
from apps import mps, home




structuredDropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Ugandan Mps 2020", href="/mps")
    ],
    nav = True,
    in_navbar = True,
    label = "set one",
)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/favicon-for-white.png", height="50px", width="120px")),
                        dbc.Col(dbc.NavbarBrand("DALICODES ANALYTICS", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=False,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [structuredDropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/mps':
        return mps.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)
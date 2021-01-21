import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px
import dash_table

data = pd.read_csv("mps.csv")
data["DISTRICT"] = data["DISTRICT"].apply(lambda x:str(x).lower())
data["PARTY"] = data["PARTY"].apply(lambda x: str(x).split('/')[0])
data = data.dropna()

DISTRICTS = len(list(data["DISTRICT"].unique()))
data["COMMENT"] = data["COMMENT"].apply(lambda x:str(x).lower())
CONSTITUENCIES = len(list(data["CONSTITUENCY"][data["CONSTITUENCY"]!="WOMAN MP"].unique()))
WOMAN_MPS = len(list(data["CONSTITUENCY"][data["CONSTITUENCY"]=="WOMAN MP"]))
NEWMPS = len(list(data["COMMENT"][data["COMMENT"]=="new"]))
OLDMPS = len(list(data["COMMENT"][data["COMMENT"]=="old"]))

old_new_df = data[["CANDIDATE","COMMENT"]].groupby(["COMMENT"]).count().reset_index()
old_new = px.pie(old_new_df, values='CANDIDATE', names='COMMENT', title='Old vs new mps', hole=.5)

party_df = data[["PARTY","COMMENT","CANDIDATE"]].groupby(["PARTY","COMMENT"]).count().reset_index()
party_df = party_df.sort_values(by="COMMENT")
party = px.bar(party_df, x='PARTY', y='CANDIDATE',color="COMMENT", orientation='v')

region_df = data[["PARTY","CANDIDATE"]].groupby(["PARTY"]).count().reset_index()

datatable = dash_table.DataTable(
    id='table',
    columns =[{"name":i,"id":i} for i in data.columns],
    data = data.to_dict('records'),
    page_size=15,
    style_header={
        'backgroundColor':'black',
        'color':'white',
        'fontWeight':'bold'
    },
    style_data_conditional=[
        {'if':{'row_index':'odd'},
        'backgroundColor':'rbg(248,248,248)'}
    ]
)

print(data)
layout = html.Div([
    dbc.Container([
        
        dbc.Row([
            dbc.Col([
                dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Constituencies", className="card-title"),
                                html.H4(CONSTITUENCIES, className="card-title"),
                            ]
                        ),
                        className="w-80",
                        color="dark",
                        inverse=True
            )
                
            ]),
            dbc.Col([
                dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("New MPs", className="card-title"),
                                html.H4(NEWMPS, className="card-title"),
                            ]
                        ),
                        className="w-80",
                        color="dark",
                        inverse=True
            )
                
            ]),
            dbc.Col([
                dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Old MPs", className="card-title"),
                                html.H4(OLDMPS, className="card-title"),
                            ]
                        ),
                        className="w-80",
                        color="dark",
                        inverse=True
            )
                
            ]),
            dbc.Col([
                dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("WOMAN MPS", className="card-title"),
                                html.H4(WOMAN_MPS, className="card-title"),
                            ]
                        ),
                        className="w-80",
                        color="dark",
                        inverse=True
            )
                
            ]),
            dbc.Col([
                dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Districts", className="card-title"),
                                html.H4(DISTRICTS, className="card-title"),
                            ]
                        ),
                        className="w-80",
                        color="dark",
                        inverse=True
            )
                
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=old_new)
            ]),

            dbc.Col([
                dcc.Graph(figure=party)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                datatable
            ])
        ])
])
])

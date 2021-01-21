import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px
import dash_table
from app import app

#data retrieval
data = pd.read_csv("mps.csv")

#data cleaning
data["DISTRICT"] = data["DISTRICT"].apply(lambda x:str(x).lower())
data["PARTY"] = data["PARTY"].apply(lambda x: str(x).split('/')[0])
data = data.dropna()
data["COMMENT"] = data["COMMENT"].apply(lambda x:str(x).lower())

#transformations
regions = ["all"]+list(data["REGION"].unique())
districts = list(data["DISTRICT"].unique())

# drop downs
region_dropdown = dcc.Dropdown(
        id='regions-dropdown',
        options=[
            {'label': reg, 'value': reg} for reg in regions
            ],
        value="all"
    )
district_dropdown = dcc.Dropdown(
    id='districts-dropdown',
    options=[
        {'label': dist, 'value': dist} for dist in districts
    ],
    multi=True
) 

layout = html.Div([
    dbc.Container([
        
        dbc.Row([
            dbc.Col([
                dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Constituencies", className="card-title"),
                                html.H4(id='CONSTITUENCIES', className="card-title"),
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
                                html.H4(id='NEWMPS', className="card-title"),
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
                                html.H4(id = 'OLDMPS', className="card-title"),
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
                                html.H4(id='WOMAN_MPS', className="card-title"),
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
                                html.H4(id='DISTRICTS', className="card-title"),
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
                html.H4("", className="card-title"),
                html.H6("Regions", className="card-title"),
                region_dropdown
            ]),
            dbc.Col([
                html.H4("", className="card-title"),
                html.H6("Districts", className="card-title"),
                district_dropdown
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='old_new')
            ]),

            dbc.Col([
                dcc.Graph(id='party')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id='datatable')
            ])
        ])
])
])




@app.callback(
    Output('old_new', 'figure'),
    Input('regions-dropdown', 'value'))

def update_figure(region_value):
    condition = (region_value==None) or (region_value=='all')
    if condition:
        df = data
        old_new_df = df[["CANDIDATE","COMMENT"]].groupby(["COMMENT"]).count().reset_index()
        old_new = px.pie(old_new_df, values='CANDIDATE', names='COMMENT', title='Piechart comparing old and new mps.', hole=.5)
    else:
        df = data[data["REGION"]==region_value]
        old_new_df = df[["CANDIDATE","COMMENT"]].groupby(["COMMENT"]).count().reset_index()
        old_new = px.pie(old_new_df, values='CANDIDATE', names='COMMENT', title='Piechart comparing old and new mps.', hole=.5)

    return old_new


@app.callback(
    Output('party', 'figure'),
    Input('regions-dropdown', 'value'))

def update_figure(region_value):
    condition = (region_value==None) or (region_value=='all')
    if condition:
        df = data
        party_df = df[["PARTY","COMMENT","CANDIDATE"]].groupby(["PARTY","COMMENT"]).count().reset_index()
        party_df = party_df.sort_values(by="COMMENT")
        party = px.bar(party_df, x='PARTY', y='CANDIDATE',color="COMMENT", orientation='v',title='Mps by party split by comment.')
    else:
        df = data[data["REGION"]==region_value]
        party_df = df[["PARTY","COMMENT","CANDIDATE"]].groupby(["PARTY","COMMENT"]).count().reset_index()
        party_df = party_df.sort_values(by="COMMENT")
        party = px.bar(party_df, x='PARTY', y='CANDIDATE',color="COMMENT", orientation='v',title='Mps by party split by comment.')
    return party



@app.callback(
    Output('datatable', 'children'),
    Input('regions-dropdown', 'value'))

def update_figure(region_value):
    condition = (region_value==None) or (region_value=='all')
    if condition:
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
    else:
        df = data[data["REGION"]==region_value]
        datatable = dash_table.DataTable(
                        id='table',
                        columns =[{"name":i,"id":i} for i in df.columns],
                        data = df.to_dict('records'),
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
    return datatable


@app.callback(
    Output('CONSTITUENCIES', 'children'),
    Input('regions-dropdown', 'value'))

def update_figure(region_value):
    condition = (region_value==None) or (region_value=='all')
    if condition:
        df = data
        CONSTITUENCIES = len(list(df["CONSTITUENCY"][df["CONSTITUENCY"]!="WOMAN MP"].unique()))
    else:
        df = data[data["REGION"]==region_value]
        CONSTITUENCIES = len(list(df["CONSTITUENCY"][df["CONSTITUENCY"]!="WOMAN MP"].unique()))
    return CONSTITUENCIES


@app.callback(
    Output('NEWMPS', 'children'),
    Input('regions-dropdown', 'value'))

def update_figure(region_value):
    condition = (region_value==None) or (region_value=='all')
    if condition:
        df = data
        NEWMPS = len(list(df["COMMENT"][df["COMMENT"]=="new"]))
    else:
        df = data[data["REGION"]==region_value]
        NEWMPS = len(list(df["COMMENT"][df["COMMENT"]=="new"]))
    return NEWMPS



@app.callback(
    Output('OLDMPS', 'children'),
    Input('regions-dropdown', 'value'))

def update_figure(region_value):
    condition = (region_value==None) or (region_value=='all')
    if condition:
        df = data
        OLDMPS = len(list(df["COMMENT"][df["COMMENT"]=="old"]))
    else:
        df = data[data["REGION"]==region_value]
        OLDMPS = len(list(df["COMMENT"][df["COMMENT"]=="old"]))
    return OLDMPS



@app.callback(
    Output('WOMAN_MPS', 'children'),
    Input('regions-dropdown', 'value'))

def update_figure(region_value):
    condition = (region_value==None) or (region_value=='all')
    if condition:
        df = data
        WOMAN_MPS = len(list(df["CONSTITUENCY"][df["CONSTITUENCY"]=="WOMAN MP"]))
    else:
        df = data[data["REGION"]==region_value]
        WOMAN_MPS = len(list(df["CONSTITUENCY"][df["CONSTITUENCY"]=="WOMAN MP"]))
    return WOMAN_MPS



@app.callback(
    Output('DISTRICTS', 'children'),
    Input('regions-dropdown', 'value'),
    Input('districts-dropdown', 'value'))

def update_figure(region_value,district_values):
    print(district_values)
    condition = (region_value==None) or (region_value=='all')
    if condition:
        df = data
        DISTRICTS = len(list(df["DISTRICT"].unique()))
    else:
        df = data[data["REGION"]==region_value]
        DISTRICTS = len(list(df["DISTRICT"].unique()))
    return DISTRICTS
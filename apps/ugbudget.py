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
import plotly.graph_objects as go

#data retrieval
data = pd.read_csv("data/budget/all_budgets.csv")

vote = list(data.VoteName.unique())
vote = ['All']+vote
vote_dropdown = dcc.Dropdown(
                    id='vote-dropdown',
                    options=[{'label': v, 'value': v } for v in vote],
                    value= vote[0],
                    multi = True
                )

programme = list(data.ProgrammeName.unique())
programme = ['All']+programme
programme_dropdown = dcc.Dropdown(
                        id='programme-dropdown',
                        options=[{'label': p, 'value': p } for p in programme],
                        value= programme[0],
                        multi = True
                    )

SubProgram = list(data.SubProgramName.unique())
SubProgram = ['All']+SubProgram
SubProgram_dropdown = dcc.Dropdown(
                        id='subprogramme-dropdown',
                        options=[{'label': p, 'value': p } for p in SubProgram],
                        value= SubProgram[0],
                        multi = True
                    )

Classes = list(data.Class.unique())
Classes = ['All']+Classes[:-1]
Class_dropdown = dcc.Dropdown(
                        id='classes-dropdown',
                        options=[{'label': p, 'value': p } for p in Classes],
                        value= Classes[0],
                        multi = True
                    )

FinancialYear = list(data.FinancialYear.unique())
FinancialYear = ['All']+FinancialYear[:-1]
FinancialYear_dropdown = dcc.Dropdown(
                        id='classes-dropdown',
                        options=[{'label': p, 'value': p } for p in FinancialYear],
                        value= FinancialYear[0],
                        multi = True
                    )
fund_type_amount = data[['FundType','Amount']].groupby(['FundType']).sum().reset_index()
fund_type_amount = fund_type_amount.sort_values(by='Amount')
fund_type_amount_fig = px.bar(fund_type_amount, y='FundType', x='Amount',orientation='h',color='Amount')

year_amount = data[['FinancialYear','Amount']].groupby(['FinancialYear']).sum().reset_index()
year_amount = year_amount.sort_values(by='Amount')
year_amount_fig = px.bar(year_amount, x='FinancialYear', y='Amount',color='Amount')

sector_amount = data[['SectorName','Amount']].groupby(['SectorName']).sum().reset_index()
sector_amount = sector_amount.sort_values(by='Amount')
sector_amount_fig = px.bar(sector_amount, x='SectorName', y='Amount',orientation='v',color='Amount')
sector_amount_fig.update_layout(
    height=700
)

gauge_height = 280
gauge_axis_range = 60000000000000
gauge_threshold = 55000000000000
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = year_amount['Amount'][year_amount['FinancialYear']=='18-19'].values[0],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "2018-2019"},
    gauge = {'axis': {'range': [None, gauge_axis_range]},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': gauge_threshold}}
    ))
fig.update_layout(paper_bgcolor = "#DCBDCF", font = {'color': "darkblue", 'family': "Arial"},height = gauge_height)

fig2 = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = year_amount['Amount'][year_amount['FinancialYear']=='19-20'].values[0],
    mode = "gauge+number+delta",
    title = {'text': "2019-2020"},
    delta = {'reference': year_amount['Amount'][year_amount['FinancialYear']=='18-19'].values[0]},
    gauge = {'axis': {'range': [None, gauge_axis_range]},
             'steps' : [
                 {'range': [0, 250], 'color': "lightgray"},
                 {'range': [250, 400], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': gauge_threshold}}))

fig2.update_layout(paper_bgcolor = "#F6B656", font = {'color': "darkblue", 'family': "Arial"},height = gauge_height)

fig3 = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = year_amount['Amount'][year_amount['FinancialYear']=='20-21'].values[0],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "2020-2021", 'font': {'size': 24}},
    delta = {'reference': year_amount['Amount'][year_amount['FinancialYear']=='19-20'].values[0], 
                'increasing': {'color': "RebeccaPurple"}},
    gauge = {
        'axis': {'range': [None, gauge_axis_range], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, year_amount['Amount'][year_amount['FinancialYear']=='18-19'].values[0]], 'color': 'cyan'},
            {'range': [year_amount['Amount'][year_amount['FinancialYear']=='18-19'].values[0],
            year_amount['Amount'][year_amount['FinancialYear']=='19-20'].values[0]], 'color': 'orange'},
            {'range': [year_amount['Amount'][year_amount['FinancialYear']=='19-20'].values[0],
             year_amount['Amount'][year_amount['FinancialYear']=='20-21'].values[0]], 'color': 'red'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': gauge_threshold}}))

fig3.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"},height = gauge_height)

df = data.drop(['SubProgramName', 'KeyOutputDescription', 'Description','FundType'],axis=1)
table = dash_table.DataTable(
                    id='table',
                    columns =[{"name":i,"id":i} for i in df.columns],
                    data = df.to_dict('records'),
                    page_size=20,
                    style_cell=dict(textAlign='left'),
                    style_header=dict(backgroundColor="paleturquoise"),
                    style_data=dict(backgroundColor="white")
                )

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3('Ugandan budgets')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig)
            ]),
            dbc.Col([
                dcc.Graph(figure=fig2)
            ]),
            dbc.Col([
                dcc.Graph(figure=fig3)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H1('')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Vote'),
                vote_dropdown
            ]),
            dbc.Col([
                html.H5('Programme'),
                programme_dropdown
            ]),
            dbc.Col([
                html.H5('Sub-Programme'),
                SubProgram_dropdown
            ]),
            dbc.Col([
                html.H5('Classes'),
                Class_dropdown
            ]),
            dbc.Col([
                html.H5('Financial year'),
                FinancialYear_dropdown
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=year_amount_fig)
            ]),
            dbc.Col([
                dcc.Graph(figure=fund_type_amount_fig)
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=sector_amount_fig)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                table
            ])
        ])
    ])
])
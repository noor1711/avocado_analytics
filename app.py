import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("avocado.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

# FIG 4
avocado = data
avocado = avocado[~(avocado.region == 'TotalUS')]
total = []
for region in np.unique(avocado.region):
    total.append([region, sum(avocado[avocado.region == region]['Total Volume'])])
total.sort(key= lambda x: x[1])
top_10 = total[-10:]
sum_ = sum(list(map(lambda x: x[1], total)))
rest = ((sum_ - sum(list(map(lambda x: x[1], top_10)))) / sum_) * 100
for i in range(len(top_10)):
    top_10[i][1] /= sum_
    top_10[i][1] *= 100

chart = [* top_10,['Rest', rest]]
labels = list(map(lambda x: x[0], chart))
values = list(map(lambda x: x[1], chart))
states = go.Figure(data=[go.Pie(labels=labels, values=values)])
chart = pd.DataFrame(chart, columns=['region', 'total_volume'])
states = px.pie(chart, values='total_volume', names='region', title='Avocado\'s by state', color_discrete_sequence=px.colors.sequential.RdBu)

# Fig 5, Organic Vs Conventional
filtered = data[data.region == "TotalUS"]
avocado_types = px.pie(filtered, values='Total Volume', names='type', title='Conventional sales Vs Organice Sales', color_discrete_sequence=px.colors.sequential.RdBu)



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Submitted by -  Noor Nimrat,  101903591, COE-23 "
                            "Analyzing and Comparing " 
                            " the sales of avocados in the US" 
                            " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": avocado_type, "value": avocado_type}
                                for avocado_type in data.type.unique()
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region1",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region2",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type2",
                            options=[
                                {"label": avocado_type, "value": avocado_type}
                                for avocado_type in data.type.unique()
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu2",
        ),



        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="compare-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(figure=states),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(figure=avocado_types),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure"), Output("compare-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("region1", "value"),
        Input("region2", "value"),
        Input("type2", "value")
    ],
)
def update_charts(region, avocado_type, start_date, end_date, r_one, r_two, type_two):
    mask = (
        (data.region == region)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    mask2  = (
        ((data.region == r_one) | (data.region == r_two))
        & (data.type == type_two)
    )
    filtered_2 = data.loc[mask2,:]

    compare_chart_figure = px.line(filtered_2, x="Date", y="Total Volume", color="region", title=str(r_one) + ' vs ' + str(r_two),template="simple_white", color_discrete_sequence=px.colors.sequential.Darkmint)
    compare_chart_figure.update_yaxes(visible=False, showticklabels=True)
    return price_chart_figure, volume_chart_figure, compare_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import yfinance as yf
import requests_cache

session = requests_cache.CachedSession('yfinance.cache')
app = Dash(external_stylesheets=[dbc.themes.CYBORG])

LOGO = 'data:image/png;base64,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'


def create_ticker_options():
    ticker_data = pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[2]
    stock_symbols = ticker_data['Symbol'].to_list()
    tickers = [ticker + '.NS' for ticker in stock_symbols]
    ticker_options = []

    for t in zip(ticker_data['Symbol'].to_list(), tickers):
        ticker_options.append({'label': t[0], 'value': t[1]})
    return stock_symbols, tickers, ticker_options


def fetch_data(ticker, period='1y'):
    data = yf.Ticker(ticker, session=session)
    hist_data = data.history(period=period)
    return hist_data


def fetch_ticker_heading(ticker):
    data = yf.Ticker(ticker, session=session)
    return data.info['longName']


def fetch_ticker_summary(ticker):
    data = yf.Ticker(ticker, session=session)
    return data.info['longBusinessSummary']


stock_symbols, tickers, stock_data_options = create_ticker_options()

# add callback for toggling the collapse on small screens


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("search-dropdown", "options"),
    Input("search-dropdown", "search_value")
)
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in stock_data_options if search_value.lower() in o["label"].lower()]


@app.callback(
    Output('ticker-heading', 'children'),
    Input('search-dropdown', 'value')
)
def update_ticker_heading(value):
    if not value:
        raise PreventUpdate
    heading = fetch_ticker_heading(value)
    return heading


@app.callback(
    Output('company-summary', 'children'),
    Input('search-dropdown', 'value')
)
def update_company_summary(value):
    if not value:
        raise PreventUpdate
    summary = fetch_ticker_summary(value)
    return summary


@app.callback(
    Output('company-data', 'children'),
    Input('search-dropdown', 'value')
)
def update_company_data(value):
    if not value:
        raise PreventUpdate
    data = yf.Ticker(value, session=session).info

    row1 = html.Tr([html.Td("Current Price"),
                   html.Td(f"₹ {data['currentPrice']}")])
    row2 = html.Tr([html.Td("Market Cap"), html.Td(
        f"₹ {data['marketCap'] // 10**7} Cr.")])
    row3 = html.Tr(
        [html.Td("52 Week High"), html.Td(f"₹ {data['fiftyTwoWeekHigh']}")])
    row4 = html.Tr([html.Td("52 Week Low"), html.Td(
        f"₹ {data['fiftyTwoWeekLow']}")])

    table_body = [html.Tbody([row1, row2, row3, row4])]
    return table_body


@app.callback(
    Output('company-ratios', 'children'),
    Input('search-dropdown', 'value')
)
def update_company_ratios(value):
    if not value:
        raise PreventUpdate
    data = yf.Ticker(value, session=session).info

    row1 = html.Tr(
        [html.Td("Stock P/E"), html.Td(np.round(data['trailingPE'], 2))])
    row2 = html.Tr([html.Td("ROE"), html.Td(
        f"{data['returnOnEquity'] * 100:.2f} %")])
    row3 = html.Tr([html.Td("Dividend Yield"), html.Td(
        f"{data['dividendYield'] * 100:.2f} %")])
    row4 = html.Tr([html.Td("Beta"), html.Td(np.round(data['beta'], 2))])

    table_body = [html.Tbody([row1, row2, row3, row4])]
    return table_body


@ app.callback(
    Output('price-time-graph', 'figure'),
    Input('search-dropdown', 'value'),
    Input('duration-tabs', 'value'),
    Input('moving-average-list', 'value')
)
def update_time_series_graph(search_value, duration_value, moving_average_values):
    if not search_value:
        raise PreventUpdate
    if search_value not in tickers:
        raise PreventUpdate
    ticker_data = fetch_data(ticker=search_value, period=duration_value)

    data_plot = ['Close']

    if(moving_average_values is not None):
        for moving_average in moving_average_values:
            ticker_data[f'{moving_average}DMA'] = ticker_data['Close'].rolling(
                window=moving_average).mean()
            data_plot.append(f'{moving_average}DMA')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=ticker_data.index,
                  y=ticker_data['Close'], name='Price'))
    if '50DMA' in data_plot:
        fig.add_trace(go.Scatter(x=ticker_data.index,
                      y=ticker_data['50DMA'], name='50DMA'))
    if '100DMA' in data_plot:
        fig.add_trace(go.Scatter(x=ticker_data.index,
                      y=ticker_data['100DMA'], name='100DMA'))
    if '200DMA' in data_plot:
        fig.add_trace(go.Scatter(x=ticker_data.index,
                      y=ticker_data['200DMA'], name='200DMA'))

    fig.update_layout(template='plotly_dark')
    return fig


search_dropdown = dcc.Dropdown(
    id='search-dropdown', style={'width': '250px'}, value=stock_data_options[0]['value'])

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Screener", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_dropdown,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
                style={'justify-content': 'flex-end'}
            ),
        ]
    ),
    color="dark",
    dark=True,
)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': '#282828'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

graph_card = dbc.Card(
    [
        dbc.CardHeader([
            dcc.Tabs([
                dcc.Tab(label='1m', value='1mo', style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(label='6m', value='6mo', style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(label='1Yr', value='1y', style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(label='3Yr', value='3y', style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(label='5Yr', value='5y', style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(label='Max', value='max', style=tab_style,
                        selected_style=tab_selected_style)
            ], id='duration-tabs', value='max')
        ]),
        dbc.CardBody(
            [
                dcc.Graph(id='price-time-graph')
            ]
        ),
        dbc.CardFooter([
            dcc.Checklist(
                options=[{'label': '50 DMA', 'value': 50},
                         {'label': '100 DMA', 'value': 100},
                         {'label': '200 DMA', 'value': 200}],
                inline=True,
                id='moving-average-list',
                labelStyle={'margin-right': '20px'},
                inputStyle={'margin-right': '4px'}
            ),
        ], style={'display': 'flex', 'justify-content': 'center'}),
    ],
    style={"margin": "25px", "padding": "24px"},
)


accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.P(id='company-summary', children="")
                ],
                title="About",
            )
        ],
        start_collapsed=True
    )
)

table_card = dbc.Card([
    dbc.CardHeader([
        html.H5(id="ticker-heading",
                className="card-title", children=""),
        accordion
    ]),
    dbc.CardBody([
        dbc.Table(id='company-data', children='',
                  bordered=True, striped=True,),
        dbc.Table(id='company-ratios', children='',
                  bordered=True, striped=True,)
    ], style={'display': 'flex'})
], style={"margin": "25px", "padding": "24px"})


app.layout = html.Div(id="parent", children=[
    navbar,
    html.H2(id="heading", children="Nifty 50 Dashboard",
            style={'text-align': 'center', 'margin-top': '8px'}),
    table_card,
    graph_card
])

if __name__ == '__main__':
    app.run_server(debug=True)

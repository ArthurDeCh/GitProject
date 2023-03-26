import dash
from dash import html
from dash import dcc
import pandas as pd
import datetime as dt
import time

app = dash.Dash(__name__)

data_ystrd = pd.read_csv('Projet/prix_airbus.csv', header=None, names=['date', 'price'])

data_ystrd['date'] = pd.to_datetime(data_ystrd['date'])

# Get today's date
today = dt.date.today()

# Get yesterday's date
yesterday = today - dt.timedelta(days=1)

# Filter the DataFrame to only include yesterday's data
yesterday_data = data_ystrd[(data_ystrd['date'].dt.date == yesterday)]

# Find the highest price from yesterday's data
highest_price = yesterday_data['price'].max()
lowest_price = yesterday_data['price'].min()
volatility = (yesterday_data['price'].pct_change()).std()
close_price = yesterday_data['price'].iloc[-1]
open_price = yesterday_data['price'].iloc[0]


app.layout = html.Div([
    dcc.Graph(id='airbus-price-graph'),
html.Div([html.P(f'Data from Yesterday'),html.P(f'Volatility: {volatility}'),html.P(f'Highest Price: {highest_price} | Close Price: {close_price}'),html.P(f'Lowest Price: {lowest_price} | Open Price: {open_price}')]),
    dcc.Interval(
        id='interval-component',
        interval=60000,  # 1 minute
        n_intervals=0
    )
])

@app.callback(dash.dependencies.Output('airbus-price-graph', 'figure'),
              [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_graph(n):
    try:
        df = pd.read_csv('Projet/prix_airbus.csv', names=['date', 'price'])
        df['date'] = pd.to_datetime(df['date'])
        data = df


        return {
            'data': [{
                'x': data['date'],
                'y': data['price'],
                'type': 'line',
                'name': 'AIRBUS price'
            }],
            'layout': {
                'title': 'AIRBUS Share Price in EUR',
                'xaxis': {
                    'title': 'Date'
                },
                'yaxis': {
                    'title': 'Price (EUR)'
                }
            }
        }
    except Exception as e:
        print(e)
        return {}

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)

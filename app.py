import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import os
from datetime import datetime, timedelta

app = dash.Dash(__name__)
server = app.server

data_dir = 'data'
data_files = {
    'AAPL': 'HistoricalData_Apple.csv',
    'AMZN': 'HistoricalData_Amazon.csv',
    'MSFT': 'HistoricalData_Microsoft.csv',
    'NFLX': 'HistoricalData_Netflix.csv',
    'SBUX': 'HistoricalData_Starbucks.csv',
    'ADANIPORTS': 'ADANIPORTS.csv',
    'TCS': 'TCS.csv',
    'TATASTEEL': 'TATASTEEL.csv',
    'TATAMOTORS': 'TATAMOTORS.csv',
    'RELIANCE': 'RELIANCE.csv'
}

def load_data(ticker):
    df = pd.read_csv(os.path.join(data_dir, data_files[ticker]))
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '').str.replace('/', '')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=['date'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%B')
    return df

def generate_predictions(df, close_col):
    last_date = df['date'].max()
    last_close = df[close_col].iloc[-1]
    future_dates = [last_date + timedelta(days=30 * i) for i in range(1, 13)]
    future_prices = [last_close * (1 + 0.02) ** i for i in range(1, 13)]  # 2% growth monthly
    pred_df = pd.DataFrame({'date': future_dates, 'predicted_close': future_prices})
    return pred_df

all_data = pd.concat([
    load_data(ticker).assign(ticker=ticker)
    for ticker in data_files
])

available_years = sorted(all_data['year'].dropna().unique())
available_months = sorted(all_data['month'].dropna().unique(), key=lambda m: datetime.strptime(m, "%B").month)

app.layout = html.Div([
    html.H1("Stock Price Dashboard", className="header-title"),

    html.Div([
        html.Label("Theme:"),
        dcc.RadioItems(
            id='theme-toggle',
            options=[
                {'label': 'Day', 'value': 'day-theme'},
                {'label': 'Night', 'value': 'night-theme'}
            ],
            value='day-theme',
            labelStyle={'display': 'inline-block', 'margin-right': '15px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    html.Div([
        html.Div([
            html.Label("Select Ticker:"),
            dcc.Dropdown(
                id='ticker-dropdown',
                options=[{'label': key, 'value': key} for key in data_files],
                value='AAPL',
                clearable=False
            )
        ], className='dropdown'),

        html.Div([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(y), 'value': y} for y in available_years],
                value=available_years[0],
                clearable=False
            )
        ], className='dropdown'),

        html.Div([
            html.Label("Select Month:"),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': m, 'value': m} for m in available_months],
                value=available_months[0],
                clearable=False
            )
        ], className='dropdown'),
    ], className='filters'),

    html.Div(id='stats-cards', className='stats-cards'),

    html.Div([
        dcc.Graph(id='volume-chart'),
        dcc.Graph(id='scatter-chart'),
        dcc.Graph(id='candlestick-chart'),
        dcc.Graph(id='prediction-chart')
    ])
])

@app.callback(
    Output('stats-cards', 'children'),
    Output('volume-chart', 'figure'),
    Output('scatter-chart', 'figure'),
    Output('candlestick-chart', 'figure'),
    Output('prediction-chart', 'figure'),
    Input('ticker-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value')
)
def update_dashboard(ticker, year, month):
    df = load_data(ticker)
    df = df[(df['year'] == year) & (df['month'] == month)]

    if df.empty:
        return html.Div("No data available."), go.Figure(), go.Figure(), go.Figure(), go.Figure()

    for col in ['open', 'high', 'low', 'closelast', 'close']:
        if col in df.columns:
            df[col] = df[col].replace({r'\$': '', ',': ''}, regex=True).astype(float)

    close_col = 'closelast' if 'closelast' in df.columns else 'close' if 'close' in df.columns else None

    open_price = df.iloc[0]['open'] if 'open' in df.columns else None
    high_price = df['high'].max() if 'high' in df.columns else None
    low_price = df['low'].min() if 'low' in df.columns else None
    close_price = df.iloc[-1][close_col] if close_col else None

    stats = html.Div([
        html.Div([html.H4("Open"), html.P(f"${open_price:,.2f}" if open_price else "N/A")], className='card'),
        html.Div([html.H4("High"), html.P(f"${high_price:,.2f}" if high_price else "N/A")], className='card green'),
        html.Div([html.H4("Low"), html.P(f"${low_price:,.2f}" if low_price else "N/A")], className='card red'),
        html.Div([html.H4("Close"), html.P(f"${close_price:,.2f}" if close_price else "N/A")], className='card')
    ], className='stats-container')

    vol_fig = go.Figure()
    if 'volume' in df.columns:
        vol_fig.add_trace(go.Scatter(x=df['date'], y=df['volume'], mode='lines+markers'))
        vol_fig.update_layout(title='Historical Volume', yaxis_title='Volume')

    scatter_fig = go.Figure()
    if 'low' in df.columns and 'high' in df.columns:
        scatter_fig.add_trace(go.Scatter(x=df['low'], y=df['high'], mode='markers'))
        scatter_fig.update_layout(title='High and Low Comparison', xaxis_title='Low', yaxis_title='High')

    candle_fig = go.Figure()
    if all(col in df.columns for col in ['open', 'high', 'low', close_col]):
        candle_fig.add_trace(go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df[close_col]
        ))
        candle_fig.update_layout(title='Historical Candlestick Chart')

    # Prediction chart
    prediction_df = generate_predictions(df, close_col)
    pred_fig = go.Figure()
    pred_fig.add_trace(go.Scatter(x=df['date'], y=df[close_col], name='Historical Close'))
    pred_fig.add_trace(go.Scatter(x=prediction_df['date'], y=prediction_df['predicted_close'], name='Predicted Close', line=dict(dash='dash')))
    pred_fig.update_layout(title='Future Close Price Predictions')

    # Save predictions to CSV
    prediction_df.to_csv(f'predictions_{ticker}.csv', index=False)

    return stats, vol_fig, scatter_fig, candle_fig, pred_fig

app.clientside_callback(
    """
    function(theme) {
        document.body.className = theme;
        return {};
    }
    """,
    Output('stats-cards', 'style'),
    Input('theme-toggle', 'value')
)

if __name__ == '__main__':
    app.run(debug=True)

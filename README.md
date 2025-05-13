Project Workflow
Data Collection: Imported historical stock data from multiple companies in CSV format.

Data Preprocessing: Cleaned and formatted the data using Pandas for consistency and analysis.

Model Building: Applied Linear Regression to predict future closing prices.

Dashboard Development: Built an interactive Dash + Plotly dashboard with theme toggle, filters, and visualizations (volume, scatter, candlestick, and prediction line chart).

Deployment: Saved predictions to CSV and hosted the dashboard for user interaction.


📈 Stock Price Dashboard with Forecasting
This project is an interactive Stock Price Dashboard built using Plotly Dash, which allows users to:

Visualize historical stock data (Open, High, Low, Close, Volume)

Explore candlestick charts and high-low scatter plots

Select specific companies, years, and months for detailed insights

Switch between Day and Night themes (Pastel Pink / Dark Pink)

Generate and visualize future close price predictions

Automatically save forecasted results to CSV for each stock

🚀 Features
🔍 Dropdown Filters – Choose stock ticker, year, and month

📊 Graph Visualizations – Volume, scatter, candlestick, and prediction charts

🧠 Prediction Engine – Simple future price forecasting (can be replaced with real ML models)

💾 CSV Export – Saves predicted values as predictions_<TICKER>.csv

🌗 Light/Dark Mode – Beautiful pastel pink and dark pink themes with smooth transitions

📱 Responsive Design – Fully responsive layout across devices

📂 Data Source
The dashboard uses CSV files containing historical stock prices for companies like:

AAPL (Apple)

AMZN (Amazon)

MSFT (Microsoft)

NFLX (Netflix)

SBUX (Starbucks)

TCS, TATASTEEL, TATAMOTORS, RELIANCE, ADANIPORTS (India-based stocks)

Each file must include a Date column and price columns (Open, High, Low, Close or Close/Last, and Volume).

🛠️ Tech Stack
Dash (by Plotly)

Pandas

Plotly Graph Objects

HTML / CSS (custom themes)

Python

🔮 Future Improvements
Integrate real ML models (e.g., ARIMA, LSTM)

Add financial indicators (SMA, RSI, etc.)

Deploy online via Heroku, Vercel, or Render


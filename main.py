import requests
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

class DataEngine:
    def __init__(self, db_name="data_warehouse.db"):
        self.db_name = db_name
        self.api_url = "https://api.coingecko.com/api/v3/coins/markets"

    def run_etl(self):
        """ENGINEERING: Extract, Transform, and Load"""
        # 1. Extract
        params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 10}
        response = requests.get(self.api_url, params=params)
        raw_data = response.json()

        # 2. Transform (Data Engineer Vibe)
        df = pd.DataFrame(raw_data)
        df = df[['id', 'symbol', 'current_price', 'market_cap', 'price_change_percentage_24h']]
        df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 3. Load (Database Logic)
        conn = sqlite3.connect(self.db_name)
        df.to_sql('market_data', conn, if_exists='append', index=False)
        conn.close()
        print("✅ Pipeline Success: Data stored in local Warehouse.")

    def generate_analytics(self):
        """ANALYST: Query and Visualize"""
        conn = sqlite3.connect(self.db_name)
        # SQL Query inside Python to show multi-skill
        query = """
            SELECT symbol, AVG(current_price) as avg_price, MAX(market_cap) as peak_cap
            FROM market_data 
            GROUP BY symbol
        """
        analysis_df = pd.read_sql(query, conn)
        conn.close()

        # Generate a high-end interactive chart
        fig = px.bar(analysis_df, x='symbol', y='avg_price', 
                     title="Market Intelligence: Average Price Trends",
                     labels={'avg_price': 'Average Price (USD)', 'symbol': 'Asset'},
                     template="plotly_dark")
        
        # Save as an interactive HTML file (The 'Dashboard')
        fig.write_html("dashboard.html")
        print("📊 Analysis Success: Dashboard generated as 'dashboard.html'.")

if __name__ == "__main__":
    engine = DataEngine()
    engine.run_etl()
    engine.generate_analytics()
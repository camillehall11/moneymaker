import streamlit as st
import pandas as pd
import time
import sys
import os
import psycopg2
from psycopg2 import sql
from bot2 import EnhancedDexScreenerBot

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Database connection parameters
DB_CONFIG = {
    'host': 'dexscreener.cpc6aoosaboe.us-east-2.rds.amazonaws.com',
    'database': 'dexscreener',  # Replace with your actual database name
    'user': 'camillehall11',          # Replace with your actual database username
    'password': 'Artist2025!!',      # Replace with your actual database password
    'port': 5432                      # Default PostgreSQL port
}

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")
        return None

# Function to insert trade data into the trade_history table
def insert_trade(trade_id, symbol, side, price, quantity, timestamp):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = sql.SQL("""
                INSERT INTO trade_history (trade_id, symbol, side, price, quantity, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (trade_id, symbol, side, price, quantity, timestamp))
            conn.commit()
            st.success("Trade inserted successfully!")
        except Exception as e:
            st.error(f"Failed to insert trade: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to insert metrics data into the metrics table
def insert_metrics(wallet_balance, total_pnl, win_rate, open_orders, positions, timestamp):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = sql.SQL("""
                INSERT INTO metrics (wallet_balance, total_pnl, win_rate, open_orders, positions, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (wallet_balance, total_pnl, win_rate, open_orders, positions, timestamp))
            conn.commit()
            st.success("Metrics inserted successfully!")
        except Exception as e:
            st.error(f"Failed to insert metrics: {e}")
        finally:
            cursor.close()
            conn.close()

# Function to fetch trade history from the database
def fetch_trade_history():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trade_history ORDER BY timestamp DESC")
            trades = cursor.fetchall()
            return trades
        except Exception as e:
            st.error(f"Failed to fetch trade history: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

# Function to fetch metrics from the database
def fetch_metrics():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 1")
            metrics = cursor.fetchone()
            return metrics
        except Exception as e:
            st.error(f"Failed to fetch metrics: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

# Initialize the bot
if "bot" not in st.session_state:
    try:
        st.session_state.bot = EnhancedDexScreenerBot()
    except Exception as e:
        st.error(f"Failed to initialize the bot: {e}")
        st.session_state.bot = None

# Streamlit UI
st.title("Trading Bot Dashboard")
st.sidebar.header("Configuration")

# Wallet Connection (Placeholder)
if st.sidebar.button("🔗 Connect Phantom Wallet"):
    st.sidebar.success("Wallet connected successfully!")

# Bot Controls
st.sidebar.header("Bot Controls")
if st.sidebar.button("▶️ Start Bot"):
    if st.session_state.bot:
        st.session_state.bot.run()
        st.success("Bot started!")
    else:
        st.error("Bot is not initialized. Check the logs for errors.")

if st.sidebar.button("⏹️ Stop Bot"):
    if st.session_state.bot:
        st.session_state.bot.stop()
        st.warning("Bot stopped!")
    else:
        st.error("Bot is not initialized. Check the logs for errors.")

# Display Trade History
st.header("Trade History")
trades = fetch_trade_history()
if trades:
    trades_df = pd.DataFrame(trades, columns=["id", "trade_id", "symbol", "side", "price", "quantity", "timestamp"])
    st.table(trades_df)
else:
    st.info("No trades executed yet.")

# Display Metrics Table
st.header("Metrics Overview")
metrics = fetch_metrics()
if metrics:
    metrics_data = {
        "Metric": ["Wallet Balance", "Total PnL", "Win Rate", "Open Orders", "Positions"],
        "Value": [
            f"${metrics[1]:.2f}",  # wallet_balance
            f"${metrics[2]:.2f}",  # total_pnl
            f"{metrics[3]:.2f}%",  # win_rate
            str(metrics[4]),       # open_orders
            str(metrics[5])        # positions
        ]
    }
    metrics_df = pd.DataFrame(metrics_data)
    st.table(metrics_df)
else:
    st.error("No metrics available.")

# Refresh the app every 2 seconds to show real-time updates
time.sleep(2)
st.rerun()

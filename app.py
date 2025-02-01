import streamlit as st
import pandas as pd
import time
import sys
import os
from bot2 import EnhancedDexScreenerBot

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
if st.session_state.bot:
    metrics = st.session_state.bot.get_metrics()
    if metrics["trades"]:
        trades_df = pd.DataFrame(metrics["trades"])
        st.table(trades_df)
    else:
        st.info("No trades executed yet.")
else:
    st.error("Bot is not initialized. Check the logs for errors.")

# Display Metrics Table
st.header("Metrics Overview")
if st.session_state.bot:
    metrics = st.session_state.bot.get_metrics()
    metrics_data = {
        "Metric": ["Wallet Balance", "Total PnL", "Win Rate", "Open Orders", "Positions"],
        "Value": [
            f"${metrics['wallet_balance']:.2f}",
            f"${metrics['total_pnl']:.2f}",
            f"{metrics['win_rate']:.2f}%",
            str(metrics["open_orders"]),
            str(metrics["positions"])
        ]
    }
    metrics_df = pd.DataFrame(metrics_data)
    st.table(metrics_df)
else:
    st.error("Bot is not initialized. Check the logs for errors.")

# Refresh the app every 2 seconds to show real-time updates
time.sleep(2)
st.rerun()

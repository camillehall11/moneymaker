import streamlit as st
import pandas as pd
import time
from bot2 import EnhancedDexScreenerBot

# Initialize the bot
if "bot" not in st.session_state:
    st.session_state.bot = EnhancedDexScreenerBot()

# Streamlit UI
st.title("Trading Bot Dashboard")
st.sidebar.header("Configuration")

# Wallet Connection (Placeholder)
if st.sidebar.button("🔗 Connect Phantom Wallet"):
    st.sidebar.success("Wallet connected successfully!")  # Replace with actual wallet connection logic

# Bot Controls
st.sidebar.header("Bot Controls")
if st.sidebar.button("▶️ Start Bot"):
    st.session_state.bot.run()
    st.success("Bot started!")

if st.sidebar.button("⏹️ Stop Bot"):
    st.session_state.bot.stop()
    st.warning("Bot stopped!")

# Display Trade History
st.header("Trade History")
metrics = st.session_state.bot.get_metrics()
if metrics["trades"]:
    trades_df = pd.DataFrame(metrics["trades"])
    st.table(trades_df)
else:
    st.info("No trades executed yet.")

# Display Metrics Table
st.header("Metrics Overview")
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

# Refresh the app every 2 seconds to show real-time updates
time.sleep(2)
st.rerun()

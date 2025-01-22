import os

import matplotlib.pyplot as plt
import pandas as pd
from langchain.tools import tool

from src.tools.data import calculate_insights, fetch_historical_data


@tool
def create_visualizations(
    token_id: str, days: int = 7, currency: str = "usd", output_folder: str = "images"
) -> str:
    """
    Fetch historical data for a token and generate visualizations.

    This tool retrieves historical price and volume data for a specified token, then generates visualizations showing price trends, volume trends, and rolling volatility.

    Args:
        token_id (str): The unique identifier of the token as per CoinGecko (e.g., 'ethereum', 'bitcoin').
        days (int, optional): Number of past days to fetch data for (default: 7).
        currency (str, optional): The target currency for the data (default: 'usd').
        output_folder (str, optional): The directory where the visualizations will be saved (default: 'images').

    Returns:
        str: The path to the output folder where visualizations are saved.

    Visualizations:
        1. Price Trend: A line plot of token prices over time.
        2. Volume Trend: A line plot of token trading volumes over time.
        3. Rolling Volatility: A line plot of the token's rolling volatility over time.
    """
    data = fetch_historical_data(token_id=token_id, days=days, currency=currency)
    data = calculate_insights(data)
    df = pd.DataFrame(data)  # Convert dictionary back to DataFrame
    os.makedirs(output_folder, exist_ok=True)

    # Price Trend
    plt.figure(figsize=(10, 6))
    plt.plot(df["dates"], df["prices"], label="Price", color="blue")
    plt.title(f"Price Trend for {token_id}")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.savefig(os.path.join(output_folder, f"{token_id}_price_trend.png"))
    plt.close()

    # Volume Trend
    plt.figure(figsize=(10, 6))
    plt.plot(df["dates"], df["volumes"], label="Volume", color="green")
    plt.title(f"Volume Trend for {token_id}")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.legend()
    plt.savefig(os.path.join(output_folder, f"{token_id}_volume_trend.png"))
    plt.close()

    # Volume Trend
    plt.figure(figsize=(10, 6))
    plt.plot(df["dates"], df["volumes"], label="Volume", color="green")
    plt.title(f"Volume Trend for {token_id}")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.legend()
    plt.savefig(os.path.join(output_folder, f"{token_id}_volume_trend.png"))
    plt.close()

    return output_folder

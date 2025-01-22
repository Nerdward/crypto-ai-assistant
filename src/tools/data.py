from pprint import pprint
from typing import Any, Dict

import numpy as np
import pandas as pd
import requests
from langchain.tools import tool

from src.config import TOKENS


def get_current_price(token_id, currency="usd"):
    """
    Fetch the current price of a token.
    :param token_id: Token ID as per CoinGecko (e.g., 'tether', 'dai')
    :param currency: Target currency (default: 'usd')
    :return: Current price of the token
    """
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": token_id, "vs_currencies": currency}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get(token_id, {}).get(currency, None)
    else:
        print(f"Failed to fetch price for {token_id}: {response.status_code}")
        return None


@tool("get_trending_coins", return_direct=True)
def get_trending_coins_tool(top_n: int = 10) -> str:
    """
    Fetches the top trending coins from CoinGecko.

    Parameters:
        top_n (int): Number of trending coins to fetch (10 or 20). Default is 10.

    Returns:
        str: A formatted string with the top trending coins and their details.
    """
    if top_n not in [10, 20]:
        return "Error: top_n must be 10 or 20."

    url = "https://api.coingecko.com/api/v3/search/trending"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Get the trending coins list
        coins = data.get("coins", [])

        # Limit to the requested number of coins
        trending_coins = coins[:top_n]

        # Create a readable string with coin details
        result = []
        for idx, coin in enumerate(trending_coins, start=1):
            name = coin["item"]["name"]
            symbol = coin["item"]["symbol"]
            market_cap_rank = coin["item"].get("market_cap_rank", "N/A")
            price_btc = coin["item"]["price_btc"]
            result.append(
                f"{idx}. {name} ({symbol}) - Market Cap Rank: {market_cap_rank} - Price (BTC): {price_btc:.8f}"
            )

        return "\n".join(result)
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"


def fetch_historical_data(token_id, days=7, currency="usd") -> Dict | None:
    """
    Fetch historical price and volume data for the tokens in the portfolio.

    Args:
        days (int): Number of past days to fetch data for.
        currency (str): Target currency for the data.

    Returns:
        dict: A dictionary.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart"
    params = {"vs_currency": currency, "days": days}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {token_id}: {response.status_code}")
        return None


def calculate_percent_change(prices):
    percent_changes = []
    for i in range(1, len(prices)):
        change = ((prices[i] - prices[i - 1]) / prices[i - 1]) * 100
        percent_changes.append(change)
    return percent_changes


def calculate_volume_change(volumes):
    volume_changes = []
    for i in range(1, len(volumes)):
        change = ((volumes[i] - volumes[i - 1]) / volumes[i - 1]) * 100
        volume_changes.append(change)
    return volume_changes


def calculate_rolling_volatility(percent_changes, window=7):
    volatilities = []
    for i in range(len(percent_changes) - window + 1):
        window_data = percent_changes[i : i + window]
        volatility = np.std(window_data)
        volatilities.append(volatility)
    return volatilities


def calculate_pvr(prices, volumes):
    return [prices[i] / volumes[i] for i in range(len(prices))]


def calculate_insights(historical_data: Dict):
    prices = [price[1] for price in historical_data["prices"]]
    volumes = [volume[1] for volume in historical_data["total_volumes"]]
    dates = [price[0] for price in historical_data["prices"]]
    df = df = pd.DataFrame(
        {
            "dates": pd.to_datetime(dates, unit="ms"),
            "prices": prices,
            "volumes": volumes,
        }
    )
    df["percent_change"] = df["prices"].pct_change() * 100
    df["volume_change"] = df["volumes"].pct_change() * 100
    df["rolling_volatility"] = df["percent_change"].rolling(window=7).std()
    df["pvr"] = df["prices"] / df["volumes"]

    return df.to_dict()


@tool
def fetch_portfolio_historical_data(days=7, currency="usd"):
    """
    Fetch historical price and volume data for the tokens in the portfolio.

    Args:
        days (int): Number of past days to fetch data for.
        currency (str): Target currency for the data.

    Returns:
        dict: A dictionary where keys are token names and values are Pandas DataFrames with historical data.
    """
    token_ids = {
        "USDT": "tether",
        "DAI": "dai",
        "USDC": "usd-coin",
        "LINK": "chainlink",
        "UNI": "uniswap",
        "WBTC": "wrapped-bitcoin",
        "AAVE": "aave",
        "MKR": "maker",
        "COMP": "compound",
        "SUSHI": "sushi",
    }
    portfolio_historical_data = {}
    for token in TOKENS:
        token_id = token_ids[token]
        historical_data = fetch_historical_data(token_id, days=days, currency=currency)
        if historical_data:
            prices = [price[1] for price in historical_data["prices"]]
            volumes = [volume[1] for volume in historical_data["total_volumes"]]
            dates = [price[0] for price in historical_data["prices"]]

            # Create DataFrame
            df = pd.DataFrame(
                {
                    "dates": pd.to_datetime(dates, unit="ms"),
                    "prices": prices,
                    "volumes": volumes,
                }
            )

            # Calculate insights
            df = calculate_insights(df)

            portfolio_historical_data[token] = df
    return portfolio_historical_data


@tool
def tool_get_current_price(token_id: str, currency: str = "usd") -> float:
    """
    Fetch the current price of a token.

    Args:
        token_id (str): Token ID as per CoinGecko (e.g., 'tether', 'dai').
        currency (str): Target currency (default: 'usd').

    Returns:
        float: Current price of the token in the specified currency.
    """
    return get_current_price(token_id, currency)


@tool(response_format="content_and_artifact")
def tool_fetch_historical_data(token_id: str, days: int = 7, currency: str = "usd"):
    """
    Fetch and return historical price and volume data for a specific token.

    This tool retrieves historical market data for a cryptocurrency token, including price trends and trading volumes over a specified number of days.
    The data is fetched from the CoinGecko API and returned along with a summary message.

    Args:
        token_id (str): The unique identifier of the token as per CoinGecko (e.g., 'tether', 'dai').
        days (int): The number of days of historical data to fetch (default: 7).
        currency (str): The target currency for the data (default: 'usd').

    Returns:
        tuple: A tuple containing a summary string and a dictionary with the following keys:
            - 'prices': List of prices for the token over the specified period.
            - 'volumes': List of trading volumes over the same period.
            - 'dates': List of corresponding timestamps for the data points.
    """
    return f"Generated data for {token_id}", fetch_historical_data(
        token_id, days, currency
    )


if __name__ == "__main__":
    # print(get_current_price("tether"))
    pprint(fetch_portfolio_historical_data())
    # Fetch data for top tokens
    # token_ids = [
    #     "tether",
    #     # "dai",
    #     # "usd-coin",
    #     # "chainlink",
    #     # "uniswap",
    #     # "wrapped-bitcoin",
    #     # "aave",
    #     # "maker",
    #     # "compound",
    #     # "sushi",
    # ]
    # for token in token_ids:
    #     data = fetch_historical_data(token, days=1)
    #     if data:
    #         print(f"{token}: {data}")  # Print the first 5 price points

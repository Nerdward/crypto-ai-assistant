from collections import defaultdict
from typing import Any, Dict

from langchain.tools import tool

from src.config import TOKENS, WALLET_ADDRESS
from src.tools.data import get_current_price
from src.utils.ethereum import _get_transaction_history, get_token_balance


@tool
def get_portfolio() -> Dict[str, float]:
    """
    Fetch the user's token portfolio balances.

    Returns:
        dict: A dictionary where the keys are token names and the values are
            their balances.
    """
    portfolio = {}
    """
    Fetch the user's token portfolio balances.

    Returns:
        dict: A dictionary where the keys are token names and the values are 
            their balances.
    """
    for token, contract_address in TOKENS.items():
        print(f"Fetching data for {token}...")
        # Fetch token balance
        balance = get_token_balance(contract_address, WALLET_ADDRESS)
        portfolio[token] = balance

    return portfolio


@tool
def get_portfolio_distribution() -> Dict[str, Any]:
    """
    Fetch the user's portfolio distribution in USD.

    Returns:
        dict: A dictionary with token names as keys and their percentage share
        in the portfolio as values.
        float: The total value of the portfolio in USD.
    """
    portfolio = defaultdict(float)
    total_value = 0
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

    for token, contract_address in TOKENS.items():
        balance = get_token_balance(contract_address, WALLET_ADDRESS)
        usd_value = balance * get_current_price(token_ids[token])
        portfolio[token] = usd_value
        total_value += usd_value

    try:
        # Calculate portfolio percentage
        portfolio_distribution = {
            token: value / total_value for token, value in portfolio.items()
        }

    except ZeroDivisionError:
        portfolio_distribution = {token: 0 for token, value in portfolio.items()}

    return {
        "Portfolio Distribution": portfolio_distribution,
        "Total Value": total_value,
    }


@tool
def get_contract_transaction_history() -> Dict[str, list]:
    """
    Fetch the transaction history for each token in the user's portfolio.

    Returns:
        dict: A dictionary where the keys are token names and the values are
        lists of transactions.
    """
    transactions = {}
    for token, contract_address in TOKENS.items():
        print(f"Fetching data for {token}...")

        # Fetch transaction history
        tx_history = _get_transaction_history(WALLET_ADDRESS, contract_address)
        transactions[token] = tx_history

    return transactions

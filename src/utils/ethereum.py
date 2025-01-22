import requests
from web3 import Web3

from src.config import ETHERSCAN_API_KEY, INFURA_API, TOKENS, WALLET_ADDRESS
from src.utils.contract import fetch_abi_with_cache

# Replace with your Infura/Alchemy API URL
INFRA_URL = f"https://mainnet.infura.io/v3/{INFURA_API}"
web3 = Web3(Web3.HTTPProvider(INFRA_URL))


def get_token_balance(contract_address, wallet_address):
    try:
        abi = fetch_abi_with_cache(contract_address)
        contract = web3.eth.contract(
            address=web3.to_checksum_address(contract_address), abi=abi
        )
        balance = contract.functions.balanceOf(wallet_address).call()
        return web3.from_wei(balance, "ether")  # Assuming token has 18 decimals
    except Exception as e:
        print(f"Error fetching balance for {contract_address}: {e}")
        return 0


def _get_transaction_history(wallet_address, contract_address):
    try:
        etherscan_api_url = f"https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "tokentx",
            "address": wallet_address,
            "contractaddress": contract_address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "asc",
            "apikey": ETHERSCAN_API_KEY,
        }
        response = requests.get(etherscan_api_url, params=params)
        data = response.json()
        if data["status"] == "1":
            return data["result"]
        else:
            print(f"No transactions found for contract {contract_address}.")
            return []
    except Exception as e:
        print(f"Error fetching transaction history: {e}")
        return []


if __name__ == "__main__":
    if not web3.is_connected():
        print("Failed to connect to Ethereum node.")
        exit()

    if not web3.is_address(WALLET_ADDRESS):
        print("Invalid wallet address.")
        exit()

    portfolio = {}
    transactions = {}

    for token, contract_address in TOKENS.items():
        print(f"Fetching data for {token}...")
        # Fetch token balance
        balance = get_token_balance(contract_address, WALLET_ADDRESS)
        portfolio[token] = balance

        # Fetch transaction history
        tx_history = _get_transaction_history(WALLET_ADDRESS, contract_address)
        transactions[token] = tx_history

    print("Portfolio:", portfolio)
    print("Transactions:")
    for token, txs in transactions.items():
        print(f"{token}: {len(txs)} transactions")

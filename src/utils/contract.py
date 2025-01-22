import json
import os

import requests  # for http requests

from src.config import ETHERSCAN_API_KEY


def fetch_abi_with_cache(contract_address: str, cache_file="abi_cache.json"):
    # Load cache if exists
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    # Check if ABI is in cache
    if contract_address in cache:
        return cache[contract_address]

    # Fetch ABI from Etherscan
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        abi = response.json().get("result")
        if abi:
            cache[contract_address] = abi
            # Save updated cache to file
            with open(cache_file, "w") as f:
                json.dump(cache, f)
            return abi
        else:
            raise ValueError(
                f"Failed to fetch ABI for {contract_address}: {response.json().get('message')}"
            )
    else:
        raise ConnectionError(
            f"Error fetching ABI: {response.status_code} - {response.text}"
        )

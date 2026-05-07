"""
Assignment 5: Deploy HelloWorld Smart Contract on Ethereum Testnet
-------------------------------------------------------------------
This script shows the basic deployment flow with Web3.py.

Before running:
1. Install dependencies: pip install web3 py-solc-x python-dotenv
2. Create .env with:
   RPC_URL=your_testnet_rpc
   PRIVATE_KEY=your_wallet_private_key
   ACCOUNT_ADDRESS=your_wallet_address

Note: Keep private key secret. Use a throwaway test wallet only.
"""

import json
import os

from dotenv import load_dotenv
from solcx import compile_standard, install_solc
from web3 import Web3


def load_contract_source(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    load_dotenv()

    rpc_url = os.getenv("RPC_URL")
    private_key = os.getenv("PRIVATE_KEY")
    account_address = os.getenv("ACCOUNT_ADDRESS")

    if not rpc_url or not private_key or not account_address:
        raise ValueError("Please set RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS in .env")

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Web3 could not connect to RPC.")

    source_code = load_contract_source("HelloWorld.sol")

    install_solc("0.8.20")
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {"HelloWorld.sol": {"content": source_code}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.20",
    )

    abi = compiled["contracts"]["HelloWorld.sol"]["HelloWorld"]["abi"]
    bytecode = compiled["contracts"]["HelloWorld.sol"]["HelloWorld"]["evm"][
        "bytecode"
    ]["object"]

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = web3.eth.get_transaction_count(account_address)

    tx = contract.constructor("Hello from testnet").build_transaction(
        {
            "from": account_address,
            "nonce": nonce,
            "gas": 500000,
            "gasPrice": web3.eth.gas_price,
            "chainId": web3.eth.chain_id,
        }
    )

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print("Deploy tx hash:", tx_hash.hex())
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Contract deployed at:", receipt.contractAddress)

    # Save ABI + address for next assignments.
    with open("helloworld_deployment.json", "w", encoding="utf-8") as f:
        json.dump({"address": receipt.contractAddress, "abi": abi}, f, indent=2)

    print("Saved deployment info to helloworld_deployment.json")

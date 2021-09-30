from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

install_solc("0.8.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our Solidity
compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

# with open("compiled_code.json", "w") as file:
#     json.dump(compile_sol, file)

# Deploy in Python - You need Bytecode and ABI
# 1st - get bytecode
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
# then - get abi
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# then - connect to Ganache (a simulated blockchain)
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x60af798F39dafAF6d8973e7f81512fC58347AA59"
private_key = os.getenv("PRIVATE_KEY")

# then - Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# then - 1. Build the Contract Deploy Transaction, 2. Sign the Trxn, 3. Send the Trxn
# But first, get latest transaction (which will be the nonce)
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# 2. Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# When working with Contract, you need: Contract ABI & Contract Address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# We can now start interacting with our contract (exactly like in Remix)
# We can interact with them in two different ways:
# Call -> Simulate making a call and getting a return value (it doesn't make a state change to the blockchain)
# Transact -> Actually make a state change
print(simple_storage.functions.retrieve().call())  # Initial value of favorite number
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())

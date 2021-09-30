from solcx import compile_standard, install_solc
import json
from web3 import Web3

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
chain_id = 5777

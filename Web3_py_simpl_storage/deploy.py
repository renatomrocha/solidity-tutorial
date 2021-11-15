from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

install_solc("0.6.0")

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)


compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")


SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address)


# Build transaction object
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
#Get receipt from deployment transaction
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed with receipt {}".format(tx_receipt))



"""Working with Contracts you need
    Contract ABI
    Contact Address"""


simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making a call and getting a return value
# Transact -> Actually make a state change

# Initial value for fav number
print("Calling retrieve function from Simplestorage")
print(simple_storage.functions.retrieve().call())

#No transaction is done, just simulates function
print("Calling store function from Simplestorage")
print(simple_storage.functions.store(15).call())


# build
print("Building store() transaction")
store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1
})

print(store_transaction)
#sign
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

#send
print("Sending tx")
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Tx confirmed with receipt {}".format(tx_receipt))
print("Calling retrieve after store tx sent")

print(simple_storage.functions.retrieve().call())

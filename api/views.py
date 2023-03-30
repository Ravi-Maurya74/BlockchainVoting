from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from web3 import Web3
from solcx import compile_standard, install_solc
from hexbytes import HexBytes


# Create your views here.

chain_id = 11155111
my_address = "0xb7A2E79FD29106f03C17b6aD2E03e520ABEf6A20"
private_key = "0xd1bdfc5831558a8c212cba587a1749f0bf22871933bacd3eacfebe9b936c0e76"
contract_address = "0x2A532DA32BF9B3e9cb6fd42d188E8317B8B3ea17"
abi = [
    {
        "inputs": [{"internalType": "string", "name": "_compString", "type": "string"}],
        "name": "compareOurString",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "ourString",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_updateString", "type": "string"}
        ],
        "name": "updateOurString",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


@api_view(["POST"])
def test(request):
    received_json_data = json.loads(request.body)
    w3 = Web3(
        Web3.HTTPProvider(
            "https://sepolia.infura.io/v3/ed97a557d0a646669e1640f304c8a111"
        )
    )

    nonce = w3.eth.get_transaction_count(my_address)
    print(nonce)

    my_contract = w3.eth.contract(address=contract_address, abi=abi)
    result = my_contract.functions.compareOurString("Abhshek").call()
    print(result)

    call_function = my_contract.functions.updateOurString(
        received_json_data["newName"]
    ).build_transaction({"chainId": chain_id, "from": my_address, "nonce": nonce})

    signed_tx = w3.eth.account.sign_transaction(call_function, private_key=private_key)

    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print(tx_receipt)

    return Response(
        {
            "status": "Working",
            "Code": 200,
            "nonce": nonce,
            "result": result,
            "receipt": json.dumps(tx_receipt["transactionHash"].hex(), default=vars),
        }
    )

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import Election, Choice, Voter
from .serializers import ElectionSerializer, VoterSerialzer, ChoiceSerialzer

from web3 import Web3
from solcx import compile_standard, install_solc
from hexbytes import HexBytes


# Create your views here.

chain_id = 11155111
my_address = "0xb7A2E79FD29106f03C17b6aD2E03e520ABEf6A20"
private_key = "0xd1bdfc5831558a8c212cba587a1749f0bf22871933bacd3eacfebe9b936c0e76"
contract_address = "0x375a062eAc7470899FD3474c412136f2bD606EAC"
abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "election_id", "type": "uint256"},
            {"internalType": "uint256", "name": "choices_count", "type": "uint256"},
        ],
        "name": "createNewElection",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "election_id", "type": "uint256"},
            {"internalType": "uint256", "name": "choice_id", "type": "uint256"},
        ],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "election_id", "type": "uint256"}
        ],
        "name": "getElectionResult",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "stateMutability": "view",
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


class NewVoter(generics.CreateAPIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerialzer


@api_view(["POST"])
def newElection(request):
    received_json_data = json.loads(request.body)
    # index = Election.objects.all().count()
    title = received_json_data["title"]
    number_of_choices = received_json_data["number_of_choices"]
    choices = received_json_data["choices"]
    elec = Election(title=title, number_of_choices=number_of_choices)
    elec.save()
    for choice in choices:
        ch = Choice(name=choice, election=elec)
        ch.save()

    w3 = Web3(
        Web3.HTTPProvider(
            "https://sepolia.infura.io/v3/ed97a557d0a646669e1640f304c8a111"
        )
    )

    my_contract = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.get_transaction_count(my_address)

    # print(nonce)

    # print(elec.id)

    call_function = my_contract.functions.createNewElection(
        elec.id, elec.number_of_choices
    ).build_transaction({"chainId": chain_id, "from": my_address, "nonce": nonce})

    signed_tx = w3.eth.account.sign_transaction(call_function, private_key=private_key)

    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    election_data = ElectionSerializer(elec).data
    return Response(
        {
            "election": election_data,
            "hash": json.dumps(tx_receipt["transactionHash"].hex(), default=vars),
        }
    )


@api_view(["POST"])
def getElectionResult(request):
    received_json_data = json.loads(request.body)
    election_id = received_json_data["election_id"]

    w3 = Web3(
        Web3.HTTPProvider(
            "https://sepolia.infura.io/v3/ed97a557d0a646669e1640f304c8a111"
        )
    )

    my_contract = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.get_transaction_count(my_address)
    result = my_contract.functions.getElectionResult(election_id).call()
    print(result)
    election = Election.objects.get(pk=election_id)
    choices = election.choices
    choices_data = ChoiceSerialzer(choices, many=True).data
    return Response(
        {
            "choices": choices_data,
            "votes": json.dumps(result, default=vars),
        }
    )

@api_view(["POST"])
def castVote(request):
    received_json_data = json.loads(request.body)
    election_id = received_json_data["election_id"]
    

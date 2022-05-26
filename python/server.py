from xmlrpc.server import SimpleXMLRPCServer
from bitstring import BitArray
import hashlib

# the transaction status is 1 if no one won yet and 0 if there is a winner
def transaction_status(transaction_id : int):
    return 1 if transactions[transaction_id]['winner'] == -1 else 0

def seed_valid(challenge : int, seed : str):
    hash_object = hashlib.sha1(seed)
    hashed = hash_object.digest()

    # the challenge is the number of '0's that must exist at the start of the hash
    mask = BitArray('0b' + '1'*challenge + '0'*(160-challenge)).tobytes()

    # do bitwise and between mask and hashed
    return not (hashed & mask)

def get_transaction_id():
    return current_transaction_id

def get_challenge(transaction_id : int):
    if transaction_id <= current_transaction_id:
        return transactions[transaction_id]['Challenge']
    else:
        return -1

def get_transaction_status(transaction_id : int):
    if transaction_id <= current_transaction_id:
        return transaction_status(transaction_id)
    else:
        return -1


def submit_challenge(transaction_id : int, client_id : int, seed : str):
    if transaction_id <= current_transaction_id:
        if transaction_status(transaction_id) == 0:
            return 2
        elif seed_valid(transactions[transaction_id]['challenge'], seed):
            current_transaction_id += 1
            transactions[transaction_id]['winner'] = client_id
            transactions[transaction_id]['seed'] = seed
            transactions.append({'transaction_id': current_transaction_id, 'challenge': 1, 'seed': None, 'winner': -1})
            return 1
        else:
            return 0
    else:
        return -1

def get_winner(transaction_id : int):
    if transaction_id <= current_transaction_id:
        return transactions[transaction_id]['winner'] if transaction_status(transaction_id) == 0 else 0
    else:
        return -1

def get_seed(transaction_id : int):
    if transaction_id <= current_transaction_id:
        return (transaction_status(transaction_id), transactions[transaction_id]['seed'], transactions[transaction_id]['challenge'])
    else:
        return -1

def divide(x, y):
    return x // y

# server starts
server = SimpleXMLRPCServer(("0.0.0.0", 8000))
print("Listening on port 8000...")

transactions = [{'transaction_id': 0, 'challenge': 1, 'seed': None, 'winner': -1}]
current_transaction_id = 0

server.register_function(get_transaction_id, 'getTransactionID')
server.register_function(get_challenge, 'getChallenge')
server.register_function(get_transaction_status, 'getTransactionStatus')
server.register_function(submit_challenge, 'submitChallenge')
server.register_function(get_winner, 'getWinner')
server.register_function(get_seed, 'getSeed')

server.serve_forever()
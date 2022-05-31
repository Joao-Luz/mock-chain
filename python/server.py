from xmlrpc.server import SimpleXMLRPCServer
from bitstring import BitArray
import hashlib
import random

class MockChainServer:

    def __init__(self, ip : str, port : str):

        self.server = SimpleXMLRPCServer((ip, port))
        self.transactions = []
        self.current_transaction_id = -1
        self.new_transaction()

        # register functions
        self.server.register_function(self.get_transaction_id, 'get_transaction_id')
        self.server.register_function(self.get_challenge, 'get_challenge')
        self.server.register_function(self.get_transaction_status, 'get_transaction_status')
        self.server.register_function(self.submit_challenge, 'submit_challenge')
        self.server.register_function(self.get_winner, 'get_winner')
        self.server.register_function(self.get_seed, 'get_seed')

    def new_transaction(self):
        # choose a new random challenge that hasn't been chosen yet
        new_challenge = random.randint(1, 120)
        old_challenges = [t['challenge'] for t in self.transactions]

        while new_challenge in old_challenges and len(old_challenges) < 120:
            new_challenge = random.randint(1, 120)

        new_transaction = {'transaction_id': 0, 'challenge': new_challenge, 'seed': b'', 'winner': -1}
        self.transactions.append(new_transaction)
        self.current_transaction_id += 1

    # the transaction status is 1 if no one won yet and 0 if there is a winner
    def transaction_status(self, transaction_id : int):
        return 1 if self.transactions[transaction_id]['winner'] == -1 else 0

    def seed_valid(challenge : int, seed : int):
        hash_object = hashlib.sha1(seed.to_bytes(seed.bit_length(), 'big'))
        hashed = hash_object.digest()

        # the challenge is the number of '0's that must exist at the start of the hash
        mask = BitArray('0b' + '1'*challenge).tobytes()
        mask += (20-len(mask))*b'\00'

        # do bitwise xor between mask and hashed
        return not bool.from_bytes(bytes([h & m for h,m in zip(hashed, mask)]), 'big')

    def get_transaction_id(self):
        return self.current_transaction_id

    def get_challenge(self, transaction_id : int):
        if transaction_id <= self.current_transaction_id:
            return self.transactions[transaction_id]['challenge']
        else:
            return -1

    def get_transaction_status(self, transaction_id : int):
        if transaction_id <= self.current_transaction_id:
            return self.transaction_status(transaction_id)
        else:
            return -1


    def submit_challenge(self, transaction_id : int, client_id : int, seed : int):
        if transaction_id <= self.current_transaction_id:
            if self.transaction_status(transaction_id) == 0:
                return 2
            elif MockChainServer.seed_valid(self.transactions[transaction_id]['challenge'], seed):
                self.transactions[transaction_id]['winner'] = client_id
                self.transactions[transaction_id]['seed'] = seed
                self.new_transaction()
                return 1
            else:
                return 0
        else:
            return -1

    def get_winner(self, transaction_id : int):
        if transaction_id <= self.current_transaction_id:
            return self.transactions[transaction_id]['winner'] if self.transaction_status(transaction_id) == 0 else 0
        else:
            return -1

    def get_seed(self, transaction_id : int):
        if transaction_id <= self.current_transaction_id:
            return (self.transaction_status(transaction_id), self.transactions[transaction_id]['seed'], self.transactions[transaction_id]['challenge'])
        else:
            return -1

    def run(self):
        address = self.server.server_address
        print(f'Listening on {address[0]}:{address[1]}...')
        self.server.serve_forever()

if __name__ == "__main__":
    mock_chain_server = MockChainServer('0.0.0.0', 8000)
    mock_chain_server.run()
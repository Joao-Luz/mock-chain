from concurrent.futures import thread
from posixpath import split
from bitstring import BitArray
from multiprocessing import Pool, Value
import hashlib
import xmlrpc.client
import sys
import os

done = False

def parallel_init(args):
    global done
    done = args

def parallel_mine(n, mask, step):
    global done
    while not done.value:

        seed = n.to_bytes(n.bit_length(), 'big')
        hash_object = hashlib.sha1(seed)
        hashed = hash_object.digest()

        xor = bytes([h & m for h,m in zip(hashed, mask)])

        if not bool.from_bytes(xor, "big"):
            done.value = True
            return n
        
        n += step
    
    return None


class MockChainClient:
    def __init__(self, ip : str, port : int):
        self.connect_to_server(ip, port)

    def connect_to_server(self, ip : str, port : int):
        self.proxy = xmlrpc.client.ServerProxy(f'http://{ip}:{port}/')

    def get_transaction_id(self):
        transaction_id = self.proxy.get_transaction_id()
        print(transaction_id)

    def get_challenge(self, transaction_id : int):
        challenge = self.proxy.get_challenge(transaction_id)
        print(challenge)
    
    def get_transaction_status(self, transaction_id : int):
        status = self.proxy.get_transaction_status(transaction_id)
        print(status)

    def get_winner(self, transaction_id : int):
        winner = self.proxy.get_winner(transaction_id)
        print(winner)

    def get_seed(self, transaction_id : int):
        seed = self.proxy.get_seed(transaction_id)
        print(seed)

    def mine(self):
        transaction_id = self.proxy.get_transaction_id()
        challenge = self.proxy.get_challenge(transaction_id)

        # the challenge is the number of '0's that must exist at the start of the hash
        mask = BitArray('0b' + '1'*challenge).tobytes()
        mask += (20-len(mask))*b'\00'

        print(f'Mining for transaction {transaction_id} (challenge = {challenge})...')

        thread_count = os.cpu_count()
        res = [0 for _ in range(thread_count)]
        n = 0

        done = Value('b', False)
        with Pool(processes=thread_count, initializer=parallel_init, initargs=(done, )) as pool:
            res = pool.starmap(parallel_mine, [(n+i, mask, thread_count) for i in range(thread_count)])

            for r in res:
                if r != None:
                    print(f'Submitting seed {r}... ')
                    self.proxy.submit_challenge(transaction_id, 1, r)


        
    
    def print_help():
        print(
            "\n1 - getTransactionID: gets the current transaction id from the server\n"
            "\n2 - getChallenge <transactionID>: gets the challenge related to given transaction id\n"
            "\n3 - getTransactionStatus <transactionID>: gets the status of the given transaction id\n"
            "\n4 - getWinner <transactionID>: gets the winner of the transaction\n"
            "\n5 - getSeed <transactionID>: gets the seed for the given transaction id if the transaction was already won\n"
            "\n6 - mine: looks for the seed related to the current transaction\n"
            "\n7 - help: prints the help message again\n"
            "\n8 - exit: exit client\n"
        )


if __name__ == '__main__':
    n = len(sys.argv)
    
    if (n!=3):
        print("\nHow to use: <server_address> <port_number>\n")
        exit(-1)
    
    mock_chain_client = MockChainClient('0.0.0.0', 8000)

    MockChainClient.print_help()

    while True:
        command = input().split()

        if len(command) == 0: continue
        elif   command[0] in ['getTransactionID', '1']:                                         mock_chain_client.get_transaction_id()
        elif len(command) == 2 and command[0] in ['getChallenge', '2']: mock_chain_client.get_challenge(int(command[1]))
        elif len(command) == 2 and command[0] in ['getTransactionStatus', '3']:               mock_chain_client.get_transaction_status(int(command[1]))
        elif len(command) == 2 and command[0] in ['getWinner', '4']:                          mock_chain_client.get_winner(int(command[1]))
        elif len(command) == 2 and command[0] in ['getSeed', '5']:                            mock_chain_client.get_seed(int(command[1]))
        elif command[0] in ['mine', '6']:                                                     mock_chain_client.mine()
        elif command[0] in ['help', '7']:                                                     MockChainClient.print_help()
        elif command[0] in ['exit', '8']:                                                     break
        else:                                                                                 print('Unknown command')


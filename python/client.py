from posixpath import split
import xmlrpc.client
import sys

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

    def run(self):
        MockChainClient.print_help()

        while True:
            command = input().split()

            if   command[0] in ['getTransactionID', '1']:     self.get_transaction_id()
            elif command[0] in ['getChallenge', '2']:         self.get_challenge(int(command[1]))
            elif command[0] in ['getTransactionStatus', '3']: self.get_transaction_status(int(command[1]))
            elif command[0] in ['getWinner', '4']:            self.get_winner(int(command[1]))
            elif command[0] in ['getSeed', '5']:              self.get_seed(int(command[1]))
            elif command[0] in ['help', '7']:                 MockChainClient.print_help()
            elif command[0] in ['exit', '8']:                 break


if __name__ == '__main__':
    n = len(sys.argv)
    
    if (n!=3):
        print("\nHow to use: <server_address> <port_number>\n")
        exit(-1)
    
    mock_chain_client = MockChainClient('0.0.0.0', 8000)
    mock_chain_client.run()


from posixpath import split
import xmlrpc.client
import sys

n = len(sys.argv)
 
if (n!=3):
    print("\nHow to use: <server_address> <port_number>\n")
    exit(-1)

server_address = "http://" + sys.argv[1] + ":" + sys.argv[2] + "/"
proxy = xmlrpc.client.ServerProxy(server_address)

def print_help():
    print("""getTransactionID: gets the current transaction id from the server\n
            getChallenge <transactionID>: gets the challenge related to given transaction id\n
            getTransactionStatus <transactionID>: gets the status of the given transaction id\n
            getWinner <transactionID>: gets the winner of the transaction\n
            getSeed <transactionID>: gets the seed for the given transaction id if the transaction was already won\n
            mine: looks for the seed related to the current transaction\n""")

while True:
    command = input()

    if   'getTransactionID' in command: proxy.get_transaction_id()
    elif 'getChallenge' in command: proxy.get_challenge(command.split()[1])
    elif 'getTransactionStatus' in command: proxy.get_transaction_status(command.split()[1])

soma = proxy.add(int(sys.argv[3]), int(sys.argv[4]))
print("%s+%s=%s" % (sys.argv[3], sys.argv[4], soma))

sub = proxy.subtract(int(sys.argv[3]), int(sys.argv[4]))
print("%s-%s=%d" % (sys.argv[3], sys.argv[4], sub))
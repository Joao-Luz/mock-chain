# mock-chain

This is a silly little program that tries to emulate the `block-chain`

## How to run

### Python

To run the Python version, simply change into de `python/` directory and run:

    python server.py

This will run the server of the application. To run the client, run:

    python client.py <server_ip> <port>

Where `<server_ip>` is the ip where the server is hosted and `<port>` is the respective port.

### C

To run the C version, go to te `c/`directory and run:

    make

This will generate the `mock_chain_server` and `mock_chain_client` executables. Now, run:

    ./mock_chain_server
    ./mock_chain_client <server_ip>

## User interface

The interface is pretty simple: run the available commands from the terminal. Both applications should have simmilar menus printed when you start the client. There are, basically, 6 main commands:

- `getTransactionID`: this will print the current transaction id of the mock-chain;
- `getChallenge <transactionID>`: this will print the respective transaction's challenge;
- `getTransactionStatus <transactionID>`: will print the status of the given transaction id (1 if there are no winners and 0 otherwise);
- `getWinner <transactionID>`: gets the winner of the transaction (the respective client id);
- `getSeed <transactionID>`: gets the seed for the given transaction id if the challenge was won;
- `mine`: looks for the seed related to the current transaction and submits to the server.

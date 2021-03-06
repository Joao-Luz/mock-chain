#include "mock_chain.h"

#include <stdlib.h>
#include "utils.h"
#include "sha1.h"

typedef struct {
	int transaction_id;
	int challenge;
	int seed;
	int winner;
} transaction_t;

transaction_t transactions[120];
int current_transaction_id = -1;

int transaction_status(int transaction_id) {
	return transactions[transaction_id].winner == -1 ? 1 : 0;
}

int new_challenge() {
	int new_challenge = rand()%120;
	
	int in_old_challenges = 0;
	do {
		for (int i = 0; i < current_transaction_id; i++) {
			if (new_challenge == transactions[i].challenge) {
				in_old_challenges = 1;
				new_challenge = rand()%120;
			}
		}
	} while (in_old_challenges);

	return new_challenge;
}

int seed_valid(int seed, int challenge) {
	unsigned char mask[20] = {0};
	create_mask(mask, challenge);

	unsigned char hashed_seed[20];
	sha1digest(hashed_seed, NULL, (uint8_t*)(&seed), sizeof(seed));

	return and_mask(hashed_seed, mask, 20);
}

void new_transaction() {
	int n_c = new_challenge();

	transaction_t transaction = {
		++current_transaction_id,
		n_c,
		0,
		-1
	};

	printf("Created new transaction with challenge %d\n", n_c);
	transactions[current_transaction_id] = transaction;

}

// RPC procedures

int* get_transaction_id_100_svc(void *argp, struct svc_req *rqstp)
{	
	static int result;

	if (current_transaction_id == -1) {
		new_transaction();
	}
	result = current_transaction_id;

	return &result;
}

int* get_challenge_100_svc(int *argp, struct svc_req *rqstp)
{
	static int result;

	if (current_transaction_id == -1) {
		new_transaction();
	}

	int transaction_id = *argp;

	if (transaction_id > current_transaction_id) result = -1;
	else result = transactions[transaction_id].challenge;

	return &result;
}

int* get_transaction_status_100_svc(int *argp, struct svc_req *rqstp)
{
	static int result;

	if (current_transaction_id == -1) {
		new_transaction();
	}

	int transaction_id = *argp;
	if (transaction_id > current_transaction_id) result = -1;
	else result = transaction_status(transaction_id);

	return &result;
}

int* submit_challenge_100_svc(submission_t *argp, struct svc_req *rqstp)
{
	static int result;

	if (current_transaction_id == -1) {
		new_transaction();
	}

	submission_t submission = *argp;
	int transaction_id = submission.transaction_id;

	if (transaction_id > current_transaction_id) result = -1;
	else if (!transaction_status(current_transaction_id)) {
		result = 2;
	}
	else {
		int client_id = submission.client_id;
		int seed = submission.seed;
		int challenge = transactions[transaction_id].challenge;

		if (seed_valid(seed, challenge)) {
			transactions[transaction_id].winner = client_id;
			transactions[transaction_id].seed = seed;
			new_transaction();
			result = 1;

			printf("Transaction %d won by %d with key %d\n", current_transaction_id, client_id, seed);
		} else {
			result = 0;
		}
	}

	return &result;
}

int* get_winner_100_svc(int *argp, struct svc_req *rqstp)
{
	static int result;

	if (current_transaction_id == -1) {
		new_transaction();
	}

	int transaction_id = *argp;
	if (transaction_id > current_transaction_id) result = -1;
	else {
		result = transaction_status(transaction_id) ? 0 : transactions[transaction_id].winner;
	}

	return &result;
}

status_t* get_seed_100_svc(int *argp, struct svc_req *rqstp)
{
	static status_t result;

	if (current_transaction_id == -1) {
		new_transaction();
	}

	int transaction_id = *argp;
	if (transaction_id > current_transaction_id)
		result = (status_t){-1, -1, -1};
	else {
		result = (status_t){
			transaction_status(transaction_id),
			transactions[transaction_id].seed,
			transactions[transaction_id].challenge
		};
	}

	return &result;
}

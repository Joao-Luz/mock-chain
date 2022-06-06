struct submission_t {
	int transaction_id;
	int client_id;
	int seed;
};

struct status_t {
	int status;
	int seed;
	int challenge;
};

program mock_chain { 
	version v { 
		int get_transaction_id() = 1; 
		int get_challenge(int) = 2;
		int get_transaction_status(int) = 3;
		int submit_challenge(submission_t) = 4;
		int get_winner(int) = 5;
		status_t get_seed(int) = 6;
	} = 100;
} = 55555555;


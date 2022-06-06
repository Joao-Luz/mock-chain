/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#ifndef _MOCK_CHAIN_H_RPCGEN
#define _MOCK_CHAIN_H_RPCGEN

#include <rpc/rpc.h>


#ifdef __cplusplus
extern "C" {
#endif


struct submission_t {
	int transaction_id;
	int client_id;
	int seed;
};
typedef struct submission_t submission_t;

struct status_t {
	int status;
	int seed;
	int challenge;
};
typedef struct status_t status_t;

#define mock_chain 55555555
#define v 100

#if defined(__STDC__) || defined(__cplusplus)
#define get_transaction_id 1
extern  int * get_transaction_id_100(void *, CLIENT *);
extern  int * get_transaction_id_100_svc(void *, struct svc_req *);
#define get_challenge 2
extern  int * get_challenge_100(int *, CLIENT *);
extern  int * get_challenge_100_svc(int *, struct svc_req *);
#define get_transaction_status 3
extern  int * get_transaction_status_100(int *, CLIENT *);
extern  int * get_transaction_status_100_svc(int *, struct svc_req *);
#define submit_challenge 4
extern  int * submit_challenge_100(submission_t *, CLIENT *);
extern  int * submit_challenge_100_svc(submission_t *, struct svc_req *);
#define get_winner 5
extern  int * get_winner_100(int *, CLIENT *);
extern  int * get_winner_100_svc(int *, struct svc_req *);
#define get_seed 6
extern  status_t * get_seed_100(int *, CLIENT *);
extern  status_t * get_seed_100_svc(int *, struct svc_req *);
extern int mock_chain_100_freeresult (SVCXPRT *, xdrproc_t, caddr_t);

#else /* K&R C */
#define get_transaction_id 1
extern  int * get_transaction_id_100();
extern  int * get_transaction_id_100_svc();
#define get_challenge 2
extern  int * get_challenge_100();
extern  int * get_challenge_100_svc();
#define get_transaction_status 3
extern  int * get_transaction_status_100();
extern  int * get_transaction_status_100_svc();
#define submit_challenge 4
extern  int * submit_challenge_100();
extern  int * submit_challenge_100_svc();
#define get_winner 5
extern  int * get_winner_100();
extern  int * get_winner_100_svc();
#define get_seed 6
extern  status_t * get_seed_100();
extern  status_t * get_seed_100_svc();
extern int mock_chain_100_freeresult ();
#endif /* K&R C */

/* the xdr functions */

#if defined(__STDC__) || defined(__cplusplus)
extern  bool_t xdr_submission_t (XDR *, submission_t*);
extern  bool_t xdr_status_t (XDR *, status_t*);

#else /* K&R C */
extern bool_t xdr_submission_t ();
extern bool_t xdr_status_t ();

#endif /* K&R C */

#ifdef __cplusplus
}
#endif

#endif /* !_MOCK_CHAIN_H_RPCGEN */

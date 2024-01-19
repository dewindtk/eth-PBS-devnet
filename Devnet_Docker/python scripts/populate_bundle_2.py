import requests
from sseclient import SSEClient
import time
import json

# Replace these URLs with your actual endpoint URLs
sse_endpoint_url = 'http://localhost:3500/eth/v1/events?topics=block'
send_request_url = 'http://localhost:8558'
wallets = ["0x124a35b68b409f73d8ccf5a0c9fa0c4b4d282299","0x2f680e617db77623bf3ed7b5b142ee47c099bfa0","0x051737c2ebd3ef38ada6900fa399f62c0aa0694b","0xbd4ed6425c04facd2d254e8dd05e43ea29eab585","0x0879a76817bfba1c75d2b8ede79023dcf0a3013e","0x475db58cd202e3530943019fc821999e82da0c22","0x722821c7b310d52456ab91d615a0f2fb3a0fb86b","0xae736c8e04068d4824ad72babfd3af0e10b90281","0xa668440fbeda974f466e73b6fcc9e7285022f054","0x227bad465465968bbbbe469485bbc0c725fe5363"]
# wallets = ["0x124a35b68b409f73d8ccf5a0c9fa0c4b4d282299"]

def bundle_transfer(event, wei):
    # Customize this function to process the SSE event data
    print('Received SSE event:')
    print(f'Event ID: {event.event}')
    print(f'Data: {event.data}')
    print('\n')

    for i in range(len(wallets)):

        response = requests.post(send_request_url, json={"method":"eth_getTransactionCount","params":[wallets[i], "latest"],"id":1,"jsonrpc":"2.0"})
        nonce = response.json().get("result")

        tx = {"from": wallets[i], "to": "0x2220000000000000000000000000000000000000", "value": hex(wei), "gas": hex(21000), "gasPrice": hex(10000000000), "nonce": nonce}

        response = requests.post(send_request_url, json={"jsonrpc": "2.0","id": 1,"method": "eth_signTransaction","params": [tx]})
        signature = response.json().get("result").get("raw")

        response = requests.post(send_request_url, json={"method":"eth_blockNumber","params":[],"id":1,"jsonrpc":"2.0"})
        block = hex(int(response.json().get("result"), 16)+1)

        # Example: Send a request to another endpoint when an event occurs
        payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_sendBundle",
        "params": [{
            "txs" : [
                signature
            ],
            "blockNumber" : block
            }]}
        
        response = requests.post(send_request_url, json=payload)
        print(f'Response from sending request: {response.status_code} {response.text}')
        print("BUNDLE SENT", i, int(block, 16), "nonce", hex(int(nonce, 16)))
        time.sleep(0.9)




sse_client = SSEClient(sse_endpoint_url)
blockcount = 0
for event in sse_client:
    if blockcount < 100:
        bundle_transfer(event, 10000000000000000) #0.01
        blockcount +=1 
    else:
        print("Blockcountn 100 reacjed")

#     @@INCREASE GAS instead of NONCE then.
# or make 10 wallets transfering to same wallet
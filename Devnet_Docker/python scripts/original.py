import requests
from sseclient import SSEClient
import time
import json

# Replace these URLs with your actual endpoint URLs
sse_endpoint_url = 'http://localhost:3500/eth/v1/events?topics=block'
send_request_url = 'http://localhost:8549'

def bundle_transfer(event, wei):
    # Customize this function to process the SSE event data
    print('Received SSE event:')
    print(f'Event ID: {event.event}')
    print(f'Data: {event.data}')
    print('\n')

    for i in range(10):

        response = requests.post(send_request_url, json={"method":"eth_getTransactionCount","params":["0x8fe74459a3ad9d1380ead0e8d2b39509ea455dd9", "latest"],"id":1,"jsonrpc":"2.0"})
        nonce = response.json().get("result")

        tx = {"from": "0x8fe74459a3ad9d1380ead0e8d2b39509ea455dd9", "to": "0x8fe74459a3ad9d1380ead0e8d2b39509ea455dd8", "value": hex(wei), "gas": hex(22000), "gasPrice": hex(10000000000), "nonce": hex(int(nonce, 16)+i)}

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
        print("BUNDLE SENT", i, int(block, 16), "nonce", hex(int(nonce, 16)+i))
        time.sleep(0.9)




sse_client = SSEClient(sse_endpoint_url)
for event in sse_client:
    bundle_transfer(event, 10000000000000000) #0.01

#     @@INCREASE GAS instead of NONCE then.
# or make 10 wallets transfering to same wallet
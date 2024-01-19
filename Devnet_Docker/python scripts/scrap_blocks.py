import requests
from sseclient import SSEClient
import time
import json

# Replace these URLs with your actual endpoint URLs
send_request_url = 'http://localhost:8545'
wallets = ["124a35b68b409f73d8ccf5a0c9fa0c4b4d282299","2f680e617db77623bf3ed7b5b142ee47c099bfa0","051737c2ebd3ef38ada6900fa399f62c0aa0694b","bd4ed6425c04facd2d254e8dd05e43ea29eab585","0879a76817bfba1c75d2b8ede79023dcf0a3013e","475db58cd202e3530943019fc821999e82da0c22","722821c7b310d52456ab91d615a0f2fb3a0fb86b","ae736c8e04068d4824ad72babfd3af0e10b90281","a668440fbeda974f466e73b6fcc9e7285022f054","227bad465465968bbbbe469485bbc0c725fe5363"]


def scrap_blocks(start, num):

    result = {}

    for i in range(num):

        print("Scrapping block", start + i)

        response = requests.post(send_request_url, json={"method":"eth_getBlockByNumber","params":[hex(start+i), "false"],"id":1,"jsonrpc":"2.0"})
        txs = response.json().get("result")
        print(txs)
        
        blockres = [0,0]
        if txs is not None:
            for tx in txs:
                response = requests.post(send_request_url, json={"method":"eth_getTransactionByHash","params":[tx],"id":1,"jsonrpc":"2.0"})
                txdata = response.json().get("result")
                txto = txdata.get("to")
                if txto == "0x1110000000000000000000000000000000000000":
                    blockres[0] = blockres[0]+1
                elif txto == "0x2220000000000000000000000000000000000000":
                    blockres[1] = blockres[1]+1
            result[start+1] = blockres

    return result

print(scrap_blocks(271, 5))

#     @@INCREASE GAS instead of NONCE then.
# or make 10 wallets transfering to same wallet
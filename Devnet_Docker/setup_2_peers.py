import requests
import json

# Fetch the bootnode address from the admin_nodeInfo RPC method at localhost:8545
response = requests.post("http://localhost:8545",
                        json={"jsonrpc": "2.0", "method": "admin_nodeInfo", "params": [], "id": 1},
                        headers={"Content-Type": "application/json"})
bootnode_addy = json.loads(response.text)["result"]["enode"]

# Prepare the JSON data for the admin_addPeer RPC method
json_data = {
    "jsonrpc": "2.0",
    "method": "admin_addPeer",
    "params": [bootnode_addy],
    "id": 1
}

# Send the admin_addPeer request to the RPC server at localhost:8547
rpc_url = "http://localhost:8547"
response = requests.post(rpc_url, json=json_data, headers={"Content-Type": "application/json"})

# Print the response from the admin_addPeer request
print(json.loads(response.text))
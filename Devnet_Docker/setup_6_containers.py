import requests
import subprocess
import shutil

# Fetch the peer address from the enode endpoint at localhost:8080/p2p
response = requests.get("http://localhost:8080/p2p")
peer_addy = "/ip4/" + response.text.split("/ip4/")[1].split(" ")[0].split("\n")[0]
print(peer_addy)

# Fetch the bootnode address from the admin_nodeInfo RPC method at localhost:8545
payload = {"jsonrpc": "2.0", "method": "admin_nodeInfo", "params": [], "id": 1}
headers = {"Content-Type": "application/json"}
response = requests.post("http://localhost:8545", json=payload, headers=headers)
bootnode_addy = response.json()["result"]["enode"]
print(bootnode_addy)

# Change the `ENV_PEER_ADDY` and `ENV_BOOTNODE_ADDY` environment variables in the Network_1x3-2.yml file
with open("devnet_2x1x3/Devnet-1x3-Four/Network_1x3-4.yml", "r") as f:
    contents = f.read()
    contents = contents.replace("ENV_PEER_ADDY", peer_addy)
    contents = contents.replace("ENV_BOOTNODE_ADDY", bootnode_addy)

with open("devnet_2x1x3/Devnet-1x3-Four/Network_1x3-4.yml", "w") as f:
    f.write(contents)

# Copy the genesis.json file from the Devnet-1x3-One/execution directory to the Devnet-1x3-Two/execution directory
shutil.copy("devnet_2x1x3/Devnet-1x3-One/execution/genesis.json", "devnet_2x1x3/Devnet-1x3-Four/execution/")

# Start the Docker containers for the Devnet-1x3-Two network in the background
subprocess.run(["docker-compose", "-f", "devnet_2x1x3/Devnet-1x3-Four/Network_1x3-4.yml", "up", "-d"])
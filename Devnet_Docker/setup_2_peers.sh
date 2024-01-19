bootnode_addy=$(curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0","method": "admin_nodeInfo","params": [],"id":1}' http://localhost:8545 | jq '.result.enode' | tr -d '"')
bootnode_addy_q=$bootnode_addy

json_data='{
	"jsonrpc": "2.0",
	"method": "admin_addPeer",
	"params": ["'"$bootnode_addy"'"],
	"id":1
}'

echo "$json_data"

rpc_url=http://localhost:8547
resp=$(curl -X POST --data "$json_data" -H "Content-Type: application/json" "$rpc_url")
echo $resp
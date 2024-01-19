peer_addy2=$(curl -s localhost:8080/p2p | grep -o -m 1 '/ip4/[^ ]*')
bootnode_addy2=$(curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0","method": "admin_nodeInfo","params": [],"id":1}' http://localhost:8545 | jq '.result.enode' | tr -d '"')

cd devnet_2x1x3/Devnet-1x3-Three

sed -i "s#ENV_PEER_ADDY#$peer_addy2#g" Network_1x3-3.yml
sed -i "s#ENV_BOOTNODE_ADDY#$bootnode_addy2#g" Network_1x3-3.yml

cd ..

cp Devnet-1x3-One/execution/genesis.json Devnet-1x3-Three/execution/

cd Devnet-1x3-Three

docker compose -f Network_1x3-3.yml up -d
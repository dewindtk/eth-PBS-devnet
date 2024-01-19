@echo off
rmdir /s /q devnet_2x1x3
xcopy /e Template_Devnet_2x1x3\* devnet_2x1x3
cd devnet_2x1x3\Devnet-1x3-One

docker-compose -f Network_1x3.yml down --remove-orphans
docker network create --subnet=172.23.0.0/24 --driver=bridge pleasework

timeout /t 3 /nobreak > nul

docker-compose -f Network_1x3.yml up -d
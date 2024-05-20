#Makefile

install:
	poetry install

PORT ?= 8000	
start_server:
	poetry run python xml_rpc/server.py

start_client:
	poetry run python xml_rpc/client.py

lint:
	poetry run flake8 xml_rpc
	
build:
	./build.sh

init_run_server: build start_server
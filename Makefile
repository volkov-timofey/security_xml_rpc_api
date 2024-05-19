#Makefile

install:
	poetry install

PORT ?= 8000	
#start_server:
	#poetry run python page_analyzer:app

#start_client:
	#poetry run python page_analyzer:app

lint: # run_linter
	poetry run flake8 xml_rpc
	
build:
	./build.sh
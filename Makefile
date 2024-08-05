# This is the main Makefile for managing all the projects from the root directory.
# See each project's Makefile for more details or refer to repo's the Readme.

SHELL := /bin/bash

PROJECT_ROOT=$(shell pwd)
PROJECT_SERVER=$(PROJECT_ROOT)/modeling
PROJECT_CLIENT=$(PROJECT_ROOT)/client

# Load .env file variables
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

setup:
	sudo apt update && \
	sudo apt install python3 python3-venv python3-pip pre-commit -y && \
	pre-commit install && \
	cp .env $(PROJECT_SERVER)/.env && \
	cp serviceAdmin.json $(PROJECT_SERVER)/private/serviceAdmin.json && \
	$(MAKE) -C $(PROJECT_SERVER) configure

# Rules to run specific commands of each project
model_%:
	@$(MAKE) -C $(PROJECT_SERVER) $(patsubst model_%,%,$@)

client_%:
	@$(MAKE) -C $(PROJECT_CLIENT) $(patsubst client_%,%,$@)

# Rule to run specific commands in all subprojects
all_%:
	@$(MAKE) -C $(PROJECT_SERVER) $(patsubst all_%,%,$@)
	@$(MAKE) -C $(PROJECT_CLIENT) $(patsubst all_%,%,$@)

# Prevent make from interpreting the command as a file name
%:
	@:
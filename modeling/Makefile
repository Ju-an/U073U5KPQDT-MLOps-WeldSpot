
SHELL := /bin/bash
PROJECT_PATH=$(shell pwd)
PARENT_MAKEFILE=../Makefile
DOCKER_IMAGE_NAME=modeling_image

# Load .env file variables
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

setup:
	$(MAKE) -f $(PARENT_MAKEFILE) setup

clean:
	rm -rf .venv
#	rm .env $(DOCKER_IMAGE_NAME).tar private

# Setup the dependencies
configure:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	python3 -m pip install -U pip && \
	pip install -r requirements.txt && \
	prefect cloud login --key $$PREFECT_CLOUD_API_KEY && \
	mkdir -p logs/fit && \
	mkdir -p logs/predict && \
	mkdir -p data/ && \
	mkdir -p data/raw/ && \
	mkdir -p data/processed/ && \
	mkdir -p data/augmented/ && \
	mkdir -p data/initial/ && \
	mkdir -p data/splits/ && \
	mkdir -p models/ && \
	mkdir -p models/best && \
	mkdir -p models/deploy

quality:
	source .venv/bin/activate && \
	PYTHONPATH=$(PROJECT_PATH) isort . && \
	PYTHONPATH=$(PROJECT_PATH) black . && \
	PYTHONPATH=$(PROJECT_PATH) pylint --recursive=y .

unit_tests:
	source .venv/bin/activate && \
	PYTHONPATH=$(PROJECT_PATH) pytest tests/

integration_test:
	source .venv/bin/activate && \
	echo "Testing dataset service" && \
	PYTHONPATH=$(PROJECT_PATH) python flows/collection_pipeline.py && \
	echo "Testing model service" && \
	PYTHONPATH=$(PROJECT_PATH) python flows/training_pipeline.py

build_image:
	docker build -t $(DOCKER_IMAGE_NAME) .

export_image: build_image
	docker save -o $(DOCKER_IMAGE_NAME).tar $(DOCKER_IMAGE_NAME)

run_image: build_image
	docker run -it $(DOCKER_IMAGE_NAME)

run_app:
	source .venv/bin/activate && \
	PYTHONPATH=$(PROJECT_PATH) python3 app.py

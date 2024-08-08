
SHELL := /bin/bash
PROJECT_PATH=$(shell pwd)
PARENT_MAKEFILE=../Makefile

export PATH="$(HOME)/fluttersdk/bin:$(PATH)"
export NVM_DIR="$(HOME)/.nvm"

# Load .env file variables
ifneq (,$(wildcard ../.env))
    include .env
    export
endif

.PHONY: icon
icon:
	dart run flutter_launcher_icons

setup:
	$(MAKE) -f $(PARENT_MAKEFILE) setup

configure:
	# Firebase CLI
	echo "CONFIGURING FLUTTER PROJECT WITH FIREBASE" && \
	sudo npm install -g firebase-tools && \
	dart pub global activate flutterfire_cli && \
	dart --disable-analytics && \
	export PATH="$(PATH)":"$(HOME)/.pub-cache/bin:/mnt/c/Windows/system32"

register:
	firebase login --no-localhost && \
	flutterfire configure --project=$$FIREBASE_PROJECT_NAME && \
	firebase init

emulate:
	firebase emulators:start

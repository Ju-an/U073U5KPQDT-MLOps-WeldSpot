
SHELL := /bin/bash
PROJECT_PATH=$(shell pwd)
PARENT_MAKEFILE=../Makefile

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
	export PATH=$(HOME)/fluttersdk/bin:$$PATH && \
	export PATH="$$PATH:$(HOME)/.pub-cache/bin:/mnt/c/Windows/system32" && \
	sudo npm install -g firebase-tools && \
	dart --disable-analytics && \
	dart pub global activate flutterfire_cli

register:
	firebase login --no-localhost && \
	export PATH=$(HOME)/fluttersdk/bin:$$PATH && \
	export PATH="$$PATH:$(HOME)/.pub-cache/bin:/mnt/c/Windows/system32" && \
	flutterfire configure --project=$$FIREBASE_PROJECT_NAME && \
	firebase init && \
	flutter clean && \
	flutter pub get

build_apk:
	export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64" && \
	export PATH=$$JAVA_HOME/bin:$$PATH && \
	export PATH=$(HOME)/fluttersdk/bin:$$PATH && \
	export PATH="$$PATH:$(HOME)/.pub-cache/bin:/mnt/c/Windows/system32" && \
	flutter build apk --release --split-per-abi

build_apk_debug:
	export JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64" && \
	export PATH=$$JAVA_HOME/bin:$$PATH && \
	export PATH=$(HOME)/fluttersdk/bin:$$PATH && \
	export PATH="$$PATH:$(HOME)/.pub-cache/bin:/mnt/c/Windows/system32" && \
	flutter build apk --debug

emulate:
	firebase emulators:start

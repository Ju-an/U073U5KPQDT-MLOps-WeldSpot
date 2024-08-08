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

dependencies_main:
	echo "[WELDSPOT] INSTALLING PYTHON AND PRECOMMIT" && \
	sudo apt update -y && sudo apt upgrade -y && \
	sudo apt install python3 python3-venv python3-pip pre-commit -y && \
	pre-commit install

dependencies_client:
	echo "[WELDSPOT] INSTALLING FLUTTER+ANDROID REQUIREMENTS" && \
	sudo apt install -y curl git unzip xz-utils zip libglu1-mesa && \
	sudo apt install -y libc6:amd64 libstdc++6:amd64 libbz2-1.0:amd64 && \
	sudo apt install -y lib32z1 libgtk-3-dev && \
	sudo apt install -y android-sdk android-sdk-build-tools && \
	sudo apt install -y clang cmake ninja-build pkg-config libgtk-3-dev && \
	sudo apt install -y openjdk-17-jdk && \
	wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O commandlinetools.zip && \
	mkdir -p $(HOME)/Android/cmdline-tools && \
	unzip commandlinetools.zip -d $(HOME)/Android/ && \
	export PATH="$(HOME)/Android/cmdline-tools/bin:$$PATH" && \
	rm commandlinetools.zip

dependencies_flutter:
	echo "[WELDSPOT] INSTALLING FLUTTER & ANDROID SDKs" && \
	wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.22.3-stable.tar.xz && \
	tar xf flutter_linux_3.22.3-stable.tar.xz && \
	mv flutter $(HOME)/fluttersdk && \
	export PATH="$(HOME)/fluttersdk/bin:$$PATH" && \
	rm flutter_linux_3.22.3-stable.tar.xz && \
	flutter precache && \
	flutter --disable-analytics && \
	mkdir -p $(HOME)/Android/sdk/ && \
	yes | $(HOME)/Android/cmdline-tools/bin/sdkmanager --sdk_root=$(HOME)/Android/sdk "platform-tools" "platforms;android-34" "build-tools;34.0.0" "cmdline-tools;latest" && \
	flutter config --android-sdk $(HOME)/Android/sdk && \
	yes | $(HOME)/Android/cmdline-tools/bin/sdkmanager --sdk_root=$(HOME)/Android/sdk --licenses && \
	yes | flutter doctor --android-licenses && \
	flutter doctor

dependencies_firebase:
	echo "[WELDSPOT] INSTALLING FIREBASE TOOLS" && \
	sudo apt update && \
	sudo apt purge -y nodejs npm && \
	sudo apt remove --purge nodejs npm -y && \
	sudo apt autoremove -y && \
	sudo apt autoclean && \
	sudo apt update && \
	sudo apt install -y curl software-properties-common && \
	curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && \
	sudo apt update && sudo apt install nodejs -y

setup: dependencies_main dependencies_client dependencies_flutter dependencies_firebase
	echo "[WELDSPOT] SETUP DONE; CONFIGURING INDIVIDUAL PROJECTS"
	cp .env $(PROJECT_SERVER)/.env && \
	mkdir -p $(PROJECT_SERVER)/private && \
	cp serviceAdmin.json $(PROJECT_SERVER)/private/serviceAdmin.json && \
	$(MAKE) -C $(PROJECT_SERVER) configure && \
	cp .env $(PROJECT_CLIENT)/.env && \
	$(MAKE) -C $(PROJECT_CLIENT) configure && \
	echo "[WELDSPOT] SETUP FINISHED SUCCESSFULLY"

# Rules to run specific commands of each project (e.g., make model_quality is equivalent to make quality in modeling subfolder)
model_%:
	@$(MAKE) -C $(PROJECT_SERVER) $(patsubst model_%,%,$@)

client_%:
	@$(MAKE) -C $(PROJECT_CLIENT) $(patsubst client_%,%,$@)

# Rule to run specific commands in all subprojects (e.g., make all_configure will call both modeling and client make configure)
all_%:
	@$(MAKE) -C $(PROJECT_SERVER) $(patsubst all_%,%,$@)
	@$(MAKE) -C $(PROJECT_CLIENT) $(patsubst all_%,%,$@)

# Prevent make from interpreting the command as a file name
%:
	@:

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
	echo "INSTALLING PYTHON AND PRECOMMIT" && \
	sudo apt update -y && sudo apt upgrade -y && \
	sudo apt install python3 python3-venv python3-pip pre-commit -y && \
	pre-commit install

dependencies_client:
	echo "INSTALLING FLUTTER+ANDROID REQUIREMENTS" && \
	sudo apt install -y curl git unzip xz-utils zip libglu1-mesa && \
	sudo apt install -y libc6:amd64 libstdc++6:amd64 libbz2-1.0:amd64 && \
	sudo apt install -y lib32z1 libgtk-3-dev && \
	sudo apt install -y android-sdk android-sdk-build-tools && \
	sudo apt install -y clang cmake ninja-build pkg-config libgtk-3-dev

dependencies_flutter:
	echo "INSTALLING FLUTTER & ANDROID SDKs" && \
	wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.22.3-stable.tar.xz && \
	tar xf flutter_linux_3.22.3-stable.tar.xz && \
	mv flutter $HOME/fluttersdk && \
	export PATH="$HOME/fluttersdk/bin:$PATH" && \
	flutter --disable-analytics && \
	flutter precache && \
	rm flutter_linux_3.22.3-stable.tar.xz && \
	sudo apt install google-android-build-tools-34.0.0-installer google-android-cmdline-tools-10.0-installer && \
	mkdir -p $HOME/Android/sdk/ && \
	sdkmanager --sdk_root=$HOME/Android/sdk "platform-tools" "platforms;android-34" "build-tools;34.0.0" "cmdline-tools;latest" && \
	flutter config --android-sdk $HOME/Android/sdk && \
	yes | sdkmanager --licenses && \
	flutter doctor --android-licenses && \
	flutter doctor

dependencies_firebase:
	echo "INSTALLING FIREBASE TOOLS" && \
	sudo apt update && \
	sudo apt purge nodejs && \
	sudo apt purge npm && \
	curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.7/install.sh | bash && \
	export NVM_DIR="$HOME/.nvm" && \
	[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm && \
	[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion && \
	nvm install 20 && \
	node -v # should print `v20.16.0` && \
	npm -v # should print `10.8.1`

setup: dependencies_main dependencies_client dependencies_flutter dependencies_firebase
	echo "SETUP DONE; CONFIGURING INDIVIDUAL PROJECTS"
	cp .env $(PROJECT_SERVER)/.env && \
	cp serviceAdmin.json $(PROJECT_SERVER)/private/serviceAdmin.json && \
	$(MAKE) -C $(PROJECT_SERVER) configure && \
	cp .env $(PROJECT_CLIENT)/.env && \
	$(MAKE) -C $(PROJECT_CLIENT) configure

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

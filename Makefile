TOOLSET_IMAGE_REPO := $(shell test -f files/registries/toolsets && cat files/registries/toolsets || echo "ghcr.io/jrosco/asdf-toolset")
TOOLSET_DIRS := $(filter-out toolset-docker-images/README.md,$(shell find toolset-docker-images/* -maxdepth 0 -type d))
TOOLSET_BUILD_TARGETS := $(notdir $(TOOLSET_DIRS))
PARALLELISM := 3

# Define a variable to store the Git tag of the current directory
GIT_TAG := $(shell git describe --tags --always --abbrev=0)
# Export the Git tag as an environment variable
export GIT_TAG

.PHONY: all build push build-toolsets push-toolsets ln-env-toolsets setup-buildx build-multiplatform push-multiplatform

all: build push

toolsets: build-toolsets push-toolsets

build:
	@docker compose build

push:
	@docker compose --parallel $(PARALLELISM) build --push

clean:
	@docker compose down --rmi all

build-toolsets: ln-env-toolsets
	@for target in $(TOOLSET_BUILD_TARGETS); do \
		echo "Building $$target"; \
		docker compose -f ./toolset-docker-images/$$target/docker-compose.yaml build || { echo "Error building $$target"; exit 1; }; \
	done

push-toolsets:
	@for target in $(TOOLSET_BUILD_TARGETS); do \
		echo "Pushing $(TOOLSET_IMAGE_REPO):$$target"; \
		docker compose --parallel $(PARALLELISM) -f ./toolset-docker-images/$$target/docker-compose.yaml build --push || { echo "Error pushing $$target"; exit 1; }; \
	done

clean-toolsets:
	@for target in $(TOOLSET_BUILD_TARGETS); do \
		echo "Remove $(TOOLSET_IMAGE_REPO):$$target"; \
		docker compose down --rmi all || { echo "Error pushing $$target"; exit 1; }; \
	done

ln-env-toolsets:
	@for target in $(TOOLSET_BUILD_TARGETS); do \
		if [ ! -e ./toolset-docker-images/$$target/.env ]; then \
			echo "Linking environment file with $$target"; \
			ln -s ../../config/environment ./toolset-docker-images/$$target/.env 2>/dev/null || { echo "Error linking $$target"; exit 1; }; \
		else \
			echo ".env file already exists in $$target, skipping..."; \
		fi \
	done

# Multi-platform build targets

setup-buildx:
	@echo "Setting up Docker Buildx with multi-platform support..."
	@docker buildx create --name asdf-builder --platform linux/amd64,linux/arm64,linux/arm/v7 2>/dev/null || true
	@docker buildx use asdf-builder
	@echo "Buildx builder 'asdf-builder' is ready"

build-multiplatform: setup-buildx
	@echo "Building images for multiple platforms..."
	@export DOCKER_BUILDKIT=1 && docker compose build

push-multiplatform: setup-buildx
	@echo "Pushing images to registry for multiple platforms..."
	@export DOCKER_BUILDKIT=1 && docker compose --parallel $(PARALLELISM) build --push

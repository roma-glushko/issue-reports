CLUSTER?=coredis
REGISTRY_PORT?=8800
SOURCE?=common services

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

cluster-start:  ## Start the cluster
	@k3d cluster create $(CLUSTER) --agents 1 \
		--registry-create $(CLUSTER)-registry:0.0.0.0:$(REGISTRY_PORT) \
		--kubeconfig-update-default --kubeconfig-switch-context

cluster-ctx:  ## Configure the cluster context
	@kubectl config set current-context k3d-$(CLUSTER)

cluster-stop: ## Stop the cluster
	@k3d cluster delete $(CLUSTER)

start: cluster-ctx ## Start the whole system
	@tilt up

image-build: ## Build the image
	@docker build -t sample/service:dev -f Dockerfile .

lint: ## Lint source code
	@poetry run black $(SOURCE)
	@poetry run ruff --fix $(SOURCE)
	@poetry run mypy --pretty $(SOURCE)
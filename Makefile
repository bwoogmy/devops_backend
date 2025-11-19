.PHONY: help build build-no-cache push load-kind install upgrade uninstall template lint test unit-test port-forward logs status history rollback clean

# Variables
IMAGE_NAME = devops-backend
IMAGE_TAG = latest
REGISTRY = ghcr.io/bwoogmy
CHART_NAME = backend
RELEASE_NAME = backend
NAMESPACE = backend
KIND_CLUSTER = devops-cluster

help:
	@echo "Available commands:"
	@echo ""
	@echo "Docker commands:"
	@echo "  make build         - Build Docker image"
	@echo "  make build-no-cache - Build without cache"
	@echo "  make push          - Push image to registry"
	@echo ""
	@echo "Test commands:"
	@echo "  make unit-test     - Run unit tests in Docker"
	@echo "  make lint          - Lint Helm chart"

build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

push:
	@echo "Pushing Docker image to registry..."
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

unit-test:
	@echo "Running unit tests in Docker..."
	docker run --rm -v $(PWD):/app -w /app python:3.10-slim sh -c "pip install --quiet -r requirements.txt && pytest tests/ -v"

lint:
	@echo "Linting Helm chart..."
	helm lint chart/

load-kind:
	@echo "Loading image into Kind cluster..."
	kind load docker-image $(IMAGE_NAME):$(IMAGE_TAG) --name $(KIND_CLUSTER)

install:
	@echo "Installing Helm chart..."
	helm install $(RELEASE_NAME) chart/ --namespace $(NAMESPACE) --create-namespace --wait

upgrade:
	@echo "Upgrading Helm release..."
	helm upgrade $(RELEASE_NAME) chart/ --namespace $(NAMESPACE) --wait

uninstall:
	@echo "Uninstalling Helm release..."
	helm uninstall $(RELEASE_NAME) --namespace $(NAMESPACE)

all: build push
	@echo "Backend built and pushed successfully!"

clean: uninstall
	@echo "Cleaning up Docker images..."
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	docker rmi $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG) || true
	@echo "Cleanup complete!"

.PHONY: help build push unit-test lint package-chart push-chart update-chart-version

# Variables
IMAGE_NAME = devops-backend
IMAGE_TAG = latest
REGISTRY = ghcr.io/bwoogmy
CHART_PATH = chart
CHART_NAME = backend

help:
	@echo "Available commands:"
	@echo "  make build              - Build Docker image"
	@echo "  make push               - Push image to registry"
	@echo "  make unit-test          - Run unit tests"
	@echo "  make lint               - Lint Helm chart"
	@echo "  make package-chart      - Package Helm chart"
	@echo "  make push-chart         - Push chart to GHCR as OCI"
	@echo "  make update-chart-version - Update Chart.yaml version"

build:
	@echo "🔨 Building Docker image..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

push:
	@echo "📦 Pushing Docker image to registry..."
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

unit-test:
	@echo "🧪 Running unit tests..."
	pip3 install --quiet --break-system-packages -r requirements.txt && pytest tests/ -v

lint:
	@echo "🔍 Linting Helm chart..."
	helm lint $(CHART_PATH)/

package-chart:
	@echo "📦 Packaging Helm chart..."
	helm package $(CHART_PATH)/ --version $(IMAGE_TAG)

push-chart:
	@echo "🚀 Pushing Helm chart to GHCR..."
	helm push $(CHART_NAME)-$(IMAGE_TAG).tgz oci://$(REGISTRY)

update-chart-version:
	@echo "📝 Updating Chart.yaml with version $(IMAGE_TAG)..."
	@sed -i "s/^version:.*/version: $(IMAGE_TAG)/" $(CHART_PATH)/Chart.yaml
	@sed -i "s/^appVersion:.*/appVersion: $(IMAGE_TAG)/" $(CHART_PATH)/Chart.yaml
	@git add $(CHART_PATH)/Chart.yaml
	@git config user.email "jenkins@devops.local"
	@git config user.name "Jenkins CI"
	@git commit -m "chore: bump chart version to $(IMAGE_TAG)" || true
	@git push origin main || true

all: build push package-chart push-chart update-chart-version
	@echo "✅ Backend built and pushed successfully!"
# Define variables
DOCKER_COMPOSE = docker-compose
PYTHON = python3

# Help command
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make build          - Build the Docker images"
	@echo "  make up             - Start the services"
	@echo "  make down           - Stop and remove containers"
	@echo "  make logs           - View container logs"
	@echo "  make test           - Run all tests"
	@echo "  make clean          - Remove temporary files and Docker resources"

# Build Docker images
.PHONY: build
build:
	$(DOCKER_COMPOSE) build

# Start services
.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

# Stop services
.PHONY: down
down:
	$(DOCKER_COMPOSE) down

# View logs
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Run tests
.PHONY: test
test:
	$(PYTHON) -m unittest discover -s tests

# Clean up temporary files and Docker resources
.PHONY: clean
clean:
	rm -rf __pycache__ .pytest_cache
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

.PHONY: image
image:
	@docker build -f Dockerfile --platform linux/amd64 -t repro/tyk-api-gateway ./

run:
	@docker-compose up -d
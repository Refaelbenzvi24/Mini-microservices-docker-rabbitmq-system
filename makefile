build-controller:
	docker build -f controller_module/Dockerfile . -t controller_module

build-password:
	docker build -f analyze_module/Dockerfile . -t analyze_module

build-analyze:
	docker build -f password_module/Dockerfile . -t password_module

build-all:
	make build-controller
	make build-password
	make build-analyze

docker-up:
	make build-all
	docker-compose up
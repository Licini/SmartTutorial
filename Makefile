.PHONY: data
data:
	cd data && git clone https://github.com/specklesystems/speckle-blender
.PHONY: store
store:
	pipenv run store
query:
	pipenv run query
.PHONY: run-backend
run-backend:
	pipenv run run
.PHONY: start-backend
start-backend:
	pipenv run start-backend
.PHONY: log-backend
log-backend:
	./run.sh log-backend
.PHONY: build-front
	cd frontend && npm install
.PHONY: run-frontend
run-frontend:
	cd frontend && npm run serve



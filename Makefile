.PHONY: data
data:
	cd data && git clone https://github.com/specklesystems/speckle-blender
.PHONY: store
store:
	pipenv run store
query:
	pipenv run query
.PHONY: run
run:
	pipenv run run
.PHONY: build-front
	cd frontend && npm install



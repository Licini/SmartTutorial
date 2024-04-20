data:
	cd data && git clone https://github.com/specklesystems/speckle-blender
store:
	pipenv run store
query:
	pipenv run query
.PHONY: run
run:
	pipenv run run



#!/bin/bash

tok=$(cat .token-openai)
export OPENAI_API_KEY=$tok

echo $tok

mkdir -p data
mkdir -p store

case $1 in
	query) python backend/query.py ;;
	store) python backend/store.py ;;
	run) cd backend && uvicorn server:app --port 3000 --reload ;;
	*) echo "?"
esac

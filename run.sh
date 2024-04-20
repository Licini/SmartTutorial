#!/bin/bash

tok=$(cat .token-openai)
export OPENAI_API_KEY=$tok

echo $tok

mkdir -p data
mkdir -p store

start_frontend()
{
	cd frontend
       	nohup npm run serve > ../frontend.log &
	echo $! > ../frontend.nohup
	echo "started (" $! ")"
}

stop_frontend()
{
	job_id=$(cat frontend.nohup)
	kill -9 $job_id
	echo "stopped ($job_id)"
}

start_backend()
{
	cd backend
       	nohup uvicorn server:app --port 3001 --reload > ../backend.log &
	echo $! > ../backend.nohup
	echo "started (" $! ")"
}

stop_backend()
{
	job_id=$(cat backend.nohup)
	kill -9 $job_id
	echo "stopped ($job_id)"
}

case $1 in
	query) python backend/query.py ;;
	store) python backend/store.py ;;
	run) cd backend && uvicorn server:app --port 3001 --reload ;;
	start-backend) start_backend ;;
	stop-backend) stop_backend ;;
	log-backend) cat backend.log ;;
	start-frontend) start_frontend ;;
	stop-frontend) stop_frontend ;;
	*) echo "?"
esac

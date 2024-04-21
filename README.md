# Smart Tutorial

SmartTutorial : a web app to make interactive, ‘intelligent’ tutorials based on your codebase and domain-specific knowledge.

Write a minimal tutorial with general key points, add links to your codebase repo, and let SmartTutorial generate for you a complete and detailed tutorial based on your programming domain.


Try it online at [smart.bimriver.com](smart.bimriver.com)


### Backend : Python

- Install the required packages from `Pipfile`

`make install-backend` or `pipenv install`

- Add your OpenAI key in an `.openai-key` file in the root folder

- Run the server

`make run-backend` or `pipenv run backend`

- Serve as daemon

`make start-backend`

`make stop-backend`

### Frontend : Vue

- Install and run the vue app

`make build-frontend` or `cd frontend && npm install`


#### References
- [Annoy (Approximate Nearest Neighbors Oh Yeah)](https://github.com/spotify/annoy)
- [LlamaIndex Github Repo Reader](https://docs.llamaindex.ai/en/stable/examples/data_connectors/GithubRepositoryReaderDemo/)
- [LlamaIndex Vector Store Index](https://docs.llamaindex.ai/en/stable/understanding/storing/storing/)
- [private-gpt](https://github.com/zylon-ai/private-gpt?tab=readme-ov-file)
- [script-gpt](https://wandb.ai/srddev/ScriptGPT/reports/Script-GPT--VmlldzozNjQ4MDA1)
- [gpt-researcher](https://github.com/assafelovic/gpt-researcher)

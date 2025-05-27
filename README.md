# LLM Deployment

> Deploying a Qwen 2.5 Coder 7B model using llama and AWS to demonstrate how models are deployed in production environments.

[Link](https://duke.box.com/s/pqyyrkcjwr0a34nu1of2m3m90wj3wkq5) to the demo of the application being deployed on AWS g5 12xlarge instance.

### How to run

- Frontend
```
cd frontend
npm install
npm run dev
```
- The application is then hosted on `localhost:5173`


- Backend
```
python -m venv .venv
source .venv/bin/activate
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload
```

- Database
```bash
sudo docker compose -f docker-compose-db.yml up
```
To connect to the dockerized db container, 

```bash
docker exec -it my-fastapi-db psql -U postgres -d app_db
```


### Building the model, and running inference

1. Install uv, and clone the [llama](https://github.com/ggml-org/llama.cpp) directory. 
```bash
pip install uv
git clone https://github.com/ggml-org/llama.cpp
```

2. After cloning, cd into the llama directory, an add the following snippet at the top of `pyproject.toml`:

```bash
[project]
name="llama-cpp-scripts"
version = "0.0.0"
description = "Scripts that ship with llama.cpp"
dependencies = [
        "numpy>=1.25.0",
        "sentencepiece>=0.1.98,<=0.2.0",
        "transformers>=4.35.2",
        "protobuf>=4.21.0",
        "torch>=2.2.0"
]
requires-python = ">=3.9"
```

3. Run the following command:
```bash
uv run python convert_hf_to_gguf.py /home/ec2-user/.cache/huggingface/hub/models--Qwen--Qwen2.5-Coder-7B/snapshots/0396a76181e127dfc13e5c5ec48a8cee09938b02/ --outfile /home/ec2-user/models/qwen2.5-coder-7b.gguf --outtype f16 --use-temp-file --verbose
```
Replace the `/home/ec2-user/...` with the path to your model snapshot, and replace `/home/ec2-user/models` with the output path of your choice.

4. On an AWS server, like g5 12xlarge with Pytorch enabled and GPUs enabled, run the following command to build the llama source files:
```bash
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

5. Run the `llama-cli` and pass the gguf model to it:
```bash
./llama-cli -m /home/ec2-user/models/qwen2.5-coder-7b.gguf -ngl 35 -c 8192 --temp 0.7 --threads 8 --no-warmup -p "You are a helpful coding assistant."
```


### Deployment

#### VCM

If you're deploying on vcm, change the vcm base url in `frontend/.env.production`. You can change the link to the url / ip address of the server you are hosting it on, if using GCP or Azure for deployment.

Commands to deploy:

```bash
cd TemplateProject # You can rename this, just make sure the current directory has the docker compose file
sudo docker compose -f docker-compose.yml up --build -d
```
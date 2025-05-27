FROM nvidia/cuda:12.2.0-devel-ubuntu20.04

# Set the working directory in the container
WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive

COPY ./requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential python3 python3-pip python-is-python3 cmake git \
    && rm -rf /var/lib/apt/lists/*

ENV CMAKE_ARGS="-DGGML_CUDA=ON"
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.2/compat:${LD_LIBRARY_PATH}

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

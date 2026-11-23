# Base image for training on rented GPUs with Plasmid: the system, torch with its CUDA wheels and the Python packages
# a trainer on Plasmid's libraries needs. No model; a model is an overlay image built FROM this one. The host brings
# the NVIDIA driver and torch's wheels bring the CUDA runtime, so no CUDA base image and no toolkit.
#   /opt/py   torch 2.15.0+cu132, transformers, accelerate, safetensors, numpy and their dependencies
#             (requirements.txt, hash-locked, compiled from requirements.in); /opt/py/LOCK is that file's sha256
# /opt/py is on sys.path through a .pth file, so `python3 -I` sees it.
ARG BASE=ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852

FROM ${BASE} AS build
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /src/
RUN python3 -m pip install --quiet --no-cache-dir --break-system-packages --require-hashes --no-deps \
      --index-url https://download.pytorch.org/whl/cu132 --extra-index-url https://pypi.org/simple \
      --target /opt/py -r /src/requirements.txt \
 && sha256sum < /src/requirements.txt | cut -d' ' -f1 > /opt/py/LOCK

FROM ${BASE}
RUN apt-get update && apt-get install -y --no-install-recommends python3 openssl ca-certificates openssh-server procps \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/* /usr/share/doc/* /usr/share/man/*
COPY --from=build /opt/py /opt/py
RUN site=$(python3 -c 'import site; print(site.getsitepackages()[0])') && mkdir -p "$site" \
 && echo /opt/py > "$site/plasmid.pth" \
 && python3 -I -c "import torch, transformers, accelerate, safetensors, numpy; print(torch.__version__, torch.version.cuda, transformers.__version__, accelerate.__version__)"

# gpu-train-images

Container images for training models on rented GPUs, built by GitHub Actions and published to
`ghcr.io/plasmid-cloud/gpu-train-images/<name>:<tag>`; users pin an image by digest.

`images.toml` lists the images of two kinds. A base is `base/Dockerfile` with the hash-locked packages of
`base/<cuda>/`, and holds no model. An overlay is `overlay/Dockerfile`: a base by digest plus the model of
`models/<model>/`. Adding a CUDA version or a model is a folder and an entry in `images.toml`; the workflow `images`
builds what changed, the bases first. `pipeline-smoke` is a folder with a workflow of its own.

Everything in an image is public and hash-checked: Ubuntu, PyPI and PyTorch wheels (hash-locked), Hugging Face
models at a pinned revision. No data, no keys.

| Image | For |
|---|---|
| `torch-cu132` | `base/cu132`. The base for training with Plasmid: torch 2.15.0+cu132, transformers, accelerate, safetensors, numpy, hash-locked. No model. The host brings the NVIDIA driver (CUDA 13.2 or newer) |
| `torch-cu128` | `base/cu128`. The same base for hosts whose driver stops at CUDA 12.8: torch 2.11.0+cu128, the newest the cu128 index offers, and the same other packages. No model |
| `torch-cu132-modernbert-base` | `models/modernbert-base` on `torch-cu132`. A model overlay: `torch-cu132` by digest plus ModernBERT-base at a pinned revision |
| `torch-cu132-smollm2-135m-instruct` | `models/smollm2-135m-instruct` on `torch-cu132`. A model overlay: SmolLM2-135M-Instruct at a pinned revision |
| `pipeline-smoke` | No training: Ubuntu, python3, openssl, openssh. For checking the run pipeline around the job (copies, encryption, stop/start) without pulling torch |

# gpu-train-images

Container images for training models on rented GPUs. Each folder is one image, built by GitHub Actions and published
to `ghcr.io/plasmid-cloud/gpu-train-images/<folder>:<tag>`; users pin it by digest.

Everything in an image is public and hash-checked: Ubuntu, PyPI and PyTorch wheels (hash-locked), Hugging Face
models at a pinned revision. No data, no keys.

| Image | For |
|---|---|
| `torch-cu132` | The base for training with Plasmid: torch 2.15.0+cu132, transformers, accelerate, safetensors, numpy, hash-locked. No model. The host brings the NVIDIA driver (CUDA 13.2 or newer) |
| `torch-cu132-modernbert-base` | A model overlay: `torch-cu132` by digest plus ModernBERT-base at a pinned revision |
| `modernbert-cu128` | ModernBERT-base fine-tunes: torch 2.8.0+cu128, the training deps, ModernBERT-base. The host brings the NVIDIA driver (CUDA 12.8 or newer) |
| `pipeline-smoke` | No training: Ubuntu, python3, openssl, openssh. For checking the run pipeline around the job (copies, encryption, stop/start) without pulling torch |

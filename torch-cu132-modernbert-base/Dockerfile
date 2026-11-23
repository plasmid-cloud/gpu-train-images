# Model overlay on the base image torch-cu132: adds ModernBERT-base and nothing else, so it shares every layer of
# the base with each other image built FROM it.
#   /vol/models/answerdotai--ModernBERT-base@8949b909ec90   the model at a pinned revision, checked against model.sha256
# BASE is the base image by digest.
ARG BASE=ghcr.io/plasmid-cloud/gpu-train-images/torch-cu132@sha256:76890546b2af451017d1a3d8dd9c1a2b8876c372648abafe51f63386056a55c9

FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852 AS fetch
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && rm -rf /var/lib/apt/lists/*
COPY model.sha256 /src/
ARG MODEL_REPO=answerdotai/ModernBERT-base
ARG MODEL_REV=8949b909ec900327062f0ebf497f51aef5e6f0c8
RUN d=/vol/models/$(echo "$MODEL_REPO" | sed 's|/|--|')@$(echo "$MODEL_REV" | cut -c1-12) && mkdir -p "$d" && cd "$d" \
 && for f in $(cut -d' ' -f3 /src/model.sha256); do \
      curl -fsSL --retry 3 -o "$f" "https://huggingface.co/$MODEL_REPO/resolve/$MODEL_REV/$f"; done \
 && sha256sum -c --quiet /src/model.sha256

FROM ${BASE}
COPY --from=fetch /vol/models /vol/models

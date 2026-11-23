# Model overlay on a base image: adds one model and nothing else, so it shares every layer of its base with each
# other image built FROM that base.
#   /vol/models/<owner>--<name>@<12 hex of the revision>   the model at a pinned revision, checked against model.sha256
# One file for every overlay: BASE is the base image by digest, MODEL_REPO and MODEL_REV come from the model's
# model.env. The build context is the model's folder:
#   docker build -f overlay/Dockerfile --build-arg BASE=... --build-arg MODEL_REPO=... --build-arg MODEL_REV=... models/<model>
ARG BASE

FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852 AS fetch
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && rm -rf /var/lib/apt/lists/*
COPY model.sha256 /src/
ARG MODEL_REPO
ARG MODEL_REV
RUN d=/vol/models/$(echo "$MODEL_REPO" | sed 's|/|--|')@$(echo "$MODEL_REV" | cut -c1-12) && mkdir -p "$d" && cd "$d" \
 && for f in $(cut -d' ' -f3 /src/model.sha256); do \
      curl -fsSL --retry 3 -o "$f" "https://huggingface.co/$MODEL_REPO/resolve/$MODEL_REV/$f"; done \
 && sha256sum -c --quiet /src/model.sha256

FROM ${BASE}
COPY --from=fetch /vol/models /vol/models

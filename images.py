"""Prints, for the workflow, the images images.toml lists: `bases=<JSON list>` and `overlays=<JSON list>`, one
object per image with its name and what its build needs. A base's tag is the hash of its inputs, so an image is
built again only when its Dockerfile or its lock changes; an overlay's tag also takes its base's digest, which the
workflow adds."""

import hashlib
import json
import tomllib
from pathlib import Path


def digest(*paths: str) -> str:
    return hashlib.sha256(b"".join(Path(p).read_bytes() for p in paths)).hexdigest()[:12]


def main() -> None:
    images = tomllib.loads(Path("images.toml").read_text())
    bases = {
        b["cuda"]: {
            "name": f"torch-{b['cuda']}",
            "cuda": b["cuda"],
            "tag": "lock-" + digest("base/Dockerfile", f"base/{b['cuda']}/requirements.txt"),
        }
        for b in images["base"]
    }
    overlays = []
    for o in images.get("overlay", []):
        folder = f"models/{o['model']}"
        env = dict(line.split("=", 1) for line in Path(folder, "model.env").read_text().split())
        base = bases[o["base"]]
        overlays.append(
            {
                "name": f"{base['name']}-{o['model']}",
                "base": f"{base['name']}:{base['tag']}",
                "model": o["model"],
                "repo": env["MODEL_REPO"],
                "rev": env["MODEL_REV"],
                "inputs": digest("overlay/Dockerfile", f"{folder}/model.env", f"{folder}/model.sha256"),
            }
        )
    print("bases=" + json.dumps(list(bases.values())))
    print("overlays=" + json.dumps(overlays))


if __name__ == "__main__":
    main()

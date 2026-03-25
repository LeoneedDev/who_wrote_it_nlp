import argparse
import os
from huggingface_hub import snapshot_download

MODELS_DIR = os.path.join(os.getcwd(), "../notebooks/models")


def main() -> None:
    downloaded_path = snapshot_download(
        repo_id="qg2020252627/twitter_author_profiling_by_gender_nlp",
        repo_type="model",
        local_dir=MODELS_DIR,
        token=os.getenv("HUGGINGFACE_HUB_TOKEN"),
    )

    print(f"Downloaded to: {downloaded_path}")


if __name__ == "__main__":
    main()

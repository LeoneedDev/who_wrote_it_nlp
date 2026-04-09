import argparse
import os
from pathlib import Path

from huggingface_hub import hf_hub_download

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "notebooks" / "models"
REPO_ID = "qg2020252627/twitter_author_profiling_by_gender_nlp"


def arg_parse_model_type(model_type: str) -> str:
    switch = {
        "LinearSVC": "model_LinearSVC.joblib",
        "LogisticRegression": "model_LogisticRegression.joblib",
        "RandomForest": "model_RandomForest.joblib",
    }

    if model_type in switch:
        return switch[model_type]
    else:
        raise ValueError(
            f"Unsupported model type: {model_type}. Supported types are: {', '.join(switch.keys())}.")


def normalize_model_filename(model_type: str) -> str:
    selected = (model_type or "").strip()
    if not selected:
        return "model_LinearSVC.joblib"

    if selected.endswith(".joblib"):
        return selected
    if selected.startswith("model_"):
        return f"{selected}.joblib"
    return f"model_{selected}.joblib"


def set_as_main_model(source_model: Path, target_model: Path) -> None:
    if target_model.exists():
        target_model.unlink()
    source_model.rename(target_model)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download model snapshot and create model.joblib alias."
    )
    parser.add_argument(
        "--model-type",
        default=None,
        help="Preferred model type or filename (e.g. LinearSVC, model_LinearSVC.joblib).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    requested_filename = normalize_model_filename(args.model_type)
    target_model = MODELS_DIR / "model.joblib"

    if os.path.exists(requested_filename):
        print(f"Model file already exists locally: {requested_filename}")
        set_as_main_model(Path(requested_filename), target_model)
        print(f"Renamed existing file to: {target_model}")
        return

    downloaded_path = hf_hub_download(
        repo_id=REPO_ID,
        repo_type="model",
        filename=requested_filename,
        local_dir=str(MODELS_DIR),
        token=os.getenv("HUGGINGFACE_HUB_TOKEN"),
    )

    downloaded_file = Path(downloaded_path)
    if not downloaded_file.exists():
        raise FileNotFoundError(
            f"Expected downloaded model file was not found: {downloaded_file}"
        )

    set_as_main_model(downloaded_file, target_model)
    print(f"Downloaded one file and renamed to: {target_model}")


if __name__ == "__main__":
    main()

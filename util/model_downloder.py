import argparse
import os
from pathlib import Path

from huggingface_hub import hf_hub_download

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "notebooks" / "models"
REPO_ID = "qg2020252627/twitter_author_profiling_by_gender_nlp"


def arg_parse_model_type(model_type: str) -> str:
    normalized = model_type.strip().lower()
    switch = {
        "svc": "model_LinearSVC.joblib",
        "linearsvc": "model_LinearSVC.joblib",
        "model_linearsvc.joblib": "model_LinearSVC.joblib",
        "lr": "model_LogisticRegression.joblib",
        "logisticregression": "model_LogisticRegression.joblib",
        "model_logisticregression.joblib": "model_LogisticRegression.joblib",
        "rf": "model_RandomForestClassifier.joblib",
        "randomforest": "model_RandomForestClassifier.joblib",
        "model_randomforest.joblib": "model_RandomForestClassifier.joblib",
    }

    if normalized in switch:
        return switch[normalized]

    raise ValueError(
        f"Unsupported model type: {model_type}. "
        "Supported values: svc, lr, rf, LinearSVC, LogisticRegression, RandomForest "
        "or explicit model_*.joblib filenames."
    )


def set_as_main_model(source_model: Path, target_model: Path) -> None:
    if source_model.resolve() == target_model.resolve():
        return

    if target_model.exists():
        target_model.unlink()
    source_model.rename(target_model)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download model snapshot and create model.joblib alias."
    )
    parser.add_argument(
        "--model-type",
        default="svc",
        help=(
            "Preferred model type or filename. "
            "Supported: svc, lr, rf, LinearSVC, LogisticRegression, RandomForest, "
            "or model_*.joblib. Default: svc."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    requested_filename = arg_parse_model_type(args.model_type)
    target_model = MODELS_DIR / "model.joblib"
    local_requested_file = MODELS_DIR / requested_filename

    if local_requested_file.exists():
        print(f"Model file already exists locally: {local_requested_file}")
        set_as_main_model(local_requested_file, target_model)
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

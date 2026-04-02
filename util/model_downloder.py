import argparse
import os
import shutil
from pathlib import Path

from huggingface_hub import snapshot_download

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "notebooks" / "models"


def resolve_target_candidate(model_type: str | None = None) -> Path | None:
    preferred = [
        MODELS_DIR / "model_LinearSVC.joblib",
        MODELS_DIR / "model_LogisticRegression.joblib",
        MODELS_DIR / "model_RandomForestClassifier.joblib",
    ]

    selected_model_type = (model_type or "").strip()
    if selected_model_type:
        specified_candidates = [
            MODELS_DIR / selected_model_type,
            MODELS_DIR / f"{selected_model_type}.joblib",
            MODELS_DIR / f"model_{selected_model_type}.joblib",
        ]
        for candidate in specified_candidates:
            if candidate.exists():
                return candidate
        print(
            f"Requested model type '{selected_model_type}' not found. Falling back to preferred list."
        )

    candidates = [path for path in preferred if path.exists()]
    if not candidates:
        candidates = sorted(MODELS_DIR.glob("model*.joblib"))
    return candidates[0] if candidates else None


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
    downloaded_path = snapshot_download(
        repo_id="qg2020252627/twitter_author_profiling_by_gender_nlp",
        repo_type="model",
        local_dir=str(MODELS_DIR),
        token=os.getenv("HUGGINGFACE_HUB_TOKEN"),
    )

    target_model = MODELS_DIR / "model.joblib"
    if not target_model.exists():
        candidate = resolve_target_candidate(args.model_type)
        if candidate:
            shutil.copy2(candidate, target_model)
            print(
                f"Created alias model file: {target_model} -> {candidate.name}")

    print(f"Downloaded to: {downloaded_path}")


if __name__ == "__main__":
    main()

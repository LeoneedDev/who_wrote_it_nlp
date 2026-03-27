import os
import shutil
from pathlib import Path

from huggingface_hub import snapshot_download

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "notebooks" / "models"


def main() -> None:
    downloaded_path = snapshot_download(
        repo_id="qg2020252627/twitter_author_profiling_by_gender_nlp",
        repo_type="model",
        local_dir=str(MODELS_DIR),
        token=os.getenv("HUGGINGFACE_HUB_TOKEN"),
    )

    target_model = MODELS_DIR / "model.joblib"
    if not target_model.exists():
        preferred = [
            MODELS_DIR / "model_LinearSVC.joblib",
            MODELS_DIR / "model_LogisticRegression.joblib",
            MODELS_DIR / "model_RandomForestClassifier.joblib",
        ]
        candidates = [path for path in preferred if path.exists()]
        if not candidates:
            candidates = sorted(MODELS_DIR.glob("model*.joblib"))
        if candidates:
            shutil.copy2(candidates[0], target_model)
            print(
                f"Created alias model file: {target_model} -> {candidates[0].name}")

    print(f"Downloaded to: {downloaded_path}")


if __name__ == "__main__":
    main()

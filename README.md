# Who Wrote It?

Bachelor thesis project focused on author profiling from tweet text. The main task is binary gender classification from text written by an unknown author.

## Quick Start (recommended)

Use `just` commands to bootstrap and run the project:

```bash
just init
just run
```

What these commands do:
- `just init`: creates `.env` from `.env.example`, checks Python 3.13, creates `venv`, and installs dependencies from `requirements.txt`.
- `just run`: ensures a model exists (downloads from Hugging Face if needed), then starts the Docker stack with `docker compose up -d --build`.

Verify and test:

```bash
just health
just predict text="I really enjoyed this match today"
```

Show all available commands:

```bash
just list
```

## Requirements

Project uses Python 3.13.

Notebook dependencies:
- `numpy~=2.4`
- `pandas~=3.0`
- `scipy~=1.17`
- `statsmodels~=0.14`
- `matplotlib~=3.10`
- `scikit-learn~=1.8`
- `seaborn~=0.13`
- `jupyterlab~=4.5`
- `wandb~=0.25`
- `xdk~=0.9`
- `playwright~=1.58`
- `fsspec~=2026.2`
- `huggingface_hub~=1.5`
- `nltk~=3.9`
- `nbstripout~=0.9`
- `zenodo-get~=3.0`
- `lxml~=6.0`

Server dependencies:
- `flask~=3.1`

Model save/load:
- `joblib~=1.5`

## Project Structure

### Python files and their purpose

- `app.py`
    - Flask inference API.
    - Loads model from `MODEL_PATH` (default: `model.joblib` in repository root).
    - Exposes `POST /predict` and `GET /health`.

- `util/preprocessing.py`
    - Contains `TweetPreprocessor` (scikit-learn transformer).
    - Normalizes tweets: line feeds, repeated chars, URLs, mentions, whitespace.
    - Tokenizes with NLTK `TweetTokenizer`.

- `util/model_downloder.py`
    - Downloads model artifacts from Hugging Face Hub into `notebooks/models`.
    - Creates alias file `notebooks/models/model.joblib` if only specific model filenames exist.

- `util/logger.py`
    - Utility helpers for Weights & Biases logging.
    - Logs search results (`RandomizedSearchCV` / `GridSearchCV`) and saves model artifacts.

- `util/__init__.py`
    - Package marker for `util` modules.

### Notebooks and workflow

Notebooks are in `notebooks/` and are ordered as a workflow:

1. `01_Dataset.ipynb`
     - Data acquisition and dataset preparation.
     - Produces train/validation/test CSV files used by later notebooks.

2. `02_EDA.ipynb`
     - Exploratory data analysis.
     - Feature distributions, n-gram analysis, and statistical tests.

3. `03_Hyperparams.ipynb`
     - Hyperparameter tuning for the text-classification pipeline.
     - Supports W&B logging and saving best configuration/model.

4. `04_Training.ipynb`
     - Final training with selected hyperparameters.
     - Test evaluation and model export.

5. `05_Hypotesis.ipynb`
     - Hypothesis-testing experiments (for example, impact of tweets-per-author).

### Detailed notebook description (same order)

1. `01_Dataset.ipynb`
     - Used for dataset creation for author profiling.
     - Includes data collection and cleaning so the resulting dataset is ready for the next notebooks.
     - Uses data originally downloaded from [TBCOV](https://crisisnlp.qcri.org/tbcov), then cleans it and enriches tweet text via Twitter/X APIs.
     - Works with two setups: one tweet per author and one hundred tweets per author ([PAN CLEF Dataset](https://zenodo.org/records/3692340)).
     - This enables testing the hypothesis that more tweets per author can improve model performance.

2. `02_EDA.ipynb`
     - Exploratory data analysis notebook.
     - Performs text feature engineering (including lexical diversity, emoji/mention/hashtag counts, punctuation ratios).
     - Produces visual analysis (boxplots, histplots, scatter plots, QQ-plots, pairplots).
     - Includes n-gram analysis (character, word, and skip n-grams).
     - Runs statistical tests (Mann-Whitney U for numerical features, Chi-square with Cramer's V for categorical/word features) to identify gender-discriminative patterns.

3. `03_Hyperparams.ipynb`
     - Needs:
         - dataset with 1 tweet per author
     - Performs hyperparameter tuning for the pipeline:
         - `TweetPreprocessor -> FeatureUnion [TfidfVectorizer(word) + TfidfVectorizer(char)] -> TruncatedSVD -> LinearSVC`
     - Search is done in two phases:
         - Randomized Search (500 iterations, 4-fold stratified CV, F1-macro scoring) for broad exploration.
         - Grid Search for refinement around the best region.
     - Tuning is staged: TF-IDF parameters, then SVD parameters, then `LinearSVC` parameters.
     - `WANDB_TOKEN` can be used to log metrics and best parameters to W&B.
     - Best model can be saved as a W&B artifact and exported locally.

4. `04_Training.ipynb`
     - Needs:
         - dataset with 1 tweet per author
         - best hyperparameters from tuning
     - Final model training notebook.
     - Merges training and validation sets (LinearSVC has no validation phase), applies tuned hyperparameters, and trains the same pipeline.
     - Evaluates on test set with classification report (precision, recall, F1) and confusion matrix.
     - Can log training results to W&B and save model artifacts.
     - Final model can be exported locally.

5. `05_Hypotesis.ipynb`
     - Needs:
         - dataset with 1 tweet per author
         - trained model on dataset with 1 tweet per author
     - Reserved for hypothesis testing.
     - Intended to verify whether using more tweets per author leads to better performance and to test related author-profiling hypotheses.

### Data and models

- `notebooks/datasets/`: prepared CSV datasets and PAN19 source files.
- `notebooks/models/`: trained models (`.joblib`) and model README.

## API

### `POST /predict`

Request:

```bash
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"text":"Your text here"}' \
    http://localhost:5000/predict
```

Success response example:

```json
{
    "response": "M"
}
```

### `GET /health`

```bash
curl http://localhost:5000/health
```

Response:

```json
{
    "status": "ok"
}
```

## Environment Variables

| Variable | Used in | Required | Default | Description |
|---|---|---|---|---|
| `MODEL_PATH` | `app.py` | No | `model.joblib` | Model file path resolved relative to repository root |
| `WANDB_TOKEN` | notebooks | Optional | - | Token for logging runs/artifacts to Weights & Biases |
| `TWITTER_BEARER_TOKEN` | `01_Dataset.ipynb` | Optional | - | Token for collecting tweet text from X/Twitter APIs |
| `HUGGINGFACE_HUB_TOKEN` | `util/model_downloder.py` | Optional | - | Token for downloading private model repos |

## Docker Image

Published image:
- `ghcr.io/LeoneedDev/who_wrote_it:latest`

Run directly:

```bash
docker run -p 5000:5000 ghcr.io/LeoneedDev/who_wrote_it:latest
```
import wandb
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.base import BaseEstimator
import pandas as pd
import joblib


def wandb_log_search_results(random_search: RandomizedSearchCV | GridSearchCV, run_name: str, job_type: str, project_name: str = "who-wrote-it-nlp", entity_name: str = "who-wrote-it-nlp"):
    run = wandb.init(name=run_name, job_type=job_type,
                     project=project_name, entity=entity_name)
    df = pd.DataFrame(random_search.cv_results_)
    cols = ["mean_test_score", "mean_train_score"] + \
        [col for col in df.columns if col.startswith("param_")]
    df = df[cols]

    table = wandb.Table(dataframe=df)
    run.log({"search_results": table})
    run.finish()


def wandb_save_model(model: BaseEstimator, model_path: str, project_name: str = "who-wrote-it-nlp", entity_name: str = "who-wrote-it-nlp"):
    save_model_path = joblib.dump(model, model_path)
    if isinstance(save_model_path, list):
        save_model_path = save_model_path[0]
        if save_model_path is None:
            raise ValueError("Model path is None")
    elif save_model_path is None:
        raise ValueError("Model path is None")

    run = wandb.init(project=project_name, entity=entity_name)
    artifact = wandb.Artifact(model_path, type="model")
    artifact.add_file(model_path)
    run.log_artifact(artifact)
    run.finish()

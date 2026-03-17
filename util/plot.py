import pandas as pd
import seaborn as sns
from sklearn.model_selection import RandomizedSearchCV
import itertools
from matplotlib import pyplot as plt


def plot_all_heatmaps(random_search: RandomizedSearchCV, metric: str = "mean_test_score"):
    df = pd.DataFrame(random_search.cv_results_)

    if metric not in df.columns:
        raise ValueError(
            f"Metric '{metric}' not found in cv_results_. Available: {list(df.columns)}")

    param_cols = [col for col in df.columns if col.startswith("param_")]
    print(f"Found {len(param_cols)} hyperparameters: {param_cols}")

    if len(param_cols) < 2:
        print("Need at least 2 hyperparameters to build heatmaps.")
        return

    for param_x, param_y in itertools.combinations(param_cols, 2):
        pivot = df.pivot_table(values=metric, index=param_y,
                               columns=param_x, aggfunc="mean")

        plt.figure(figsize=(8, 6))
        sns.heatmap(pivot, annot=True, fmt=".3f", cmap="viridis")
        plt.title(f"Heatmap of {metric} for {param_x} vs {param_y}")
        plt.tight_layout()
        plt.show()

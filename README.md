# Bc thesis with name "Who wrote it?"

Code base for a Bc thiesis
The thesis is about author profiling, and the main goal is to determmine the author gender based on a text written by the unknown author.

# Code base
The code base in notebook is written in Python 3.14 and uses the following libraries:
- numpy~=2.4
- pandas~=3.0
- scipy~=1.17
- statsmodels~=0.14
- matplotlib~=3.10
- scikit-learn~=1.8
- seaborn~=0.13
- jupyterlab~=4.5
- wandb~=0.25

Server code is written in Python 3.14 and uses the following libraries:
- flask~=3.1

# Docker
The code base is dockerized using Dockerfile. The Docker image is based on python:3.14-slim-trixie and exposes port 5000 for the server. The requirements are installed using pip and the app.py file is copied to the container. The server is started using the command "flask run".

# Docker image
Workflow will automatically build a Docker image and push it to github container registry.
Latest image can be found here:
**ghcr.io/LeoneedDev/who_wrote_it:latest**

# Usage
## Use over interface
To run the application locally, you can use Docker:
```bash
docker run -p 5000:5000 ghcr.io/LeoneedDev/who_wrote_it:latest
```
This will start the server on port 5000. You can then access the application by navigating to http://localhost:5000 in your web browser.

##Use over API
You can also use the API directly by sending a POST request to http://localhost:5000/predict with a JSON payload containing the text you want to analyze. For example:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "Your text here"}' http://localhost:5000/predict
```

This will return OK(200) response and JSON with the predicted gender of the author.
Possible response: is "m" for male and "f" for female
```json
{
    "gender": "m"
}
```

# API additional endpoints
## Health check
You can check the health of the server by sending a GET request to http://localhost:5000/health. This will return a JSON response indicating the status of the server:
```json
{
    "status": "ok"
}
```

# Notebooks
## Using JupyterLab and Python venv on Unix systems
The code base also includes Jupyter notebooks for data analysis and model training. These notebooks are located in the "notebooks" directory and can be run using JupyterLab. To start JupyterLab, you can use the following command:
```bash
jupyter lab
```
This will open JupyterLab in your web browser, where you can navigate to the "notebooks" directory and open the notebooks to run them individually and only part that you interest in. 

** Remeber to install the required libraries before running the notebooks **
```bash
python -m venv venv && source venv/bin/activate
```
```bash
pip install -r requirements.txt
```

## Using JupyterLab and Python venv on Windows systems
Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

Then install dependencies and start JupyterLab:
```bash
pip install -r requirements.txt
jupyter lab
```

# Describtion for the notebooks
## **Dataset.ipynb**
This notebook is used for dataset creation. You can find there code that can be used to create your own dataset for author profiling. This notebook consist of code for data collection, data cleaning. So the resulting dataset is ready for use in the next notebooks.

## **EDA.ipynb**
This notebook is used for exploratory data analysis. You can find there code that can be used to analyze the dataset and visualize the results. This notebook consist of code for data visualization, data analysis, and data preprocessing. So the resulting dataset is ready for use in the next notebooks.

# **Hyperparams.ipynb**
This notebook is used for hyperparameter tuning. You can find there code that can be used to tune the hyperparameters of the model. This notebook consist of code for hyperparameter tuning, model evaluation, and model selection. So the resulting model is ready for use in the next notebooks. 

You can also provide a wandb token to log the results of hyperparameter tuning to Weights & Biases.
Best model from hyperparameter tuning is saved in wandb, so we dont need to retrain it again in the next notebook.
At then end of notebook you can save the best model from hyperparameter tuning locally. It will save time and not requare retraining the model in the next notebook.

# **Training.ipynb**
This notebook is used for model training. You can find there code that can be used to train the model. This notebook consist of code for model training, model evaluation, and model selection. So the resulting model is ready for use in the next notebooks. 

You can also provide a wandb token to log the results of model training to Weights & Biases and save the best one in wandb artifacts.
At the end of notebook you can save the best model from model training locally.
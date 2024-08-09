import os
from options import SPLIT_PATH, INITIAL_PATH
from service.model_creation import mobilenet_model, model_load, model_store, model_convert
from service.model_optimization import model_training
from service.training_configuration import get_split_generators
from prefect import flow, task

current_version = 0 # Latest version of the model
path_models_best = "models/best" # Path to the best models
path_models_tflite = "models/deploy" # Path to the converted models to upload
latest_split = "" # Latest split of the dataset collected and used for retraining

def last_model_path():
    return f"{path_models_best}/weld_{current_version}.keras"

def next_model_path(root="."):
    global current_version
    current_version += 1
    return f"{root}/{path_models_best}/weld_{current_version}.keras"

@task
def create_model():
    return mobilenet_model()

@task
def train_model(model, data, epochs=5):
    print("Starting model training...")
    return model_training(model, data[0], data[1], epochs)

@task
def save_model(model, path=""):
    model_store(model, next_model_path(path))

@task
def load_model(path):
    return model_load(path)

@task
def upload_model(path, valid=True):
    """
    Upload the model to Firebase.

    Args:
        path: The path to the model file.
        valid: Whether the model should be deployed to clients.
    """
    model_convert(path, f"{path_models_tflite}/weld_{current_version}.tflite")
    if valid:
        print("Uploading model to Firebase...") # TODO: Implement
    else:
        print("Ignoring model deployment due to poor performance.")

@task
def evaluate_performance(model, initial_test, test):
    """
    Evaluate the model's performance on the test data.

    Args:
        model: The trained model
        initial_test: Initial test data to use for evaluation.
        test: Additional test data to use in addition to the initial.

    Returns:
        True if the model's performance is acceptable, False otherwise.
    """
    # Code to evaluate the model's performance
    pass

@task
def find_data(initial=False, root="."):
    if initial:
        return *get_split_generators(INITIAL_PATH if root == "." else root), False
    directories = [f for f in os.listdir(f"{root}/{SPLIT_PATH}") if os.path.isdir(os.path.join(f"{root}/{SPLIT_PATH}", f))]
    if not directories:
        print("WARNING: No Dataset Splits found, attempting to load Initial dataset instead.")
        return *get_split_generators(INITIAL_PATH), True
    path = sorted(directories, reverse=True)[0]
    repeating = path == latest_split
    latest_split = path
    return *get_split_generators(path), repeating

@flow
def initial_training_flow():
    model = create_model()
    data = find_data(initial=True)
    train_model(model, data, epochs=1)
    save_model(model)
    upload_model(model)
    evaluation = evaluate_performance(model, data[2])
    print(evaluation)

@flow
def periodic_retraining_flow():
    data = find_data()
    if data is None or data[0] is None or data[3]:
        print("Skipping after no new drift split found.")
        return
    else:
        model = load_model()
        train_model(model, data)
        save_model(model)
        evaluation = evaluate_performance(model, find_data(True)[2], data[2])
        if evaluation:
            print("Model performance is sufficient.")
            upload_model(model)
        else:
            print("Model performance is insufficient.")
            upload_model(model, valid=False)

if __name__ == "__main__":
    print("Testing modeling integration.")
    model = create_model()
    os.makedirs("temp", exist_ok=True)
    data = find_data(True, "temp")
    print("Train model")
    model_training(model, data[0], data[1], 256)
    print("Model trained")
    os.makedirs("temp/models", exist_ok=True)
    os.makedirs("temp/models/best", exist_ok=True)
    os.makedirs("temp/models/deploy", exist_ok=True)
    save_model(model, "temp")
    results = evaluate_performance(model, data[2])
    print(results)
    upload_model(model, False)

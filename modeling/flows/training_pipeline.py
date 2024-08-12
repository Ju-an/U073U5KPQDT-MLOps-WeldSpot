import os

from prefect import flow, task

from options import AUC_THRESHOLD, INITIAL_PATH, SPLIT_PATH
from service.cloud_storage import upload_tflite
from service.model_creation import (
    mobilenet_model,
    model_convert,
    model_load,
    model_store,
)
from service.model_optimization import measure_performance, model_training
from service.training_configuration import get_split_generators

SKIP_EVAL = True  # Bypass evaluation of the model performance
current_version = 0  # Latest version of the model
path_models_best = "models/best"  # Path to the best models
path_models_tflite = "models/deploy"  # Path to the converted models to upload
latest_split = ""  # Latest split of the dataset collected and used for retraining


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
    final_path = next_model_path(path)
    print(f"Saving model to {final_path}")
    model_store(model, final_path)


@task
def load_model(path):
    return model_load(path)


@task
def deploy_model(path, valid=True, tags=["unknown"]):
    """
    Upload the model to Firebase.

    Args:
        path: The path to the model file.
        valid: Whether the model should be deployed to clients.
        tags: Tags to associate with the model (e.g., staging, weld, mobilenet, test).
    """
    convert_output = f"{path_models_tflite}/weld_{current_version}.tflite"
    model_convert(path, convert_output)
    if valid:
        print("Uploading model to Firebase...")
        upload_tflite(convert_output, tags)
    else:
        print(
            "Ignoring model deployment due to poor performance. You can still manually upload it."
        )


@task
def evaluate_performance(model, initial_test, test=None):
    """
    Evaluate the model's performance on the test data.

    This saves confusion matrices in the logs/predict folder as general_.png (the global performance compared with our prestablished initial test dataset)
    and test_.png (based on the new data provided).

    Args:
        model: The trained model
        initial_test: Initial test data to use for evaluation.
        test: Additional test data to use in addition to the initial.

    Returns:
        True if the model's performance is acceptable, False otherwise.
    """
    if SKIP_EVAL:
        return True
    auc = measure_performance(model, initial_test, "general")
    if test is not None:
        auc_t = measure_performance(model, test)
        if auc_t < auc:
            auc = auc_t
    return auc >= AUC_THRESHOLD


@task
def find_data(initial=False, root="."):
    global latest_split
    if initial:
        print("Looking for initial data")
        return *get_split_generators(INITIAL_PATH if root == "." else root), False
    directories = [
        f
        for f in os.listdir(f"{root}/{SPLIT_PATH}")
        if os.path.isdir(os.path.join(f"{root}/{SPLIT_PATH}", f))
    ]
    if not directories:
        print(
            "WARNING: No Dataset Splits found, attempting to load Initial dataset instead."
        )
        return *get_split_generators(INITIAL_PATH), True
    path = sorted(directories, reverse=True)[0]
    repeating = path == latest_split
    latest_split = path
    return *get_split_generators(f"{root}/{SPLIT_PATH}/{path}"), repeating


@flow
def initial_training_flow():
    model = create_model()
    data = find_data(initial=True)
    print(f"Found data generators: {data}")
    train_model(model, data, epochs=5)
    save_model(model)
    deploy_model(model, tags=["initial", "weld", "mobilenet"])
    evaluation = evaluate_performance(model, data[2])
    print(evaluation)


@flow
def periodic_retraining_flow():
    data = find_data()
    if data is None or data[0] is None or data[3]:
        print("Skipping after no new drift split found.")
        return
    else:
        current_path = last_model_path()
        print(f"Loading model from {current_path}")
        model = load_model(current_version)
        train_model(model, data)
        save_model(model)
        evaluation = evaluate_performance(model, find_data(True)[2], data[2])
        if evaluation:
            print("Model performance is sufficient.")
            deploy_model(model, tags=["weld", "mobilenet", f"v{current_version}"])
        else:
            print("Model performance is insufficient.")
            deploy_model(model, valid=False)


if __name__ == "__main__":
    print("Testing modeling integration.")
    model = create_model()
    os.makedirs("temp", exist_ok=True)
    data = find_data(True, "temp")
    print("Train model")
    model_training(model, data[0], data[1], 10)
    print("Model trained")
    os.makedirs("temp/models", exist_ok=True)
    os.makedirs("temp/models/best", exist_ok=True)
    os.makedirs("temp/models/deploy", exist_ok=True)
    save_model(model, "temp")
    deploy_model(model, False)

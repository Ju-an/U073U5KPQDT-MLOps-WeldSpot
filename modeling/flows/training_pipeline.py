from prefect import flow, task

current_version = 1 # Latest version of the model

@task
def create_model():
    # Code to create and initialize the model
    pass

@task
def train_model(model):
    # Code to train the model
    pass

@task
def save_model(model):
    # Code to save the trained model
    pass

@task
def load_model(path):
    # Code to load a model from a file
    pass

@task
def upload_model(path, valid=True):
    """
    Upload the model to Firebase.
    
    Args:
        path: The path to the model file.
        valid: Whether the model should be deployed to clients.
    """
    # Code to convert to tflite and upload the model to firebase
    pass

@task
def evaluate_performance(model, test):
    """
    Evaluate the model's performance on the test data.
    
    Args:
        model: The trained model
        test: Additional test data to use in addition to the initial.

    Returns:
        True if the model's performance is acceptable, False otherwise.
    """
    # Code to evaluate the model's performance
    pass

@task
def find_data():
    # Code to check for new splits
    pass

@flow
def initial_training_flow():
    model = create_model()
    train_model(model)
    save_model(model)
    upload_model(model)
    evaluate_performance(model)

@flow
def periodic_retraining_flow():
    data = find_data()
    if data is None:
        print("Skipping after no new drift split found.")
        return
    else:
        model = load_model()
        train_model(model, data)
        save_model(model)
        evaluation = evaluate_performance(model)
        if evaluation:
            print("Model performance is sufficient.")
            upload_model(model)
        else:
            print("Model performance is insufficient.")
            upload_model(model, valid=False)
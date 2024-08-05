from prefect import flow, task

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
def upload_model(path):
    # Code to convert to tflite and upload the model to firebase
    pass

@task
def evaluate_performance(model):
    # Code to evaluate the model's performance
    pass

@task
def find_data():
    # Code to check for new splits
    pass

@flow
def initial_training_flow():
    model = create_model()
    trained_model = train_model(model)
    saved_model = save_model(trained_model)
    uploaded_model = upload_model(saved_model)
    evaluation = evaluate_performance(uploaded_model)

@flow
def periodic_retraining_flow():
    model = create_model()
    data = find_data()
    trained_model = train_model(model, data)
    saved_model = save_model(trained_model)
    uploaded_model = upload_model(saved_model)
    evaluation = evaluate_performance(uploaded_model)
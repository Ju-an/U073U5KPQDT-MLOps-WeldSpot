from prefect import serve
from prefect.automations import Automation
from prefect.events.schemas.automations import EventTrigger

from flows.collection_pipeline import initial_dataset_flow, periodic_monitoring_flow
from flows.training_pipeline import initial_training_flow, periodic_retraining_flow

DATASET_SCHEDULE = "0 12 * * *" # Daily at 12:00 PM #TODO: .env

def register_flows():
    initial_dataset_flow()
    dataset_pipeline = periodic_monitoring_flow.to_deployment(name="Dataset Deployment Pipeline",
                        description="Daily flow for downloading data from Firebase and treat it for the model training flow.",
                        cron=DATASET_SCHEDULE, tags=["dataset", "data preparation", "data collection"])
    initial_training_flow()
    modeling_pipeline = periodic_retraining_flow.to_deployment(name="Modeling Deployment Pipeline",
                        description="Daily flow for training the model with the new dataset and evaluate its performance.",
                        cron=DATASET_SCHEDULE, tags=["modeling", "model training", "model evaluation"])

    serve(dataset_pipeline)

# Register the flows with Prefect
if __name__ == "__main__":
    register_flows()


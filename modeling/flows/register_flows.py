import logging, subprocess
from prefect import flow, serve
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from flows.collection_pipeline import initial_dataset_flow, periodic_monitoring_flow
from flows.training_pipeline import initial_training_flow, periodic_retraining_flow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATASET_SCHEDULE = "0 12 * * *"  # At 12:00 every day.
MODELING_SCHEDULE = "0 13 * * *"  # At 13:00 every day

@flow
def register_flows():
    logger.info("Registering initial dataset flow")
    initial_dataset_flow()

    logger.info("Creating dataset deployment pipeline")
    dataset_pipeline = Deployment.build_from_flow(
        flow=periodic_monitoring_flow,
        name="Dataset Deployment Pipeline",
        description="Daily flow for downloading data from Firebase and treat it for the model training flow.",
        schedule=CronSchedule(cron=DATASET_SCHEDULE),
        tags=["dataset", "data preparation", "data collection"],
    )

    logger.info("Creating modeling deployment pipeline")
    modeling_pipeline = Deployment.build_from_flow(
        flow=periodic_retraining_flow,
        name="Modeling Deployment Pipeline",
        description="Daily flow for training the model with the new dataset and evaluate its performance.",
        schedule=CronSchedule(cron=MODELING_SCHEDULE),
        tags=["modeling", "model training", "model evaluation"],
    )

    logger.info("Applying dataset deployment pipeline")
    dataset_pipeline.apply()
    # serve(dataset_pipeline)
    logger.info("Applying modeling deployment pipeline")
    modeling_pipeline.apply()
    # serve(modeling_pipeline)

    logger.info("Deployments registered successfully")

# Register the flows with Prefect
if __name__ == "__main__":
    register_flows()
    # prefect agent start --pool "default-agent-pool"

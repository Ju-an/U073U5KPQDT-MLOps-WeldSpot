
# Weld Spot - Detecting Defects in Welding

Welding consists in joining metal parts together by melting and cooling them. The process involves heat, chemicals and other materials.
The quality of the welding may vary depending on several factors, like the positions, quantity and quality of the materials, pressure, heat, and so on. Defects that welding may result in include cracks, porosity (e.g., air bubbles), tearing, etc.

To ensure adequate quality of the welding, it is important to test the welding (e.g., by applying weight).
Visual inspection is a prior way to detect common defects.
Weldings made by human and machines can be visually checked in search of such defects.
However, when there are a lot of welding points to check in a structure, a human watcher could overlook or misjudge some.

Having an AI-tool to aid during that step can mitigate some of the human errors and prevent failures in the welding to become a major inconvenience.
This project proposes the use of computer vision to automate the visual inspection of weldings, reducing time, costs and failures.

# Table of Contents
- [Objective](#objective)
- [Structure](#structure)
  - [Data](#data)
  - [Modeling](#data)
  - [Cloud](#data)
    - [Containers](#containers)
  - [Client](#data)
- [Installation](#installation)

# Objective

The goal of this project is to create a minimum viable product (MVP) that allows clients to check the quality of welding with their smartphone cameras.

The MLOps Lifecycle presented in this repository should be a starting point to achieve this goal.

###### NOTE: There are a lot of types of welding, which include different approaches based on the metals, applications, environments, techniques, and so on. This project only focuses on visual detection in generic welding for basic use cases to make it simple.

# Structure

The following is a diagram that shows each part of the project, involving all required parts like client app, data, cloud deployment, etc. This project is centered in MLOps, although DevOps (CI/CD) is also integrated.

![Project Architecture](images/WeldSpot.png)

This project is divided into three main components: The modeling service, the cloud and the client app.

## Data
As it can be observed in the illustration, data for model training comes from two sources:

* [Roboflow - Weld Quality Inspection dataset](https://universe.roboflow.com/welding-2bplp/weld-quality-inspection-rei9l/dataset/9) was found, which offers a staring point to train ML models.
* User feedback to measure drift and retrain with their provided images. **![Privacy Warning](images/Warning.png) THE IMAGES ARE NOT ANONYMIZED OR CENSORED: INTENDED FOR PRIVATE USE**.

When training the models, data is divided in 3 folders, namely "train" for ML training epochs, "valid" for ML validation epochs, and "test" for testing and evaluation.
Each of these folders, at the same time, contains subfolders for each of the possible classes identified: Background (no welding present), Bad Welding, Crack, Excess Reinforcement, Good Welding, Porosity, and Splatters.

The Weld Quality Inspection dataset does not contain "background" images (which may help improve our model learning performance). So I curated a set of random unrelated images for the initial dataset from public sources.

## Modeling
The two processes that communicate with the cloud deployment are developed inside the `modeling` folder: **Dataset Collection** and **Model Training**, with the following structure:

```
modeling/
├──.env: Where required configuration variables are manually set.
├──requirements.txt: Python code dependencies.
├──Makefile: Automation of development processes.
├──Dockerfile: For containerizing the modeling project.
├──options.py: Loads setting variables and files for the python code.
├──app.py: Entry point to execute the modeling service.
├──tests/: Where pytest unit tests are stored.
├──private/: Where private data (e.g., cloud authentication keys) are stored.
├──flows/: Orchestration workflows.
|  ├──register_flows.py: For registering all the prefect flows.
|  ├──collection_pipeline.py: For the Dataset Collection pipeline.
|  └──training_pipeline.py: For the Model Training pipeline.
├──data/: Where datasets are stored.
|  ├──initial/: Where the initial (Roboflow) dataset is stored.
|  ├──raw:/ Where images corrected by users are stored for future trainings.
|  ├──procesed/: Where the preprocessing tasks stores the images.
|  ├──augmented/: Where augmented images are stored after the preprocess.
|  ├──splits/: Where the final, splitted (train, valid, test) versions are stored for training.
|  └──initial.zip: Background class initial split to use with roboflow dataset.
└──service/: Where the rest of the python code is located.

###### NOTE: Some of the paths may be missing and are created when following the [installation instructions](#installation).

```

## Cloud

Two cloud services are employed:

* [Firebase](https://firebase.google.com/) from google, is like GCP but more focused to smartphone apps. Offers a _Spark Plan_ with limited free services.
* [Prefect 2](https://docs.prefect.io/latest/) cloud account is free too. We can run the pipeline in a container and monitor it from the cloud.

Instructions on how to create accounts and configure them are provided in the [Installation](#installation) section.

### Containers

The data collection and model training are built to run on docker container and tested with Ubuntu image.
Because I am using a Windows machine, I installed [Docker Desktop](https://www.docker.com/products/docker-desktop/) and configured it to use [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/windows/wsl/install). Only installing [Docker](https://docs.docker.com/engine/install/) in your system or deploying to cloud should also work.

Instructions on how to generate the docker image are provided in the [Installation](#installation) section.

Additionally, if using WSL, for allowing NVIDIA GPU in model training, the Windows machine should have updated [NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx) installed. This is optional if no NVIDIA GPU is available, but will increase the training speed.

## Client
There is an app based in [example of TFLite plugin for flutter](https://github.com/tensorflow/flutter-tflite/tree/main/example/image_classification_mobilenet).
It is built for android with the APK already included. The project can also be built for iOS, although I haven't tested.

Instructions on how to use and configure the app to work with your Firebase account are provided later.

# Installation

1. Clone this repo (`git clone ...`) if you haven't.

## Requirements

### Local machine

### Cloud accounts

#### [Firebase](https://firebase.google.com/).



#### [Prefect 2](https://docs.prefect.io/latest/).

# Monitoring:
Evidently, WhyLabs/whylogs, ...
https://blog.tensorflow.org/2020/06/enhance-your-tensorflow-lite-deployment-with-firebase.html

https://firebase.google.com/docs/ml/android/use-custom-models?hl=es-419
https://blog.tensorflow.org/2020/06/enhance-your-tensorflow-lite-deployment-with-firebase.html

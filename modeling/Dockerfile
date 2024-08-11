
# The OS image
FROM ubuntu:24.04

# The code directory in the container
WORKDIR /modeling

# Copy the required content in the current local folder to the container
COPY app.py /modeling/app.py
COPY options.py /modeling/options.py
COPY .env /modeling/.env
COPY requirements.txt /modeling/requirements.txt
COPY data /modeling/data
COPY flows /modeling/flows
COPY logs /modeling/logs
COPY private /modeling/private
COPY service /modeling/service
COPY models /modeling/models
COPY __init__.py /modeling/__init__.py

# Install dependencies and Python 3.10
RUN apt update -y && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update -y && \
    apt install -y python3.10 python3.10-venv python3.10-dev

# Create a virtual environment with Python 3.10
RUN python3.10 -m venv /modeling/.venv

# Activate the virtual environment and install requirements
RUN /bin/bash -c "source /modeling/.venv/bin/activate && pip install -r /modeling/requirements.txt"

# Tensorboard port exposed (default 6006)
EXPOSE 6006

# Run app.py when the container launches
CMD ["/modeling/.venv/bin/python", "modeling/app.py"]

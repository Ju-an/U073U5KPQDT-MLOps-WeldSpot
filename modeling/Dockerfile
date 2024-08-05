
# The OS image
FROM ubuntu:24.04

# The code directory in the container
WORKDIR /app

# Copy all the content in the current local folder to the container
COPY . /app

# Setup depenencies
RUN apt update -y && apt install -y python3.12 python3-pip python3-venv & pip3 install -r requirements.txt && pip3 install -r requirements.txt

# No ports exposed as it accesses Firebase Storage and pushes to the Modeling service.

# Run app.py when the container launches
CMD ["python3", "app.py"]

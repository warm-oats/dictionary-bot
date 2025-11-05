# Uses python3.13 as base image
FROM python:3.13

# Copy required files
WORKDIR /app
COPY ./src ./src
COPY ./requirements.txt .
COPY ./setup.py .

# Install requirements
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./src/main.py"]
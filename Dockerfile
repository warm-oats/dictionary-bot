# Uses python3.13 as base image
FROM python:3.13

# Install OpenJDK-21
RUN apt-get update && \
    apt-get install -y openjdk-21-jdk && \
    apt-get install -y ant && \
    apt-get clean;
    
# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME = /usr/lib/jvm/java-21-openjdk-amd64/
RUN export JAVA_HOME

# Copy required files
WORKDIR /app
COPY ./src ./src
COPY ./requirements.txt .
COPY ./setup.py .

# Install requirements
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./src/main.py"]
# Example of Temporal-based application

![CI workflow](https://github.com/oleggorj/temporal-application/.github/workflows/azure-ci-pipeline.yml/badge.svg)

This is a simple application that uses the temporal.io SDK to demonstrate how to use Temporal to orchestrate a workflow.
Intention of this application is to demonstarte how to use Temporal to orchestrate a workflow that involves multiple steps and how to handle failures in the workflow.

## What is this application about?

Initial version of this application is a simple workflow that involves 3 steps:

1. Call API endpoint `/request` to receive and validate a request from a client, it returns a request id along with callback url.
2. API endpoint calls a service to process the request and return a response. Service is Temporal worker that is listening to a task queue.
3. Service creates main long running Temporal workflow that orchestrates the chail workfllows to process long running tasks.
4. Main workflow creates child workflows to process the long running tasks. Each child workflow is responsible for processing a single task.
5. Each child workflow performs the task and returns the result to the main workflow.
6. Another API endpoint `<request id>/status` resposnible for fetching overall status of the workflow, which includes status of each child workflow.

## API Endpoints:

- `/request` - Accepts and validates initial requests
- `/<request_id>/status` - Checks workflow status

## How to run the application:

1. Start the Temporal server using docker-compose:
```bash
docker-compose up
```

2. Start the Temporal worker:
```bash
go run worker/main.go
```

3. Start the Temporal web UI:
```bash
docker run --rm -d -p 8088:8088 --network=host --name temporal-web temporalio/web:1.6.0
```

4. Start the application:
```bash
go run main.go
```

5. Use the following curl commands to interact with the application:

```bash
curl -X POST http://localhost:8080/request
curl -X GET http://localhost:8080/<request_id>/status
```

6. Check the Temporal web UI to see the workflow execution.

## How to run the tests:

```bash
go test ./...
```

## Running the application locally

Setup virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```



## How to run the application in Docker:

1. Build the Docker image:
```bash
docker build -t temporal-application .
```

2. Run the Docker container:
```bash
docker run -p 8080:8080 temporal-application
```

3. Use the following curl commands to interact with the application:

```bash
curl -X POST http://localhost:8080/request

curl -X GET http://localhost:8080/<request_id>/status
```

4. Check the Temporal web UI to see the workflow execution.

## How to run the application in Kubernetes:

1. Start the Minikube cluster:
```bash
minikube start
```

2. Enable the Ingress controller:
```bash
minikube addons enable ingress
```

3. Deploy the Temporal server:
```bash
kubectl apply -f k8s/temporal-server.yaml
```

4. Deploy the Temporal worker:
```bash
kubectl apply -f k8s/temporal-worker.yaml
```

5. Deploy the application:
```bash
kubectl apply -f k8s/temporal-application.yaml
```

6. Get the Minikube IP address:
```bash
minikube ip
```

7. Use the following curl commands to interact with the application:

```bash
curl -X POST http://<minikube_ip>/request

curl -X GET http://<minikube_ip>/<request_id>/status
```

8. Check the Temporal web UI to see the workflow execution.


# Pre-setup: Podman installation

You need **Podman** and **Podman Compose** installed on your system.

---

## Windows

The recommended way is to install [Podman Desktop](https://podman.io/getting-started/installation).

> It also requires **Windows Subsystem for Linux (WSL)**.
> If you do not have it yet, open Windows Terminal and run:

```bash
wsl --install
```

## macOS

The recommended way is to use **Homebrew**:

```bash
brew install podman podman-compose
```

# Task 1 — Wrap Database Service into a Container using Podman

This task continues the microservices project from the previous homework. The goal is to containerize the `database_service` (FastAPI-based) using Podman and run it as a standalone service.

## What Was Done:

- Moved `Dockerfile` to project root.
- Built container image using Podman.
- Ran the container and exposed port 5003.
- Tested all service endpoints via `curl`.
- Verified logs and cleaned up the environment.

## How to Build and Run

### 1. Go to project folder
```bash
cd database_service
```

### 2. Build the image
```bash
podman build -t database-service-image .
```

### 3. Run the container
```bash
podman run -d -p 5003:5003 --name database-service-container database-service-image
```

## Test Endpoints

### Root endpoint
Check that the service is running:
```bash
curl http://localhost:5003/
```

***Expected response:***


### Health check
```bash
curl http://localhost:5003/health
```

***Expected response:***


### Write translation record

```bash
curl -X POST http://localhost:5003/write \
  -H "Content-Type: application/json" \
  -d '{"original_text": "Hello", "translated_text": "Hola", "target_language": "es", "detected_language": "en"}'
```

***Expected response:***

### Read records

```bash
curl http://localhost:5003/read
```

***Expected response:***


## View Logs

```bash
podman logs database-service-container
```

***The response I got:***


## Clean Up

### Stop and remove container

```bash
podman stop database-service-container
podman rm database-service-container
```

### (Optional) Remove image

```bash
podman rmi database-service-image
```

# Task 2 — Multi-Container Setup with Podman Compose

## What Was Done

- Created a second FastAPI service (`scheduler_service`) that calls the first service (`database_service`) every 10 seconds.
- Exposed the first service on port `5003`.
- Configured environment variables and container-to-container communication.
- Used `podman-compose` to build and deploy both services into a common custom network.

## How to Build and Run

### 1. Navigate to the project root

```bash
cd HW6
```

### 2. Run both services

```bash
podman-compose up --build -d
```

### 3. Check container status

```bash
podman ps
```

### 4. View logs

**Database service**

```bash
podman logs database_service
```

It should show entries like:
```
"GET /health HTTP/1.1" 200 OK
```

## Scheduler Behavior

The scheduler_service automatically sends a GET request to http://database_service:5003/health every 10 seconds using httpx.AsyncClient.

You can modify the target via the TARGET_URL environment variable in docker-compose.yaml.

## Clean Up

To remove all containers and images created during the process:

### Stop and remove containers

```bash
podman-compose down
```

### (Optional) Remove images
```bash
podman rmi scheduler-service-compose:latest
podman rmi database-service-compose:latest
```

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

- Created `Dockerfile` for containerization of database service.
- Built container image using Podman.
- Ran the container and exposed port 5003.
- Tested all service endpoints via `curl`.
- Verified logs and cleaned up the environment.

## How to Build and Run

### 1. Go to project folder
```bash
cd hw6
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

<img width="476" alt="image" src="https://github.com/user-attachments/assets/d9cd6d04-5f86-421c-b47d-c68c7352cf01" />


### Health check
```bash
curl http://localhost:5003/health
```

***Expected response:***

<img width="527" alt="image" src="https://github.com/user-attachments/assets/8c809b11-89f4-4725-8720-5eb9ee89bdc1" />


### Write translation record

```bash
curl -X POST http://localhost:5003/write \
  -H "Content-Type: application/json" \
  -d '{"original_text": "Hello", "translated_text": "Hola", "target_language": "es", "detected_language": "en"}'
```

***Expected response:***

```
{"message":"Record saved.","record":{"original_text":"Hello","translated_text":"Hola","target_language":"es","detected_language":"en"}}
```

### Read records

```bash
curl http://localhost:5003/read
```

***Expected response:***

```
{"records":[{"original_text":"Hello","translated_text":"Hola","target_language":"es","detected_language":"en"}]}% 
```

## View Logs

```bash
podman logs database-service-container
```

***The response I got:***

<img width="542" alt="image" src="https://github.com/user-attachments/assets/4b4afbd9-df4d-4eed-98ec-a7e40ab8b1eb" />


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
cd hw6
```

### 2. Run both services

```bash
podman-compose up --build -d
```

### 3. Check container status

```bash
podman ps
```

<img width="1063" alt="image" src="https://github.com/user-attachments/assets/e6767e6d-94c6-484a-b5b4-ba41a2d77708" />


### 4. View logs

**Database service**

```bash
podman logs database_service
```

It should show entries like:
```
"GET /health HTTP/1.1" 200 OK
```

<img width="518" alt="image" src="https://github.com/user-attachments/assets/b8d1efc7-3c9e-4ac0-b925-16a3d1a11c75" />


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

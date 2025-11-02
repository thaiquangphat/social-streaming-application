# Running the Social Streaming Application

This guide provides step-by-step instructions to set up and run the Social Streaming Application.

---

## Prerequisites
1. **Install Docker and Docker Compose**:
   - Ensure Docker and Docker Compose are installed on your system.
   - Verify installation:
     ```powershell
     docker --version
     docker compose --version
     ```

2. **Python**:
   - Python 3.13 is used in the project. Ensure you have Python installed if you plan to run parts of the project locally.

3. **Environment Configuration**:
   - Ensure `.env.kafka` is properly configured for the `social_service`.

---

## Step 1: Build and Start Docker Services

1. **Build Docker Images**:
   ```powershell
   docker compose build
   ```

2. **Start All Services**:
   ```powershell
   docker compose up -d
   ```

3. **Verify Running Containers**:
   Check if all containers are running:
   ```powershell
   docker ps
   ```

---

## Step 2: Running Spark Jobs

1. **Run a Sample with Mock Data**:
   ```powershell
   docker exec -it spark-master spark-submit --master spark://spark-master:7077 /opt/spark-apps/main.py
   ```

2. **Listen to Reddit Submissions**:
   ```powershell
   docker exec -it spark-master `
     spark-submit `
     --master spark://spark-master:7077 `
     /opt/spark-apps/main_kafka.py --mode submissions
   ```

3. **Listen to Reddit Comments**:
   ```powershell
   docker exec -it spark-master `
     spark-submit `
     --master spark://spark-master:7077 `
     /opt/spark-apps/main_kafka.py --mode comments
   ```

---

## Step 3: Running Kafka and `social_service`

1. **Start Kafka Services**:
   Ensure Kafka-related services are running:
   ```powershell
   docker compose up -d broker schema-registry connect
   ```

2. **Verify Kafka Services**:
   Check the logs to ensure Kafka services are ready:
   ```powershell
   docker logs broker
   docker logs schema-registry
   ```

3. **Run `social_service`**:
   - Access the `social_service` container:
     ```powershell
     docker exec -it social_service bash
     ```
   - Synchronize dependencies:
     ```bash
     uv sync
     ```
   - Start the service:
     ```bash
     uv run
     ```

4. **Verify `social_service`**:
   Check the health endpoint:
   ```powershell
   curl http://localhost:8005/health
   ```

---

## Step 4: Stopping Services

1. **Stop All Services**:
   ```powershell
   docker compose down
   ```

2. **Restart Stopped Containers**:
   If containers are stopped but not removed, restart them:
   ```powershell
   docker compose start
   ```

---

## Additional Notes

1. **Rebuilding Images**:
   If you modify `Dockerfile` or dependencies, rebuild the images:
   ```powershell
   docker compose build
   docker compose up -d
   ```

2. **Logs**:
   View logs for any service:
   ```powershell
   docker logs <container_name>
   ```

3. **Health Checks**:
   - Spark Master: `http://localhost:8080`
   - Kafka Broker: `http://localhost:9092`
   - Schema Registry: `http://localhost:8081`
   - `social_service`: `http://localhost:8005/health`

4. **Volumes**:
   - Postgres data: `./infra/postgres_data`
   - Redis data: `./infra/redis_data`

---

This document should cover all steps to successfully run the project. Let me know if you need further clarification!
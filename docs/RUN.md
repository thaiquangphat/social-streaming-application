# Run Guide

Follow these steps to set up dependencies, start Kafka with Docker, and run the Spark streaming consumer and the Reddit producer.

## 1) Install uv

uv manages the virtual environment and dependencies defined in `pyproject.toml`.

- macOS/Linux:
  - `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows (PowerShell):
  - `powershell -c "iwr https://astral.sh/uv/install.ps1 -useb | iex"`

Verify install: `uv --version`

## 2) Sync the virtual environment

From the project root:

- `uv sync`

This creates `.venv` and installs all Python dependencies (including PySpark).

## 3) Start infrastructure with Docker

Ensure Docker is running, then from the project root:

- `docker compose up -d --build`

This launches Kafka (and supporting services). Kafka is exposed on `localhost:9092` as configured in `docker-compose.yml`.

Optional: wait for the broker to become ready:
- `docker compose logs -f broker`

## 4) Prepare two terminals

Open two terminals in the project root directory.

### Terminal A — Start Spark streaming consumer

Run the Spark streaming job to read from Kafka and write processed JSON files locally.

- Default (submissions):
  - `uv run app/spark/streaming.py --bootstrap localhost:9092 --save-dir ./data/spark`

- Optional (comments topic):
  - `uv run app/spark/streaming.py --topic reddit.comments --bootstrap localhost:9092 --save-dir ./data/spark`

Output goes to `./data/spark/kafka/output/<topic>` and checkpoints to `./data/spark/kafka/checkpoints/<topic>`.

### Terminal B — Run the Reddit producer flow

Ensure required environment variables are set in `.env.kafka` (already loaded by the app):

Required keys in `.env.kafka`:
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USER_AGENT`
- `KAFKA_BOOTSTRAP_SERVERS=localhost:9092`
- `KAFKA_CLIENT_ID=prefect-ingestion` (or your preferred ID)

Then run the flow to publish events to Kafka:

- `uv run app/flow.py`

The flow will discover trending Reddit content and publish events to Kafka topics:
- `reddit.submissions` (default)
- `reddit.comments` (if enabled by settings and implemented in the task)

With Terminal A running, processed records will be written under `./data/spark/kafka/output/<topic>`.

## Notes

- If you want to change the write location, set `--save-dir` in the streaming command (or set `SPARK_SAVE_DIR`).
- Spark may print benign warnings (e.g., adaptive execution disabled for streaming, Kafka consumer thread warnings). They do not affect local runs.
- To stop everything: `Ctrl+C` in both terminals, then `docker compose down`.


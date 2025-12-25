# Social Streaming Application

A real-time social media analytics platform that streams, processes, and visualizes Reddit data using modern data engineering tools.

## Overview

This application provides end-to-end streaming analytics for social media data, enabling real-time insights through keyword extraction, clustering, and interactive dashboards.

## Architecture

```
Reddit Data → Kafka → Spark Streaming → Elasticsearch → Kibana
                ↓
            Prefect (Orchestration)
                ↓
            Monitoring (Prometheus + Grafana)
```

## Tech Stack

- **Apache Kafka** - Message broker for data streaming
- **Apache Spark** - Stream processing engine
- **Elasticsearch** - Search and analytics engine
- **Kibana** - Data visualization and dashboards
- **Prefect** - Workflow orchestration
- **Docker** - Containerization
- **Python** - Primary programming language

## Features

- [x] Real-time Reddit data ingestion via Kafka
- [x] Stream processing with data cleaning and transformation
- [x] Keyword extraction and text embedding
- [x] Interactive dashboards with Kibana
- [x] Clustering and pattern detection
- [x] Comprehensive monitoring and metrics

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.x

### Installation

1. Clone the repository:
```bash
git clone https://github.com/thaiquangphat/social-streaming-application.git
cd social-streaming-application
```

2. Start the services:
```bash
docker-compose up -d
```

3. Access the applications:
   - Kibana: `http://localhost:5601`
   - Spark UI: `http://localhost:4040`
   - Prefect UI: `http://localhost:4200`

## Project Structure

```
.
├── src/                    # Source code
├── docs/                   # Documentation
├── monitoring/             # Monitoring configurations
├── jmx_exporter/          # JMX metrics exporter
├── docker-compose.yml     # Service orchestration
├── Dockerfile.kafka       # Kafka container
├── Dockerfile.spark       # Spark container
└── Dockerfile.prefect-worker  # Prefect worker container
```

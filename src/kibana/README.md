# Reddit Analytics Platform 🚀

A real-time Reddit data analytics platform that streams, processes, and visualizes Reddit submissions and comments using Kafka, Spark, Elasticsearch, and Kibana.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.13-green.svg)
![Kibana](https://img.shields.io/badge/Kibana-8.13-purple.svg)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-3.x-orange.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Visualizations](#visualizations)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

This platform provides real-time analytics for Reddit data by:
1. **Streaming** Reddit submissions/comments via Kafka
2. **Processing** data using Apache Spark (keyword extraction, text cleaning, embeddings)
3. **Storing** processed data in Elasticsearch
4. **Visualizing** metrics in Kibana dashboards

---

## 🏗️ Architecture

```
Reddit API
    ↓
Kafka Topics (reddit.submissions, reddit.comments)
    ↓
Apache Spark Processing
    ├── Text Cleaning
    ├── Keyword Extraction
    └── Embedding Generation
    ↓
JSON Output Files
    ↓
inject.py (File Watcher)
    ↓
Elasticsearch Indices
    ├── reddit_submissions
    └── reddit_comments
    ↓
Kibana Dashboard (Real-time Visualization)
```

---

## ✨ Features

### Data Processing
- ✅ Real-time Reddit data ingestion
- ✅ Text cleaning and preprocessing
- ✅ Keyword extraction
- ✅ Text embedding generation
- ✅ Automatic deduplication

### Analytics & Visualizations
- 📊 **12 Real-time Visualizations**:
  - Posts timeline
  - Top subreddits distribution
  - Total posts & average score metrics
  - Keyword cloud & trends
  - Activity heatmap by hour
  - Score distribution histogram
  - Engagement rate tracking
  - Posting velocity (per minute)
  - Top posts leaderboard
  - Comments vs Score correlation

### Performance
- ⚡ Auto-refresh every 5 seconds
- 🔄 Idempotent data ingestion (no duplicates)
- 📈 Scalable architecture
- 💾 Efficient Elasticsearch indexing

---

## 📦 Prerequisites

### Required Software
- **Python 3.8+**
- **Docker & Docker Compose** (for Elasticsearch & Kibana)
- **Apache Spark 3.x**
- **Kafka** (if not using Docker)

### Python Dependencies
```bash
pip install elasticsearch requests
```

---

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd reddit-analytics-platform
```

### 2. Start Elasticsearch & Kibana
```bash
docker-compose up -d elasticsearch kibana
```

Wait for services to start (check with `docker ps`).

### 3. Create Elasticsearch Indices
```bash
python create_index.py
```

Expected output:
```
✅ Created index: reddit_submissions
✅ Created index: reddit_comments
```

### 4. Set Up Kibana Visualizations
```bash
python visualization.py
```

Expected output:
```
=== Original Visualizations ===
✓ Posts Over Time
✓ Top Subreddits
✓ Total Posts
✓ Average Score
✓ Top Keywords
✓ Posts by Hour

=== New Enhanced Visualizations ===
✓ Score Distribution Histogram
✓ Comments vs Score Analysis
✓ Engagement Rate Over Time
✓ Top Posts Table
✓ Keyword Trend Timeline
✓ Posting Velocity

✅ Created 14 objects
```

---

## 💻 Usage

### Start Data Ingestion

#### Step 1: Run Spark Processing
```bash
# Your Spark job that reads from Kafka and outputs JSON files
spark-submit your_spark_job.py
```

#### Step 2: Start File Watcher & Injector
```bash
python inject.py
```

This will:
- Watch the output directory for new JSON files
- Automatically index data to Elasticsearch
- Move processed files to `processed/` folder

Output example:
```
Watching folder: /path/to/output/reddit.submissions
Target index: reddit_submissions
Elasticsearch: your_cluster_name

[SUCCESS] Indexed 150 documents from: part-00001.json
[SUCCESS] Indexed 200 documents from: part-00002.json
```

### Access Dashboard

Open your browser and navigate to:
```
http://localhost:5601/app/dashboards
```

Look for: **"Reddit Analytics Dashboard - Enhanced"**

---

## 📊 Visualizations

### Overview Dashboard Layout

```
┌─────────────────────────┬─────────────────────────┐
│  Posts Over Time (Line) │  Top Subreddits (Pie)  │
├─────────────┬───────────┴─────────────────────────┤
│ Total Posts │ Avg Score │  Keyword Cloud         │
├─────────────┴───────────┼─────────────────────────┤
│   Activity Heatmap      │                         │
├─────────────────────────┼─────────────────────────┤
│  Score Distribution     │  Engagement Timeline    │
├──────────┬──────────┬───┴─────────────────────────┤
│ Keyword  │ Velocity │  Comments vs Score         │
│ Trends   │          │                             │
├──────────┴──────────┴─────────────────────────────┤
│          Top Posts Table (Full Width)             │
└───────────────────────────────────────────────────┘
```

### Visualization Details

| Visualization | Type | Purpose | Key Metrics |
|--------------|------|---------|-------------|
| **Posts Over Time** | Line Chart | Track posting volume | Count by time |
| **Top Subreddits** | Pie Chart | Subreddit distribution | Top 10 by volume |
| **Total Posts** | Metric | Overall count | Real-time total |
| **Average Score** | Metric | Engagement level | Mean upvotes |
| **Keyword Cloud** | Tag Cloud | Trending topics | Top 50 keywords |
| **Activity Heatmap** | Heatmap | Hourly patterns | Posts per hour |
| **Score Distribution** | Histogram | Score spread | Distribution bins |
| **Engagement Timeline** | Line Chart | Score + Comments | Avg over time |
| **Keyword Trends** | Area Chart | Topic evolution | Top 5 keywords |
| **Posting Velocity** | Line Chart | Activity speed | Posts per minute |
| **Comments vs Score** | Table | Top posts | Multi-metric view |
| **Top Posts Table** | Data Table | Leaderboard | Title, score, comments |

---

## 📁 File Structure

```
reddit-analytics-platform/
├── create_index.py           # Creates Elasticsearch indices
├── inject.py                 # Watches and indexes JSON files
├── visualization.py          # Creates Kibana visualizations
├── README.md                 # This file
├── data/
│   └── spark/
│       └── kafka/
│           └── output/
│               ├── reddit.submissions/
│               │   ├── part-00001.json
│               │   └── processed/      # Archived files
│               └── reddit.comments/
└── docker-compose.yml        # Elasticsearch & Kibana setup
```

---

## ⚙️ Configuration

### Elasticsearch Settings (`create_index.py`)

```python
ES_HOST = "http://elasticsearch:9200"

# Index Settings
"number_of_shards": 1
"number_of_replicas": 0
"refresh_interval": "5s"
```

### Inject Settings (`inject.py`)

```python
INDEX_NAME = "reddit_submissions"  # Target index
WATCH_DIR = "/path/to/output/reddit.submissions"
SLEEP_INTERVAL = 5  # Check every 5 seconds
```

### Kibana Settings (`visualization.py`)

```python
KIBANA_URL = "http://localhost:5601"
ES_URL = "http://localhost:9200"

# Dashboard refresh
"refreshInterval": {
    "pause": False,
    "value": 5000  # 5 seconds
}
```

---

## 🔧 Troubleshooting

### Issue: "Index does not exist"
**Solution:**
```bash
python create_index.py
```

### Issue: "Connection refused to Elasticsearch"
**Solution:**
```bash
# Check if Elasticsearch is running
curl http://localhost:9200

# Restart Docker containers
docker-compose restart elasticsearch
```

### Issue: "No visualizations showing in Kibana"
**Solution:**
1. Verify index has data:
   ```bash
   curl http://localhost:9200/reddit_submissions/_count
   ```
2. Check time range in Kibana (top-right corner)
3. Refresh index pattern in Kibana Management

### Issue: "inject.py not processing files"
**Solution:**
- Check file permissions on watch directory
- Verify JSON file format (one JSON object per line)
- Check Elasticsearch connectivity
- Look for error messages in console

### Issue: "Keyword field error"
**Solution:**
- Ensure you're using `payload.subreddit` NOT `payload.subreddit.keyword`
- The field is already mapped as keyword type in the index

---

## 🐛 Common Errors & Fixes

### Error: `"field": "payload.subreddit.keyword" not found`
**Fix:** Change to `"field": "payload.subreddit"` (already keyword type)

### Error: `JSONDecodeError`
**Fix:** Ensure JSON files are in JSONL format (one object per line, not arrays)

### Error: `BulkIndexError`
**Fix:** Check index mapping matches your data structure

### Error: `RequestError: mapper_parsing_exception`
**Fix:** Field type mismatch - recreate index with correct mapping

---

## 📊 Data Schema

### Reddit Submissions Index

```json
{
  "entity_type": "submission",
  "source": "reddit",
  "mode": "streaming",
  "emitted_at": "2024-12-07T10:30:00Z",
  "payload": {
    "id": "abc123",
    "subreddit": "python",
    "author": "user123",
    "title": "Check out my project!",
    "body": "Full post text here...",
    "created_utc": "2024-12-07T10:00:00Z",
    "score": 150,
    "num_comments": 25,
    "url": "https://reddit.com/...",
    "permalink": "/r/python/comments/...",
    "flair": "Project"
  },
  "keywords": ["python", "project", "coding"],
  "clean_body": "cleaned text here",
  "embedding": "base64_encoded_vector"
}
```

### Reddit Comments Index

```json
{
  "entity_type": "comment",
  "payload": {
    "id": "def456",
    "submission_id": "abc123",
    "parent_id": "abc123",
    "subreddit": "python",
    "author": "user456",
    "body": "Great work!",
    "created_utc": "2024-12-07T10:15:00Z",
    "score": 10,
    "controversiality": 0
  }
}
```

---

## 🎯 Performance Tips

1. **Increase refresh interval** for better indexing performance:
   ```python
   "refresh_interval": "30s"  # Default is 5s
   ```

2. **Batch processing**: Process multiple files together in `inject.py`

3. **Optimize Spark**: Increase partitions for larger datasets

4. **Index optimization**: Run occasionally:
   ```bash
   curl -X POST "localhost:9200/reddit_submissions/_forcemerge?max_num_segments=1"
   ```

---

## 🔐 Security Considerations

⚠️ **For Production Use:**

1. Enable Elasticsearch security:
   ```yaml
   xpack.security.enabled: true
   ```

2. Add authentication to `inject.py` and `visualization.py`:
   ```python
   es = Elasticsearch(
       "http://localhost:9200",
       basic_auth=("username", "password")
   )
   ```

3. Use environment variables for credentials:
   ```bash
   export ES_USER="username"
   export ES_PASSWORD="password"
   ```

4. Implement rate limiting for Reddit API calls

---

## 📈 Scaling Recommendations

### For High-Volume Data

1. **Increase Elasticsearch resources**:
   ```yaml
   ES_JAVA_OPTS: "-Xms2g -Xmx2g"
   ```

2. **Add more shards**:
   ```python
   "number_of_shards": 3
   ```

3. **Enable replicas** for redundancy:
   ```python
   "number_of_replicas": 1
   ```

4. **Use Spark cluster** instead of local mode

---

## 📝 Future Enhancements

- [ ] Add sentiment analysis visualization
- [ ] Implement user authentication
- [ ] Add real-time alerts for viral posts
- [ ] Create mobile-responsive dashboard
- [ ] Add export functionality (CSV, PDF)
- [ ] Implement ML-based viral prediction
- [ ] Add subreddit comparison tools
- [ ] Create API for external access

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---
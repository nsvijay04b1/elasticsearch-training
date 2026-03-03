# Lab 18: Downsampling Time-Series Data

## Goal
Create a time-series data stream with sample metrics, then use a Transform to downsample the granular per-second data into summarized per-minute aggregates.

## Scenario
Your infrastructure monitoring system is ingesting CPU and memory metrics every second from 3 servers. After 7 days, you don't need per-second granularity anymore — per-minute averages are sufficient. Downsampling reduces storage costs dramatically while preserving analytical value.

## Prerequisites
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

### 1. Create a Sample Metrics Index with Timestamped Data
```json
PUT server_metrics
{
  "mappings": {
    "properties": {
      "hostname": { "type": "keyword" },
      "cpu_percent": { "type": "float" },
      "memory_percent": { "type": "float" },
      "@timestamp": { "type": "date" }
    }
  }
}
```

**Expected Output:**
```json
{ "acknowledged": true, "shards_acknowledged": true, "index": "server_metrics" }
```

### 2. Insert Sample Time-Series Data
```json
POST server_metrics/_bulk
{"index":{}}
{"hostname": "web-01", "cpu_percent": 45.2, "memory_percent": 68.1, "@timestamp": "2024-10-15T10:00:00Z"}
{"index":{}}
{"hostname": "web-01", "cpu_percent": 52.8, "memory_percent": 70.3, "@timestamp": "2024-10-15T10:00:30Z"}
{"index":{}}
{"hostname": "web-01", "cpu_percent": 48.1, "memory_percent": 69.5, "@timestamp": "2024-10-15T10:01:00Z"}
{"index":{}}
{"hostname": "web-02", "cpu_percent": 30.5, "memory_percent": 55.2, "@timestamp": "2024-10-15T10:00:00Z"}
{"index":{}}
{"hostname": "web-02", "cpu_percent": 35.1, "memory_percent": 57.8, "@timestamp": "2024-10-15T10:00:30Z"}
{"index":{}}
{"hostname": "web-02", "cpu_percent": 33.0, "memory_percent": 56.0, "@timestamp": "2024-10-15T10:01:00Z"}
{"index":{}}
{"hostname": "db-01", "cpu_percent": 78.9, "memory_percent": 85.4, "@timestamp": "2024-10-15T10:00:00Z"}
{"index":{}}
{"hostname": "db-01", "cpu_percent": 82.3, "memory_percent": 87.1, "@timestamp": "2024-10-15T10:00:30Z"}
{"index":{}}
{"hostname": "db-01", "cpu_percent": 80.0, "memory_percent": 86.0, "@timestamp": "2024-10-15T10:01:00Z"}
```

### 3. Verify the Raw Data
```json
GET server_metrics/_count
```

**Expected Output:**
```json
{ "count": 9 }
```

### 4. Create a Transform to Downsample
This Transform groups raw data by `hostname` and 1-minute time intervals, computing the average, min, and max of CPU and memory metrics.
```json
PUT _transform/downsample_metrics
{
  "source": { "index": "server_metrics" },
  "dest": { "index": "server_metrics_1m" },
  "pivot": {
    "group_by": {
      "hostname": { "terms": { "field": "hostname" } },
      "timestamp": { "date_histogram": { "field": "@timestamp", "fixed_interval": "1m" } }
    },
    "aggregations": {
      "avg_cpu": { "avg": { "field": "cpu_percent" } },
      "max_cpu": { "max": { "field": "cpu_percent" } },
      "avg_memory": { "avg": { "field": "memory_percent" } },
      "max_memory": { "max": { "field": "memory_percent" } }
    }
  }
}
```
* **Why?** Storing every single metric every second forever is extremely expensive. Downsampling summarizes the data (e.g., from seconds to minutes), allowing you to keep long-term trends for years while using 90% less disk space.

**Expected Output:**
```json
{ "acknowledged": true }
```

### 5. Start the Transform
```json
POST _transform/downsample_metrics/_start
```

### 6. Verify the Downsampled Data
Wait a few seconds, then query the summarized index:
```json
GET server_metrics_1m/_search
{
  "sort": [{"hostname": "asc"}, {"timestamp": "asc"}]
}
```

**Expected Output (example):**
```json
{
  "hits": {
    "hits": [
      {
        "_source": {
          "hostname": "db-01",
          "timestamp": "2024-10-15T10:00:00.000Z",
          "avg_cpu": 80.4,
          "max_cpu": 82.3,
          "avg_memory": 86.17,
          "max_memory": 87.1
        }
      },
      {
        "_source": {
          "hostname": "web-01",
          "timestamp": "2024-10-15T10:00:00.000Z",
          "avg_cpu": 48.7,
          "max_cpu": 52.8,
          "avg_memory": 69.3,
          "max_memory": 70.3
        }
      }
    ]
  }
}
```
*9 raw documents were compressed into ~6 summarized records — one per hostname per minute!*

### 7. Reclaiming Storage (Manual Deletion)
> **Crucial Concept:** It is important to understand that the downsampling transform creates a **brand new** summarized index (`server_metrics_1m`). It does **not** automatically delete the records from your original raw index (`server_metrics`). 
> 
> To actually reclaim storage capacity on your servers, you must manually delete the original index (or configure an ILM policy in the "Delete" phase to automatically drop the old indices once the transform has safely summarized them).
>
> ```json
> DELETE server_metrics
> ```

---

[Previous Lab: Lab 17](lab17.md) | [Return to Module 5](module5.md) | [Next Lab: Lab 19](../module6/lab19.md)

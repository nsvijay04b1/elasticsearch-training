# Lab 16: Working with Data Streams

## Goal
Create and manage a Data Stream — Elasticsearch's built-in mechanism for handling append-only, time-series data like logs or metrics.

## Scenario
Your monitoring system generates thousands of log events per minute. Instead of manually managing index rollovers, you use a **Data Stream** which automatically handles index creation, rotation, and querying across all backing indices transparently.

## Prerequisites
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management → Dev Tools** in Kibana).*

---

### Understanding the Architecture:
Before we begin, it's crucial to understand how modern data streams are constructed using composable templates:

1. **Component Templates (`logs-mappings`, `logs-settings`):** These are reusable, modular building blocks. You don't apply these directly to indices. Instead, you create separate components for mappings, settings, or aliases so they can be reused across different types of data.
2. **Index Templates (`app-logs-template`):** This acts as the "glue". It defines an index pattern (e.g., `app-logs-*`) and declares which Component Templates should be "composed" together. When a new index matching the pattern is created, the Index Template applies all its underlying building blocks to it.
3. **Data Streams / Indices:** The actual data store. When a document comes in matching the Index Template pattern, Elasticsearch uses the blueprint defined in the Index Template (and its Component Templates) to build the underlying backing index for the Data Stream.

---

### 1. Create a Component Template (Mappings)
Component templates are reusable building blocks. This one defines the field mappings.
```json
PUT _component_template/logs-mappings
{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "message": { "type": "text" },
        "log.level": { "type": "keyword" },
        "service.name": { "type": "keyword" }
      }
    }
  }
}
```

**Expected Output:**
```json
{ "acknowledged": true }
```

### 2. Create a Component Template (Settings)
```json
PUT _component_template/logs-settings
{
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }
}
```

### 3. Create an Index Template for the Data Stream
This template ties the components together and tells Elasticsearch that any index matching `app-logs-*` should be a data stream.
```json
PUT _index_template/app-logs-template
{
  "index_patterns": ["app-logs-*"],
  "data_stream": {},
  "composed_of": ["logs-mappings", "logs-settings"],
  "priority": 500
}
```

**Expected Output:**
```json
{ "acknowledged": true }
```

### 4. Index Documents into the Data Stream
Data streams require a `@timestamp` field. Simply POST documents — the data stream and its backing index are created automatically!
```json
POST app-logs-training/_doc
{
  "@timestamp": "2024-10-15T10:00:00Z",
  "message": "Application started successfully",
  "log.level": "INFO",
  "service.name": "auth-service"
}
```

```json
POST app-logs-training/_doc
{
  "@timestamp": "2024-10-15T10:01:00Z",
  "message": "Failed login attempt from 192.168.1.50",
  "log.level": "WARN",
  "service.name": "auth-service"
}
```

```json
POST app-logs-training/_doc
{
  "@timestamp": "2024-10-15T10:02:00Z",
  "message": "Database connection pool exhausted",
  "log.level": "ERROR",
  "service.name": "payment-service"
}
```

### 5. Verify the Data Stream Exists
```json
GET _data_stream/app-logs-training
```

**Expected Output:**
```json
{
  "data_streams": [
    {
      "name": "app-logs-training",
      "timestamp_field": { "name": "@timestamp" },
      "indices": [
        { "index_name": ".ds-app-logs-training-2024.10.15-000001" }
      ],
      "status": "GREEN",
      "template": "app-logs-template"
    }
  ]
}
```
*Notice how Elasticsearch automatically created a backing index (`.ds-app-logs-training-...000001`).*

### 6. Search the Data Stream
You query the data stream name directly — Elasticsearch searches across all backing indices transparently.
```json
GET app-logs-training/_search
{
  "query": {
    "match": { "log.level": "ERROR" }
  }
}
```

**Expected Output:**
```json
{
  "hits": {
    "total": { "value": 1 },
    "hits": [
      { "_source": { "message": "Database connection pool exhausted", "log.level": "ERROR", "service.name": "payment-service" } }
    ]
  }
}
```

### 7. View the Backing Indices
```json
GET _cat/indices/.ds-app-logs-*?v&h=index,docs.count,store.size
```

**Expected Output:**
```text
index                                       docs.count store.size
.ds-app-logs-training-2024.10.15-000001              3       8kb
```

---

### Key Concepts
| Feature | Regular Index | Data Stream |
|---------|:---:|:---:|
| Append-only (no updates/deletes) | ❌ | ✅ |
| Auto-creates backing indices | ❌ | ✅ |
| Requires `@timestamp` | ❌ | ✅ |
| Transparent multi-index search | ❌ | ✅ |
| Works with ILM for auto-rollover | Manual setup | Built-in |

---

[Previous Lab: Lab 15](lab15.md) | [Return to Module 5](module5.md) | [Next Lab: Lab 17](lab17.md)

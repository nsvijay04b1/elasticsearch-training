# Lab 9: Explicit Mappings & Ingest Pipelines

## Goal
Use Kibana Dev Tools to define an explicit mapping (preventing Mapping Explosions) and create an ingest pipeline to add timestamps to incoming data.

## Scenario
Your application sends sparse log data that doesn't include a timestamp. You need Elasticsearch to append the exact time the log was received. Additionally, you want to strictly control the mapping so that the `status` field is only ever treated as a `keyword` for exact filtering, and `message` as `text` for full-text search.

## Prerequisites
- Completion of Lab 4.
- Kibana must be running and accessible via your web browser.
- You must be logged into the Kibana Web UI.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

### 1. Create an Ingest Pipeline
This pipeline uses the `set` processor to add a field called `ingest_time`.
```json
PUT _ingest/pipeline/my_pipeline
{
  "description": "Add timestamp on ingest",
  "processors": [
    {
      "set": { "field": "ingest_time", "value": "{{_ingest.timestamp}}" }
    }
  ]
}
```

**Expected Output:**
```json
{ "acknowledged": true }
```

### 2. Create an index with an Explicit Mapping
We enforce that `status` cannot be tokenized (keyword only) and `message` supports full-text search.
```json
PUT my_logs
{
  "mappings": {
    "properties": {
      "status": { "type": "keyword" },
      "message": { "type": "text" }
    }
  }
}
```

**Expected Output:**
```json
{ "acknowledged": true, "shards_acknowledged": true, "index": "my_logs" }
```

### 3. Index a document using the new pipeline
Note the `?pipeline=my_pipeline` parameter.
```json
POST my_logs/_doc/1?pipeline=my_pipeline
{
  "status": "ERROR",
  "message": "Failed to connect to the database securely."
}
```

**Expected Output:**
```json
{ "_index": "my_logs", "_id": "1", "result": "created" }
```

### 4. Retrieve the document to verify the injected timestamp
```json
GET my_logs/_doc/1
```

**Expected Output:**
```json
{
  "_index": "my_logs",
  "_id": "1",
  "_source": {
    "status": "ERROR",
    "message": "Failed to connect to the database securely.",
    "ingest_time": "2024-10-15T14:32:01.123456Z"
  }
}
```
*The `ingest_time` field was automatically populated by the pipeline!*

### 5. Verify the Mapping
```json
GET my_logs/_mapping
```

**Expected Output:**
```json
{
  "my_logs": {
    "mappings": {
      "properties": {
        "ingest_time": { "type": "date" },
        "message": { "type": "text" },
        "status": { "type": "keyword" }
      }
    }
  }
}
```

---

[Previous Lab: Lab 8](lab8.md) | [Return to Module 3](module3.md) | [Next Lab: Lab 10](../module4/lab10.md)

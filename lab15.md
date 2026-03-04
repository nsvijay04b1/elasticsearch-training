# Lab 15: Implementing Index Lifecycle Management (ILM)

## Goal
Create an automated ILM policy to roll over an index when it gets too large, and eventually delete it when it grows too old.

## Scenario
You are collecting daily log data from a swarm of microservices. To prevent the cluster's disk from filling up, you need a policy that automatically rolls over the active write-index when it hits 50GB or 1 day old, and deletes data after 30 days.

## Prerequisites
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

### 1. Create the ILM Policy
```json
PUT _ilm/policy/logs_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": { 
          "rollover": { "max_age": "1d", "max_size": "50gb" } 
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": { "delete": {} }
      }
    }
  }
}
```
* **Why?** Index Lifecycle Management (ILM) is essential for production clusters. It automates the "grunt work" of managing data, ensuring you don't run out of disk space by automatically rolling over active indices and deleting old ones.

**Expected Output:**
```json
{ "acknowledged": true }
```

### 2. Verify Policy Creation
```json
GET _ilm/policy/logs_policy
```

**Expected Output:**
```json
{
  "logs_policy": {
    "policy": {
      "phases": {
        "hot": { "actions": { "rollover": { "max_age": "1d", "max_size": "50gb" } } },
        "delete": { "min_age": "30d", "actions": { "delete": {} } }
      }
    }
  }
}
```

### 3. Create an Index Template that Attaches the Policy
This template automatically applies `logs_policy` to any new index matching the `logs-*` pattern.

> **Important Notes on Index Templates:**
> 1. **New Indices Only:** Index templates are only applied during index creation. They do **not** affect existing indices that already match the pattern.
> 2. **Override Precedence:** If you provide explicit index settings or mappings in your `PUT` request when manually creating an index, those explicit settings will **override** any matching settings defined in the index template.

```json
PUT _index_template/logs_template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "index.lifecycle.name": "logs_policy",
      "index.lifecycle.rollover_alias": "logs"
    }
  }
}
```
* **Why?** Connecting a policy to an index template is the "set it and forget it" step. Any new index matching `logs-*` will now automatically inherit your retention and rollover rules.

**Expected Output:**
```json
{ "acknowledged": true }
```

### 4. Create the Initial Write Index
The `is_write_index` flag tells Elasticsearch this is the active index for new writes.
```json
PUT logs-000001
{
  "aliases": {
    "logs": { "is_write_index": true }
  }
}
```

**Expected Output:**
```json
{ "acknowledged": true, "shards_acknowledged": true, "index": "logs-000001" }
```

### 5. Index a Sample Document via the Alias
```json
POST logs/_doc
{
  "message": "Service started successfully",
  "level": "INFO",
  "@timestamp": "2024-10-15T10:00:00Z"
}
```

### 6. Verify ILM is Attached
```json
GET logs-000001/_ilm/explain
```

**Expected Output:**
```json
{
  "indices": {
    "logs-000001": {
      "index": "logs-000001",
      "managed": true,
      "policy": "logs_policy",
      "phase": "hot"
    }
  }
}
```

---

[Previous Lab: Lab 14](../module4/lab14.md) | [Return to Module 5](module5.md) | [Next Lab: Lab 16](lab16.md)

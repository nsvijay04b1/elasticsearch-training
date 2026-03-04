# Lab 22: Security Threat Hunting

## Objective
Learn to ingest simulated authentication logs and use ES|QL to detect brute force attacks and visualize anomalies.

## Prerequisites
- Elasticsearch and Kibana are running.
- Access to Kibana Dev Tools.

## Steps

### Step 1: Create an Ingest Pipeline for Logs
We need a pipeline to simulate parsing incoming security logs and adding a processing timestamp.

```json
PUT _ingest/pipeline/auth_logs_pipeline
{
  "description": "Pipeline for authentication logs",
  "processors": [
    {
      "set": {
        "field": "event.ingested",
        "value": "{{_ingest.timestamp}}"
      }
    }
  ]
}
```

### Step 2: Ingest Dummy Authentication Data
Let's simulate a brute force attack by indexing several failed login attempts followed by a successful one from the same IP.

```json
POST auth-logs/_bulk?pipeline=auth_logs_pipeline
{"index":{}}
{"@timestamp":"2024-10-25T10:00:01Z","source":{"ip":"192.168.1.100"},"user":{"name":"admin"},"event":{"action":"login","outcome":"failure"},"host":{"name":"sec-gateway-1"}}
{"index":{}}
{"@timestamp":"2024-10-25T10:00:03Z","source":{"ip":"192.168.1.100"},"user":{"name":"admin"},"event":{"action":"login","outcome":"failure"},"host":{"name":"sec-gateway-1"}}
{"index":{}}
{"@timestamp":"2024-10-25T10:00:05Z","source":{"ip":"192.168.1.100"},"user":{"name":"admin"},"event":{"action":"login","outcome":"failure"},"host":{"name":"sec-gateway-2"}}
{"index":{}}
{"@timestamp":"2024-10-25T10:00:07Z","source":{"ip":"192.168.1.100"},"user":{"name":"admin"},"event":{"action":"login","outcome":"failure"},"host":{"name":"sec-gateway-1"}}
{"index":{}}
{"@timestamp":"2024-10-25T10:00:10Z","source":{"ip":"192.168.1.100"},"user":{"name":"admin"},"event":{"action":"login","outcome":"success"},"host":{"name":"sec-gateway-1"}}
{"index":{}}
{"@timestamp":"2024-10-25T10:05:00Z","source":{"ip":"10.0.0.50"},"user":{"name":"jdoe"},"event":{"action":"login","outcome":"success"},"host":{"name":"sec-gateway-1"}}
{"index":{}}
{"@timestamp":"2024-10-25T10:08:00Z","source":{"ip":"203.0.113.45"},"user":{"name":"root"},"event":{"action":"login","outcome":"failure"},"host":{"name":"sec-gateway-3"}}
{"index":{}}
{"@timestamp":"2024-10-25T10:08:01Z","source":{"ip":"203.0.113.45"},"user":{"name":"root"},"event":{"action":"login","outcome":"success"},"host":{"name":"sec-gateway-3"}}
```

### Step 3: Detect Brute Force using ES|QL
Use the Elasticsearch Query Language (ES|QL) to find source IPs that have more than 3 failed login attempts.

```text
POST /_query?format=txt
{
  "query": """
    FROM auth-logs
    | WHERE event.action == "login" AND event.outcome == "failure"
    | STATS failed_attempts = COUNT(event.outcome) BY source.ip, user.name
    | WHERE failed_attempts > 3
    | SORT failed_attempts DESC
  """
}
```

**Why?** This lab introduces ES|QL, the new pipe-based query language. Notice how much easier it is to write `STATS failed_attempts = COUNT(...) BY source.ip` compared to the deeply nested aggregations (terms aggs, value_count aggs) you would need in standard Query DSL.

### Expected Output
You should see that the IP `192.168.1.100` is flagged for having 4 failed attempts against the `admin` user.

```text
source.ip    |user.name|failed_attempts
-------------+---------+---------------
192.168.1.100|admin    |4              
```

### Step 4: Map the Attack Timeline
Let's look at the timeline of events for the suspicious IP using ES|QL to see if they eventually got in.

```text
POST /_query?format=txt
{
  "query": """
    FROM auth-logs
    | WHERE source.ip == "192.168.1.100"
    | KEEP @timestamp, user.name, event.outcome
    | SORT @timestamp ASC
  """
}
```

This sequence represents a classic brute force followed by a potential compromise.

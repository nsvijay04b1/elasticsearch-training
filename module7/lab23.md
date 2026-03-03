# Lab 23: Application Debugging

## Objective
Correlate application logs with APM traces to find slow processing transactions and debug unhandled exceptions.

## Prerequisites
- Familiarity with Query DSL and indexing.
- Kibana Dev Tools access.

## Steps

### Step 1: Create the Logs and Traces Indices
We'll create two indices: one for application structured logs and another simulating APM trace data. Both share a common `trace.id`.

```json
PUT app-logs
{
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "trace.id": { "type": "keyword" },
      "message": { "type": "text" },
      "log.level": { "type": "keyword" }
    }
  }
}

PUT apm-traces
{
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "trace.id": { "type": "keyword" },
      "transaction.duration.us": { "type": "long" },
      "transaction.name": { "type": "keyword" },
      "transaction.result": { "type": "keyword" }
    }
  }
}
```

### Step 2: Populate Dummy Application Data
Insert data simulating a slow transaction and an application crash.

```json
POST _bulk
{"index":{"_index":"apm-traces"}}
{"@timestamp":"2024-10-25T11:00:00Z", "trace.id":"trace-123", "transaction.name":"GET /api/users", "transaction.duration.us": 15000, "transaction.result":"HTTP 2xx"}
{"index":{"_index":"app-logs"}}
{"@timestamp":"2024-10-25T11:00:00Z", "trace.id":"trace-123", "log.level":"INFO", "message":"Fetching user profile"}
{"index":{"_index":"apm-traces"}}
{"@timestamp":"2024-10-25T11:05:00Z", "trace.id":"trace-456", "transaction.name":"POST /api/checkout", "transaction.duration.us": 8500000, "transaction.result":"HTTP 5xx"}
{"index":{"_index":"app-logs"}}
{"@timestamp":"2024-10-25T11:05:01Z", "trace.id":"trace-456", "log.level":"ERROR", "message":"Database connection timeout"}
{"index":{"_index":"app-logs"}}
{"@timestamp":"2024-10-25T11:05:05Z", "trace.id":"trace-456", "log.level":"FATAL", "message":"Unhandled RuntimeException: Null pointer during checkout phase"}
{"index":{"_index":"apm-traces"}}
{"@timestamp":"2024-10-25T11:10:00Z", "trace.id":"trace-789", "transaction.name":"POST /api/login", "transaction.duration.us": 7200000, "transaction.result":"HTTP 4xx"}
{"index":{"_index":"app-logs"}}
{"@timestamp":"2024-10-25T11:10:01Z", "trace.id":"trace-789", "log.level":"WARN", "message":"Authentication service responded slowly"}
{"index":{"_index":"app-logs"}}
{"@timestamp":"2024-10-25T11:10:04Z", "trace.id":"trace-789", "log.level":"ERROR", "message":"Invalid credentials supplied by user"}
```

### Step 3: Identify Slow Transactions (> 5 seconds)
Search the APM traces for any API calls taking abnormally long (greater than 5,000,000 microseconds).

```json
GET apm-traces/_search
{
  "_source": ["trace.id", "transaction.name", "transaction.duration.us"],
  "query": {
    "range": {
      "transaction.duration.us": {
        "gt": 5000000
      }
    }
  }
}
```

**Note the `trace.id` returned. It should be `trace-456`.**

### Step 4: Correlate Trace with Application Logs
Take the `trace.id` from the slow/failed transaction and look up the exact logs that occurred during that request.

```json
GET app-logs/_search
{
  "query": {
    "term": {
      "trace.id": "trace-456"
    }
  },
  "sort": [
    { "@timestamp": "asc" }
  ]
}
```


### Insights
By searching the logs associated with `trace-456`, we instantly see that a "Database connection timeout" led to an "Unhandled RuntimeException", explaining the 8.5 second duration and the HTTP 5xx error. This represents the core workflow of APM Log Correlation.

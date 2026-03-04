# Lab 24: Day 2 - Performance Troubleshooting

## Objective
Use Elasticsearch monitoring APIs to diagnose high CPU usage and utilize the Profile API to debug slow queries.

## Prerequisites
- Working Elasticsearch Cluster.
- Kibana Dev Tools.

## Steps

### Step 1: Diagnose High CPU / Load with Nodes Hot Threads
When an Elasticsearch node is responding slowly or consuming 100% CPU, the `_nodes/hot_threads` API is the fastest way to pinpoint what the JVM is actually doing.

Run the following command:
```json
GET _nodes/hot_threads?threads=3
```

**What to look for:**
- If threads are stuck in `Lucene.search`, the cluster is under heavy search load.
- If threads are in `write` or `merge`, the cluster is under heavy indexing pressure.
- If threads are in `GC` (Garbage Collection), the node is suffering from heap memory pressure.

**Why?** Monitoring dashboards only tell you that a node *is* slow. The `hot_threads` API tells you *where* it is slow. It's a live "X-ray" of the Java process, allowing you to catch problematic queries or internal bottlenecks in real-time.

### Step 2: Use the Task Management API
Sometimes a single massive query or reindex operation can drag down performance. The Tasks API shows what is currently executing in the cluster.

```json
GET _tasks?detailed=true&actions=*search*
```
This shows all currently running search tasks across all nodes. If a task has been running for an unusually long time, you can cancel it using `POST _tasks/<task_id>/_cancel`.

### Step 3: Create a Complex Query for Profiling
Let's index a few documents and write a poorly optimized query with a wildcard.

```json
POST sample-data/_bulk
{"index":{}}
{"text": "Elasticsearch is a distributed, RESTful search and analytics engine"}
{"index":{}}
{"text": "Kibana lets you visualize your Elasticsearch data"}
{"index":{}}
{"text": "Logstash is a server-side data processing pipeline"}
```

Now, run a query with `profile: true`. We will use a leading wildcard which is notoriously slow.

```json
GET sample-data/_search
{
  "profile": true,
  "query": {
    "wildcard": {
      "text": {
        "value": "*search*"
      }
    }
  }
}
```

### Step 4: Analyze the Profile Output
Look closely at the JSON response.

3. You will notice the `MultiTermQueryConstantScoreWrapper` taking up the majority of the time, demonstrating the cost of evaluating leading wildcards.

**Why?** The Profile API is essential for query optimization. Instead of guessing why a query is slow, it provides a nanosecond-level breakdown of every Lucene operation, helping you prove to developers that certain patterns (like leading wildcards) are mathematically expensive.

### Best Practice
Instead of wildcards, rely on `text` field analysis and standard `match` queries for full-text search, keeping wildcards only for highly specific, bounded use cases.

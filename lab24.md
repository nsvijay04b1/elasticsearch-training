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

Here is the complete operational guide connecting **ILM Rollover**, **Hot Threads**, **Query Profiling**, and **Cluster Allocation** in a structured Markdown format.

---

# 🛠️ Elasticsearch Operations & Troubleshooting Guide

This guide connects high-level automation (ILM) with deep-dive diagnostic tools (`hot_threads`, `profile`, `allocation/explain`).

## 1. The Strategy: Index Lifecycle Management (ILM)

The **Rollover** action is the heartbeat of your cluster. It prevents indices from growing so large that they become unmanageable (high CPU, slow recovery).

```json
PUT _ilm/policy/advanced_logs_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": { "max_primary_shard_size": "50gb", "max_age": "1d" }
        }
      },
      "warm": {
        "min_age": "2d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 }
        }
      }
    }
  }
}

```

---

## 2. The "Escape Hatch": Diagnosing CPU Spikes

When your ILM policy is active but the cluster is unresponsive, use `hot_threads`. This tells you if the CPU is busy with **Indexing** (too many small writes) or **Searching** (heavy queries).

### Identifying High CPU Tasks

```bash
# See what Java is doing right now (Top 3 threads)
GET _nodes/hot_threads?threads=3

# Identify the specific search task causing the spike
GET _tasks?detailed=true&actions=*search*

```

---

## 3. The Drill-Down: Profiling Slow Queries

If `hot_threads` points to a search bottleneck, use the `profile` API. This is critical for catching "expensive" patterns like **leading wildcards**.

### Why Leading Wildcards are "Illegal" in Production

```json
GET _search
{
  "profile": true,
  "query": {
    "wildcard": {
      "message": { "value": "*search*" }
    }
  }
}

```

* **The Problem:** `*search*` forces Lucene to scan every term.
* **The Output:** Look for `MultiTermQueryConstantScoreWrapper`. If the `time_in_nanos` here is high, your query is the reason for the cluster lag.

---

## 4. The "Homeless" Shard: Allocation Explain

If your ILM policy fails to move an index to the **Warm** phase, the index may turn **Yellow** or **Red**. `_cluster/allocation/explain` is the only way to see why a shard is "stuck."

### Diagnose Stuck Allocations

```json
GET _cluster/allocation/explain
{
  "index": "resilient-index", 
  "shard": 0, 
  "primary": true
}

```

* **Decider Result:** If you see `node_match: NO`, your ILM policy is trying to move data to a node attribute (like `high_io`) that doesn't exist.

---

## 5. The "Safety Switch": Rolling Restarts

To fix a "Hot Thread" issue (like a hung process), you may need to restart a node. **Never** stop the daemon without disabling allocation first, or you will trigger a catastrophic "shard storm."

### The Procedure

| Step | Action | Command |
| --- | --- | --- |
| **1** | **Disable Allocation** | `PUT _cluster/settings { "persistent": { "cluster.routing.allocation.enable": "none" } }` |
| **2** | **Restart Node** | Stop/Start the Elasticsearch Service. |
| **3** | **Re-enable Allocation** | `PUT _cluster/settings { "persistent": { "cluster.routing.allocation.enable": "all" } }` |

---

## Summary: Connecting the Tools

1. **ILM Rollover** keeps your shards at the "sweet spot" (50GB) to prevent performance decay.
2. **Hot Threads** identifies if a node is struggling with the current ILM workload.
3. **Profile API** proves why a specific query is bypassing your performance optimizations.
4. **Allocation Explain** fixes the "stuck" state when ILM transitions between Hot and Warm phases.

**Would you like me to generate a specific monitoring dashboard query to track these rollover events in real-time?**


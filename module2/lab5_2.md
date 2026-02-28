# Lab 5.2: Advanced Troubleshooting Concepts

## Goal
Identify common issues within an Elasticsearch cluster, such as Unassigned Shards, Thread Pool rejections, and memory pressure.

## Scenario
The cluster health alert has triggered in your production monitoring system. You need to identify whether a shard is unassigned due to disk space issues, node failures, or misconfigured routing rules. You also need to verify memory usage.

## Prerequisites
- Completion of Lab 5.
- Elasticsearch must be running securely.
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

1. **Check Overall Cluster Health:**
   Get a high-level view of the cluster state (Green, Yellow, or Red).
   ```json
   GET _cluster/health
   ```

2. **Diagnose Unassigned Shards:**
   If the health is Yellow or Red, discover exactly *why* Elasticsearch is refusing to allocate shards. The Allocation Explain API is the most powerful tool for this.
   ```json
   GET _cluster/allocation/explain
   ```
   *Look at the `deciders` block in the output. It will tell you exactly which node rejected the shard and why (e.g., "node does not match index allocation filtering" or "the node is above the high watermark cluster setting").*

3. **Check Node Resource Usage (Heap and Disk):**
   Memory pressure or disk space filling up (hitting watermarks) are the top reasons clusters fail. Verify heap percent and disk percent.
   ```json
   GET _cat/nodes?v&h=name,heap.percent,ram.percent,cpu,disk.used_percent
   ```

4. **Verify Thread Pool Rejections:**
   If clients are complaining about timeouts or HTTP 429 Too Many Requests errors, check if your internal thread pools are rejecting tasks because they are overwhelmed.
   ```json
   GET _cat/thread_pool/search,write?v&h=node_name,name,active,queue,rejected
   ```
   *If the `rejected` count is steadily climbing, the cluster is receiving more concurrent requests than it has threads available to process them.*

5. **Examine the Pending Tasks Queue:**
   If Master nodes are overwhelmed (perhaps due to a Mapping Explosion of thousands of dynamic fields), cluster state updates will back up.
   ```json
   GET _cluster/pending_tasks
   ```

---
[Previous Lab: Lab 5](lab5.md) | [Return to Module 2](module2.md) | [Next Lab: Lab 6](../module3/lab6.md)

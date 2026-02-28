# Lab 5: Simulating & Troubleshooting Cluster Issues

## Goal
Understand why a cluster turns yellow by intentionally breaking the allocation rules, and use the Allocation Explain API to troubleshoot.

## Scenario
You get an alert at 3:00 AM stating the Elasticsearch cluster has entered a `Yellow` health state. You need to identify *exactly* why shards are unassigned. 

*(Since our local cluster is a single node, we can simulate this by requesting a replica, which Elasticsearch will refuse to assign to the same node as the primary!)*

## Prerequisites
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

1. **Check the current cluster health:**
   ```json
   GET _cluster/health
   ```
   *Note the cluster status.*

2. **Break the rules:**
   Create an index that explicitly demands 1 Replica. Since your cluster only has 1 Data Node, Elasticsearch cannot assign the replica safely.
   ```json
   PUT /troubleshoot_index
   { 
     "settings": { "number_of_replicas": 1 } 
   }
   ```

3. **Check the cluster health again:**
   ```json
   GET _cluster/health
   ```
   *The cluster should now be in a `Yellow` state!*

4. **Ask Elasticsearch why it's Yellow:**
   The Allocation Explain API gives you the exact reason why a shard is unassigned.
   ```json
   GET _cluster/allocation/explain
   ```
   *Look through the `"decisions"` array in the response. You should see an explanation stating: `the node is on the same host as the primary shard` or similar, indicating it is waiting for a 2nd Data Node to join the cluster.*


### Part 2: Advanced Troubleshooting Concepts


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

---

---
[Previous Lab: Lab 4](lab4.md) | [Return to Module 2](module2.md) | [Next Lab: Lab 6](../module3/lab6.md)

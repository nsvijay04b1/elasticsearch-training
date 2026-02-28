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

---

---

---
[Previous Lab: Lab 5](../module2/lab5.md) | [Return to Module 3](module3.md) | [Next Lab: Lab 7](lab7.md)

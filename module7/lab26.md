# Lab 26: Day 2 - Cluster Resilience

## Objective
Diagnose complex shard allocation failures and perform a simulated rolling restart configuration.

## Prerequisites
- Kibana Dev Tools.

## Steps

### Step 1: Simulate a Routing Allocation Failure
We are going to purposefully configure an index with requirements that our single-node (or basic) cluster cannot satisfy.

```json
PUT resilient-index
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "index.routing.allocation.require.storage": "high_io"
  }
}
```
*Note: Because none of our nodes have the attribute `node.attr.storage: high_io`, this index will be stuck in a YELLOW or RED state.*

### Step 2: Use Allocation Explain API
When shards won't initialize or migrate, the `_cluster/allocation/explain` API is the definitive way to find out why.

```json
GET _cluster/allocation/explain
{
  "index": "resilient-index",
  "shard": 0,
  "primary": true
}
```

### Expected Output
Look at the `deciders` portion of the response. You should see `node_match` returning `NO` because the node does not match the requested `storage: high_io` attribute.

### Step 3: Fix the Allocation Issues
Remove the impossible routing requirement to let the cluster automatically recover the shard.

```json
PUT resilient-index/_settings
{
  "index.routing.allocation.require.storage": null
}
```
Run `GET _cat/indices/resilient-index?v` and observe the state transition to `GREEN`.

### Step 4: Preparing for a Node Restart (Day 2 Ops)
When doing maintenance (OS patching, elasticsearch version upgrade) on a cluster, you must prevent the cluster from frantically rebuilding shards while a node is temporarily rebooting. 

**Before stopping the Elasticsearch service on a node, disable allocation:**
```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "none"
  }
}
```

*(At this point, you would restart the systemd service or VM).*

**After the node joins the cluster again, re-enable allocation:**
```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "all"
  }
}
```
This procedure is the hallmark of zero-downtime rolling upgrades.

# Lab 25: Day 2 - Advanced Data Lifecycle

## Objective
Create an Index Lifecycle Management (ILM) policy that covers the entire data journey: Hot (rollover), Warm (shrink), Cold, and Delete phases.

## Prerequisites
- Kibana Dev Tools.

## Steps

### Step 1: Define the Advanced ILM Policy
We will define a policy named `advanced_logs_policy`.

- **Hot Phase:** Rollover when the index reaches 50GB or is 1 day old.
- **Warm Phase:** Move to warm after 2 days, shrink to a single primary shard.
- **Cold Phase:** Move to cold after 7 days to save on storage costs (requires cold tier nodes in a real cluster).
- **Delete Phase:** Delete data after 30 days.

```json
PUT _ilm/policy/advanced_logs_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "1d"
          }
        }
      },
      "warm": {
        "min_age": "2d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "7d",
        "actions": {
          "set_priority": {
            "priority": 0
          }
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### Step 2: Create an Index Template attached to the Policy
We must ensure that any new logs generated align with the policy we created.

```json
PUT _index_template/logs_template
{
  "index_patterns": ["syslogs-*"],
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1,
      "index.lifecycle.name": "advanced_logs_policy",
      "index.lifecycle.rollover_alias": "syslogs"
    }
  }
}
```

### Step 3: Bootstrap the First Index
To use rollover, the initial index must be created manually with the correct alias and write permissions.

```json
PUT syslogs-000001
{
  "aliases": {
    "syslogs": {
      "is_write_index": true
    }
  }
}
```

### Step 4: Verify the Policy Application
Check the explanation of the ILM status on your new index to ensure it was picked up correctly.

```json
GET syslogs-000001/_ilm/explain
```

### Expected Output
You should see `"step": "check-rollover-ready"` indicating that ILM is successfully monitoring the index against your `advanced_logs_policy` parameters.

# Lab 12: Implementing Index Lifecycle Management (ILM)

## Goal
Create an automated ILM policy to roll over an index when it gets too large, and eventually delete it when it grows too old.

## Scenario
You are collecting daily log data from a swarm of microservices. To prevent the cluster's disk from filling up, you need a policy that automatically rolls over the active write-index when it hits 50GB or 1 day old, and deletes data after 30 days.

## Prerequisites
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

1. **Create the ILM Policy:**
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

2. **Verify Policy Creation:**
   ```json
   GET _ilm/policy/logs_policy
   ```

*(In a real production environment, you would then create an Index Template that applies `logs_policy` to any new indices matching the pattern `logs-*`).*

---

---

---
[Previous Lab: Lab 11](../module4/lab11.md) | [Return to Module 5](module5.md) | [Next Lab: Lab 13](lab13.md)

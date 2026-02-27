# Lab 10: Analyzing Search Performance

## Goal
Use the Profile API to peek under the hood at Lucene's execution times, allowing you to troubleshoot slow queries.

## Scenario
A user complains that searches for "shoe" are suddenly taking a long time. You need to verify exactly how many milliseconds the internal Lucene token-matching took.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

1. **Execute a Query with Profiling Enabled:**
   Adding `"profile": true` forces Elasticsearch to attach a detailed timing breakdown to the end of the JSON response.
   ```json
   GET products/_search
   {
     "profile": true,
     "query": { "match": { "name": "shoe" } }
   }
   ```

2. **Review the Profile Response:**
   - Look for the `"profile"` object at the bottom of the response.
   - Expand `"shards"` -> `"0"` -> `"searches"` -> `"query"`.
   - Observe the `"time_in_nanos"` statistic. This tells you the exact execution time down to the nanosecond level. In giant clusters, this is how you identify if a particular regex or script query is causing high latency.

---
[Return to Module 4](module-4.md)

# Lab 10: Aggregations Framework

## Goal
Execute structured searches in Kibana Dev Tools to understand the deep difference between scoring a document via `must` (Query Context) versus exact filtering via `filter` (Filter Context).

## Scenario
You need to search the `products` index created back in Lab 5. Users are looking for the word "shoe", but they only want to see results that cost less than $100.

## Prerequisites
- Completion of Lab 11 (The `products` index must exist).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

1. **Execute a Mixed Context Search:**
   ```json
   GET products/_search
   {
     "query": {
       "bool": {
         "must": { 
           "match": { "name": "shoe" } 
         },
         "filter": { 
           "range": { "price": { "lt": 100 } } 
         }
       }
     }
   }
   ```

2. **Analyze the Results:**
   - Look at the `_score` field in the response. The document matched the word "shoe", so BM25 gave it a relevance score!
   - Notice how the `filter` block simply acted as a binary gate (Yes/No if `< 100`) without affecting the score.

3. **Swap context to see the difference:**
   Move the `match` query down into the `filter` block.
   ```json
   GET products/_search
   {
     "query": {
       "bool": {
         "filter": [
           { "match": { "name": "shoe" } },
           { "range": { "price": { "lt": 100 } } }
         ]
       }
     }
   }
   ```
   - Execute it again. Observe that the `_score` is now exactly `0.0`. You have traded relevance ranking for pure caching speed.

---

---

---
[Previous Lab: Lab 9](lab9.md) | [Return to Module 4](module4.md) | [Next Lab: Lab 11](lab11.md)

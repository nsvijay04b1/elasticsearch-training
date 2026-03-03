# Lab 10: Query vs. Filter Contexts

## Goal
Execute structured searches in Kibana Dev Tools to understand the deep difference between scoring a document via `must` (Query Context) versus exact filtering via `filter` (Filter Context).

## Scenario
You need to search the `products` index created in Lab 6. Users are looking for the word "shoe", but they only want to see results that cost less than $100.

## Prerequisites
- Completion of Lab 6 (The `products` index must exist with sample data).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

### Part 0: Insert Sample Data
Before running queries, let's insert some sample products.
```json
POST /products/_bulk
{"index":{"_id":"1"}}
{"name": "Running Shoe", "category": "Footwear", "price": 90}
{"index":{"_id":"2"}}
{"name": "Walking Shoe", "category": "Footwear", "price": 120}
{"index":{"_id":"3"}}
{"name": "Winter Jacket", "category": "Apparel", "price": 150}
```

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

2. **Analyze the Results (Query Context):**
   - Look at the `_score` field in the response. Because the document matched the word "shoe" inside the `must` block, Elasticsearch invoked its BM25 scoring algorithm to calculate *how relevant* this match is compared to others, yielding a floating-point score!
   - Notice how the `filter` block simply acted as a binary gate (Yes/No if `< 100`). It restricted the result pool, but it **did not** contribute to or alter the relevance `_score`.

### Part 2: Pure Filter Context (Speed & Caching)
Sometimes you don't care about relevance ranking at all; you just want exact matches (e.g., retrieving a specific user ID or filtering by an exact status).

3. **Swap context to see the difference:**
   Move the `match` query down into the `filter` block alongside the price range.
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
   - Execute it again. Observe that the `_score` is now exactly `0.0`. 
   
**Why do this?** 
Because you traded relevance ranking for pure speed. Elasticsearch skips the expensive BM25 calculation entirely, simply returning matching documents in arbitrary order. Furthermore, Elasticsearch **automatically caches** the results of frequently used filters, making subsequent identical queries lightning fast!

---

---


---
[Previous Lab: Lab 9](../module3/lab9.md) | [Return to Module 4](module4.md) | [Next Lab: Lab 11](lab11.md)

# Lab 5: Simulating & Troubleshooting Cluster Issues

## Goal
Update a document field dynamically using a Painless script without having to pull the document out of Elasticsearch, modify it in application code, and send it back.

## Scenario
Inflation has hit! You need to increase the price of a specific product ("Running Shoe", ID 1) by a flat amount natively inside the cluster.

## Prerequisites
- Completion of Lab 11 (The `products` index must exist).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

1. **Verify Current Price**:
   ```json
   GET products/_doc/1
   ```
   *Note the `price` field value.*

2. **Execute the Update Script**:
   We use `ctx._source` to access the document's fields. We also use a parameterized variable `markup` rather than hardcoding the added value. This enables Elasticsearch to cache the compiled bytecode of the script!
   ```json
   POST products/_update/1
   {
     "script": {
       "source": "ctx._source.price += params.markup",
       "params": { "markup": 10 }
     }
   }
   ```

3. **Verify the Increment:**
   ```json
   GET products/_doc/1
   ```
   *The price should be 10 higher!*

---

---

---
[Previous Lab: Lab 4](lab4.md) | [Return to Module 2](module2.md) | [Next Lab: Lab 6](../module3/lab6.md)

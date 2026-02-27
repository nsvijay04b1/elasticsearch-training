# Lab 13: Using Painless Scripts

## Goal
Update a document field dynamically using a Painless script without having to pull the document out of Elasticsearch, modify it in application code, and send it back.

## Scenario
Inflation has hit! You need to increase the price of a specific product ("Running Shoe", ID 1) by a flat amount natively inside the cluster.

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
[Previous Lab: Lab 12](../module5/lab12.md) | [Return to Module 6](module6.md) | [Next Lab: Lab 14](lab14.md)

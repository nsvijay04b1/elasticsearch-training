# Lab 14: Using Painless Scripts

## Goal
Update a document field dynamically using a Painless script without having to pull the document out of Elasticsearch, modify it in application code, and send it back.

## Scenario
Inflation has hit! You need to increase the price of a specific product ("Running Shoe", ID 1) by a flat amount natively inside the cluster.

## Prerequisites
- Completion of Lab 6 (The `products` index must exist).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

### Part 0: Insert Target Document
Let's create the product we are going to modify via Painless.
```json
PUT /products/_doc/1
{
  "name": "Running Shoe",
  "category": "Footwear",
  "price": 90
}
```

### 1. Verify Current Price
```json
GET products/_doc/1
```

**Expected Output:**
```json
{
  "_index": "products",
  "_id": "1",
  "_source": {
    "name": "Running Shoe",
    "category": "Footwear",
    "price": 90
  }
}
```

### 2. Execute the Update Script
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

**Expected Output:**
```json
{
  "_index": "products",
  "_id": "1",
  "result": "updated",
  "_version": 2
}
```

### 3. Verify the Increment
```json
GET products/_doc/1
```

**Expected Output:**
```json
{
  "_source": {
    "name": "Running Shoe",
    "category": "Footwear",
    "price": 100
  }
}
```
*The price increased from 90 to 100!*

### 4. Conditional Painless Script
Apply a 20% discount, but ONLY if the current price is above $50. This demonstrates conditional logic inside Painless.
```json
POST products/_update/1
{
  "script": {
    "source": "if (ctx._source.price > params.threshold) { ctx._source.price = (int)(ctx._source.price * 0.8) }",
    "params": { "threshold": 50 }
  }
}
```

**Expected Output:**
```json
{ "result": "updated", "_version": 3 }
```

### 5. Verify the Conditional Update
```json
GET products/_doc/1
```

**Expected Output:**
```json
{
  "_source": {
    "name": "Running Shoe",
    "category": "Footwear",
    "price": 80
  }
}
```
*The price dropped from 100 to 80 (20% discount applied because 100 > 50).*

### 6. Painless Script in a Search Query (Script Fields)
You can also use Painless at search time to compute virtual fields on the fly:
```json
GET products/_search
{
  "query": { "match_all": {} },
  "script_fields": {
    "price_with_tax": {
      "script": {
        "source": "doc['price'].value * 1.15"
      }
    }
  }
}
```
*This adds a computed `price_with_tax` field (15% tax) to every result without modifying the stored data.*

---

[Previous Lab: Lab 13.2](../module5/lab13_2.md) | [Return to Module 6](module6.md) | [Next Lab: Lab 14.2](lab14_2.md)

# Lab 6: Indexing Data via Bulk API

## Goal
Learn how to use the high-throughput Bulk API endpoint to index multiple documents in a single HTTP request using `curl`.

## Scenario
Instead of sending 10,000 separate `curl` commands to insert your product catalog, you format them into a single file to bypass network latency and HTTP header overhead.

## Prerequisites
- Completion of Lab 4.
- Elasticsearch must be running securely.
- You must have your `elastic` superuser password handy.

## Instructions

### 1. Create a Bulk formatted file
The Bulk API requires a specific newline-delimited format (NDJSON), where an action instruction line is immediately followed by the document payload line.
```bash
cat <<EOF > requests.json
{ "index" : { "_index" : "products", "_id" : "1" } }
{ "name": "Running Shoe", "price": 95, "category": "Footwear", "in_stock": true }
{ "index" : { "_index" : "products", "_id" : "2" } }
{ "name": "Winter Hat", "price": 25, "category": "Accessories", "in_stock": true }
{ "index" : { "_index" : "products", "_id" : "3" } }
{ "name": "Leather Belt", "price": 45, "category": "Accessories", "in_stock": false }
{ "index" : { "_index" : "products", "_id" : "4" } }
{ "name": "Walking Shoe", "price": 120, "category": "Footwear", "in_stock": true }
{ "index" : { "_index" : "products", "_id" : "5" } }
{ "name": "Summer T-Shirt", "price": 30, "category": "Apparel", "in_stock": true }
{ "index" : { "_index" : "products", "_id" : "6" } }
{ "name": "Winter Jacket", "price": 150, "category": "Apparel", "in_stock": true }
{ "index" : { "_index" : "products", "_id" : "7" } }
{ "name": "Hiking Boots", "price": 180, "category": "Footwear", "in_stock": false }
{ "index" : { "_index" : "products", "_id" : "8" } }
{ "name": "Wool Scarf", "price": 35, "category": "Accessories", "in_stock": true }
EOF
```
*Note: Ensure there is a trailing newline at the end of the file!*

### 2. Execute the Bulk API Request
Pass the file to curl using the `--data-binary` flag.
```bash
curl -X POST "https://localhost:9200/_bulk" \
  -H 'Content-Type: application/json' \
  --cacert /etc/elasticsearch/certs/http_ca.crt \
  -u elastic \
  --data-binary @requests.json
```

**Expected Output (truncated):**
```json
{
  "took": 45,
  "errors": false,
  "items": [
    { "index": { "_index": "products", "_id": "1", "result": "created", "status": 201 } },
    { "index": { "_index": "products", "_id": "2", "result": "created", "status": 201 } },
    ...
  ]
}
```
*Key check: `"errors": false` means every document was indexed successfully.*

### 3. Verify Insertion
```bash
curl -X GET "https://localhost:9200/products/_count" \
  --cacert /etc/elasticsearch/certs/http_ca.crt \
  -u elastic
```

**Expected Output:**
```json
{
  "count": 8,
  "_shards": { "total": 1, "successful": 1, "skipped": 0, "failed": 0 }
}
```

### 4. Verify a Single Document
```bash
curl -X GET "https://localhost:9200/products/_doc/1" \
  --cacert /etc/elasticsearch/certs/http_ca.crt \
  -u elastic | jq .
```

**Expected Output:**
```json
{
  "_index": "products",
  "_id": "1",
  "_source": {
    "name": "Running Shoe",
    "price": 95,
    "category": "Footwear",
    "in_stock": true
  }
}
```

---

[Previous Lab: Lab 5](../module2/lab5.md) | [Return to Module 3](module3.md) | [Next Lab: Lab 7](lab7.md)

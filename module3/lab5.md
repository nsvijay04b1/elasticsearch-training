# Lab 5: Indexing Data via Bulk API

## Goal
Learn how to use the high-throughput Bulk API endpoint to index multiple documents in a single HTTP request using `curl`.

## Scenario
Instead of sending 10,000 separate `curl` commands to insert your product catalog, you format them into a single file to bypass network latency and HTTP header overhead.

## Prerequisites
- Completion of Lab 4.
- Elasticsearch must be running securely.
- You must have your `elastic` superuser password handy.

## Instructions

1. **Create a Bulk formatted file:**
   The Bulk API requires a specific newline-delimited format (NDJSON), where an action instruction line is immediately followed by the document payload line.
   ```bash
   cat <<EOF > requests.json
   { "index" : { "_index" : "products", "_id" : "1" } }
   { "name": "Running Shoe", "price": 95, "category": "Footwear" }
   { "index" : { "_index" : "products", "_id" : "2" } }
   { "name": "Winter Hat", "price": 25, "category": "Accessories" }
   { "index" : { "_index" : "products", "_id" : "3" } }
   { "name": "Leather Belt", "price": 45, "category": "Accessories" }
   EOF
   ```
   *Note: Ensure there is a trailing newline at the end of the file!*

2. **Execute the Bulk API Request:**
   Pass the file to curl using the `--data-binary` or `@` flag.
   ```bash
   curl -X POST "https://localhost:9200/_bulk" \
     -H 'Content-Type: application/json' \
     --cacert /etc/elasticsearch/certs/http_ca.crt \
     -u elastic \
     --data-binary @requests.json
   ```

3. **Verify Insertion:**
   *(You will be prompted for your password)*
   ```bash
   curl -X GET "https://localhost:9200/products/_count" \
     --cacert /etc/elasticsearch/certs/http_ca.crt \
     -u elastic
   ```
   *The `"count"` field should reflect the number of documents submitted.*

---
[Previous Lab: Lab 4](../module2/lab4.md) | [Return to Module 3](module3.md) | [Next Lab: Lab 6](lab6.md)

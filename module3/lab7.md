# Lab 7: Explicit Mappings & Ingest Pipelines

## Goal
Use Kibana Dev Tools to define an explicit mapping (preventing Mapping Explosions) and create an ingest pipeline to add timestamps to incoming data.

## Scenario
Your application sends sparse log data that doesn't include a timestamp. You need Elasticsearch to append the exact time the log was received. Additionally, you want to strictly control the mapping so that the `status` field is only ever treated as a `keyword` for exact filtering, and `message` as `text` for full-text search.

## Instructions

*(Note: We will execute these commands directly in the Kibana Dev Tools Console. Navigate to **Management -> Dev Tools** in Kibana).*

1. **Create an Ingest Pipeline:**
   This pipeline uses the `set` processor to add a field called `ingest_time`.
   ```json
   PUT _ingest/pipeline/my_pipeline
   {
     "description": "Add timestamp",
     "processors": [
       {
         "set": { "field": "ingest_time", "value": "{{_ingest.timestamp}}" }
       }
     ]
   }
   ```

2. **Create an index with an Explicit Mapping:**
   We enforce that `status` cannot be tokenized.
   ```json
   PUT my_logs
   {
     "mappings": {
       "properties": {
         "status": { "type": "keyword" },
         "message": { "type": "text" }
       }
     }
   }
   ```

3. **Index a document using the new pipeline:**
   Note the `?pipeline=my_pipeline` parameter.
   ```json
   POST my_logs/_doc/1?pipeline=my_pipeline
   {
     "status": "ERROR",
     "message": "Failed to connect to the database securely."
   }
   ```

4. **Retrieve the document to verify the injected timestamp:**
   ```json
   GET my_logs/_doc/1
   ```
   *You should see the `ingest_time` field automatically populated!*

---
[Previous Lab: Lab 6](lab6.md) | [Return to Module 3](module3.md) | [Next Lab: Lab 8](../module4/lab8.md)

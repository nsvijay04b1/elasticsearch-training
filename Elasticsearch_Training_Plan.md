# Elasticsearch 2-Day Expert Training Plan

This document provides a comprehensive 2-day, 8-hours-per-day training plan to cover 6 Elasticsearch modules. It includes an hour-by-hour breakdown, theory topics, and hands-on lab instructions tailored for students using Ubuntu machines.

---

## **Day 1: Foundations, Setup, and Data Ingestion**
*(Covers Module 1, Module 2, and Module 3)*

### **Hour 1: Core Concepts & Search vs. Database Mindset**
**Theory to Cover (Module 1):**
* What Problem Elasticsearch Solves: Relational DBs vs. Search Engines, why `LIKE` queries fail at scale.
* Lucene & Inverted Index Internals: Tokenization, segment storage, term dictionary, and posting lists.
* Core Data Model: Documents, Fields, Indices, and Mappings (Text vs. Keyword deep difference).

**Lab 1: Exploring JSON and REST APIs on Ubuntu**
* **Goal:** Verify Ubuntu environment, practice basic REST interactions.
* **Instructions:**
  ```bash
  # Open terminal on your Ubuntu machine
  # Verify curl is installed 
  curl --version
  
  # Create a sample JSON file to represent a document
  echo '{"title": "Introduction to Elasticsearch", "author": "Trainer"}' > doc1.json
  
  # View the document
  cat doc1.json
  ```

### **Hour 2: Distributed Architecture & Execution Flow**
**Theory to Cover (Module 1):**
* Distributed Architecture: Node Roles (Master, Data, Ingest, Coordinating).
* Cluster State & Shard Allocation.
* Primary vs Replica Mechanics (Write Operations).
* Search Execution Flow: Scatter-Gather phase.
* Enterprise Case Study: E-Commerce architecture.

**Lab 2: Architecture Whiteboarding**
* **Goal:** Group exercise to architect a 3-master, 6-data node setup. 
* *(No CLI execution required for this lab. Focus on conceptual design and shard distribution diagrams).*

### **Hour 3: Installation & Development vs Production Setup**
**Theory to Cover (Module 2):**
* Development vs Production environments (Single Node vs Multi-node).
* Bootstrap Process and `elasticsearch.yml` settings (`discovery.seed_hosts`, `cluster.initial_master_nodes`).

**Lab 3: Installing Elasticsearch & Kibana on Ubuntu**
* **Goal:** Install and start a single-node Elasticsearch cluster and Kibana.
* **Instructions:**
  ```bash
  # 1. Import the Elastic PGP Key
  wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
  
  # 2. Install apt-transport-https and add the repository
  sudo apt-get install apt-transport-https
  echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
  
  # 3. Install Elasticsearch & Kibana
  sudo apt-get update && sudo apt-get install elasticsearch kibana
  
  # 4. Start Elasticsearch Service (Note the generated superuser password!)
  sudo systemctl start elasticsearch.service
  
  # 5. Verify the installation
  curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic https://localhost:9200
  ```

### **Hour 4: Security, High Availability, and Upgrades**
**Theory to Cover (Module 2):**
* Security Architecture: Authentication, RBAC, TLS Encryption.
* High Availability: Replica recovery, Split-Brain prevention, Quorum logic.
* Cluster Health States (Green, Yellow, Red).
* Rolling Upgrade Strategy.

**Lab 4: Configuring Basic Security & Kibana Setup**
* **Goal:** Reset default passwords and start Kibana.
* **Instructions:**
  ```bash
  # 1. Auto-generate new passwords (if needed)
  sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
  
  # 2. Start Kibana 
  sudo systemctl start kibana.service
  
  # 3. Generate Kibana enrollment token
  sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
  
  # 4. Open Kibana in the browser (http://localhost:5601) and use the token to set it up.
  ```

### **Hour 5: Indexing Internals & The Bulk API**
**Theory to Cover (Module 3):**
* Indexing Internals: Refresh cycles, memory buffers, and flushes.
* Segment Creation & Merge Process (Segments are immutable).
* Bulk API: Trade-offs between throughput and latency.

**Lab 5: Indexing Data via Bulk API**
* **Goal:** Use `curl` to perform bulk indexing.
* **Instructions:**
  ```bash
  # 1. Create a bulk request file (requests.json)
  cat <<EOF > requests.json
  { "index" : { "_index" : "products", "_id" : "1" } }
  { "name": "Running Shoe", "price": 95, "category": "Footwear" }
  { "index" : { "_index" : "products", "_id" : "2" } }
  { "name": "Winter Hat", "price": 25, "category": "Accessories" }
  EOF
  
  # 2. Execute Bulk API
  curl -X POST "https://localhost:9200/_bulk" -H 'Content-Type: application/json' --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic -d @requests.json
  ```

### **Hour 6: Data Ingestion with Logstash & Beats**
**Theory to Cover (Module 3):**
* Logstash Architecture: Input, Filter, Output pipelines (ETL).
* Beats Architecture: Filebeat, Metricbeat, Packetbeat (Lightweight Shippers).

**Lab 6: Installing and Configuring Filebeat**
* **Goal:** Ingest Ubuntu system logs into Elasticsearch via Filebeat.
* **Instructions:**
  ```bash
  # 1. Install Filebeat
  sudo apt-get install filebeat
  
  # 2. Enable the system module (captures local syslog)
  sudo filebeat modules enable system
  
  # 3. Setup Filebeat assets (dashboards, pipelines)
  sudo filebeat setup -e \
    -E output.elasticsearch.hosts=['https://localhost:9200'] \
    -E output.elasticsearch.username=elastic \
    -E output.elasticsearch.password='<YOUR_PASSWORD>' \
    -E output.elasticsearch.ssl.certificate_authorities=['/etc/elasticsearch/certs/http_ca.crt']
  
  # 4. Start Filebeat
  sudo systemctl start filebeat
  ```

### **Hour 7: Ingest Pipelines & Mapping Strategy**
**Theory to Cover (Module 3):**
* Ingest Pipelines: Processors (Grok, GeoIP, Date).
* Mapping Strategy: Dynamic vs. Explicit Mapping. Mapping Explosions.
* Fielddata & Doc Values.

**Lab 7: Creating an Explicit Mapping & Ingest Pipeline**
* **Goal:** Use Kibana Dev Tools to define a mapping and a pipeline.
* **Instructions (Execute in Kibana Dev Tools):**
  ```json
  // 1. Create a Pipeline
  PUT _ingest/pipeline/my_pipeline
  {
    "description": "Add timestamp",
    "processors": [
      {
        "set": { "field": "ingest_time", "value": "{{_ingest.timestamp}}" }
      }
    ]
  }
  
  // 2. Create index with mapping
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

### **Hour 8: Day 1 Review & Q/A**
* Review Topics: Nodes, Shards, Security, Bulk API, Filebeat.
* Discuss Trainer Interview Questions (e.g., "Explain shard vs replica clearly", "What happens internally during indexing?").
* Assist students with any broken local environments.

---

## **Day 2: Search, Data Lifecycle, and Advanced APIs**
*(Covers Module 4, Module 5, and Module 6)*

### **Hour 1: Query DSL & Search Internals**
**Theory to Cover (Module 4):**
* Query Context vs Filter Context (Scoring vs No Scoring).
* Full-Text Search Internals: Analyzers, Tokenizers, Stemming, Synonyms.
* Bool Query Architecture (`must`, `should`, `filter`, `must_not`).

**Lab 8: Query Context vs. Filter Context**
* **Goal:** Execute searches demonstrating BM25 scoring vs exact filtering.
* **Instructions (Kibana Dev Tools):**
  ```json
  // Execute a bool query combining search and filter
  GET products/_search
  {
    "query": {
      "bool": {
        "must": { "match": { "name": "shoe" } },
        "filter": { "range": { "price": { "lt": 100 } } }
      }
    }
  }
  ```

### **Hour 2: Relevance Scoring & Aggregations**
**Theory to Cover (Module 4):**
* BM25 Ranking Explained (TF, IDF, Field Length Normalization).
* Aggregations Framework: Bucket vs Metrics Aggregations.
* ES|QL vs EQL vs SQL overviews.

**Lab 9: Building Aggregations**
* **Goal:** Create metrics (average price) nested inside buckets (category).
* **Instructions (Kibana Dev Tools):**
  ```json
  GET products/_search
  {
    "size": 0,
    "aggs": {
      "categories": {
        "terms": { "field": "category.keyword" },
        "aggs": {
          "avg_price": { "avg": { "field": "price" } }
        }
      }
    }
  }
  ```

### **Hour 3: Search Optimization Techniques**
**Theory to Cover (Module 4):**
* Using filter context for caching.
* Avoiding heavy scripts.
* Proper shard sizing & avoiding Doc Values misuse.

**Lab 10: Analyzing Search Performance**
* **Goal:** Use the Profile API to inspect query execution times.
* **Instructions:**
  ```json
  GET products/_search
  {
    "profile": true,
    "query": { "match": { "name": "shoe" } }
  }
  ```
  *(Review the breakdown of Lucene query timing in the response).*

### **Hour 4: Data Lifecycle Management (ILM)**
**Theory to Cover (Module 5):**
* Index Lifecycle Management (ILM) Deep Dive: Hot, Warm, Cold, Frozen, Delete phases.
* Data Tiers architecture.

**Lab 11: Creating an ILM Policy**
* **Goal:** Automate index rollover using ILM.
* **Instructions (Kibana Dev Tools):**
  ```json
  PUT _ilm/policy/my_policy
  {
    "policy": {
      "phases": {
        "hot": {
          "actions": { "rollover": { "max_age": "1d", "max_size": "50gb" } }
        },
        "delete": {
          "min_age": "30d",
          "actions": { "delete": {} }
        }
      }
    }
  }
  ```

### **Hour 5: Storage Optimization, Snapshots & Restores**
**Theory to Cover (Module 5):**
* Downsampling & Rollups.
* Snapshot & Restore Internals (Incremental limits, Repository types).
* Segment Merging and Compression. Heap Sizing best practices.

**Lab 12: Configuring a Local Snapshot Repository**
* **Goal:** Create a local filesystem repository on Ubuntu and take a snapshot.
* **Instructions:**
  ```bash
  # 1. Modify elasticsearch.yml to register backup path
  echo 'path.repo: ["/var/backups/es_repo"]' | sudo tee -a /etc/elasticsearch/elasticsearch.yml
  sudo mkdir -p /var/backups/es_repo
  sudo chown -R elasticsearch:elasticsearch /var/backups/es_repo
  sudo systemctl restart elasticsearch
  ```
  **(In Kibana Dev Tools):**
  ```json
  PUT _snapshot/my_fs_backup
  {
    "type": "fs",
    "settings": { "location": "/var/backups/es_repo" }
  }
  
  PUT _snapshot/my_fs_backup/snapshot_1?wait_for_completion=true
  ```

### **Hour 6: APIs, Client Architecture, & Painless Scripting**
**Theory to Cover (Module 6):**
* REST API Design Philosophy.
* Official Clients Architecture (Java, Python, JS).
* Painless Scripting Internals (Sandboxed execution, update docs, custom scoring).

**Lab 13: Using Painless Scripts**
* **Goal:** Update a document field dynamically using a Painless script.
* **Instructions (Kibana Dev Tools):**
  ```json
  POST products/_update/1
  {
    "script": {
      "source": "ctx._source.price += params.markup",
      "params": { "markup": 10 }
    }
  }
  ```

### **Hour 7: Plugin Ecosystem, Monitoring, and Troubleshooting**
**Theory to Cover (Module 6):**
* Plugin Ecosystem (Analysis plugins, Repository plugins).
* Monitoring Cluster Health, Unassigned Shards.
* Troubleshooting High Heap Usage and Slow Queries.
* Enterprise Deployment Blueprint.

**Lab 14: Simulating and Troubleshooting a Yellow Cluster**
* **Goal:** Understand why a cluster turns yellow.
* **Instructions:**
  ```json
  // Request cluster health
  GET _cluster/health
  
  // Create an index with 1 replica on a single-node cluster
  PUT /troubleshoot_index
  { "settings": { "number_of_replicas": 1 } }
  
  // Explain why shards are unassigned
  GET _cluster/allocation/explain
  ```

### **Hour 8: Final Review & Interview Simulations**
* Review Topics: Query DSL, BM25, ILM, Snapshots, Painless, Troubleshooting.
* Trainer Interview Simulation Questions (e.g., "How does BM25 work conceptually?", "Design a production ES architecture for enterprise").
* Distribute completion certificates / wrap up the 2-day course.

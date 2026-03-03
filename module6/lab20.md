# Lab 20: REST API Deep Dive & Python Client

## Goal
Master the essential Elasticsearch REST APIs beyond basic CRUD, and connect to the cluster programmatically using the official Python client.

## Scenario
You are building an operations dashboard. You need to programmatically query cluster health, node statistics, and index metadata. Additionally, your data engineering team uses Python and needs a working example of indexing and searching via the official `elasticsearch-py` client library.

## Prerequisites
- Completion of Lab 6 (The `products` index must exist with sample data).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.
- Python 3 must be installed on your Ubuntu VM.

## Instructions

---

### Part 1: Essential REST APIs (Kibana Dev Tools)

*(Navigate to **Management -> Dev Tools** in Kibana).*

#### 1. Cluster Health API
```json
GET _cluster/health
```

**Expected Output:**
```json
{
  "cluster_name": "elasticsearch",
  "status": "yellow",
  "number_of_nodes": 1,
  "number_of_data_nodes": 1,
  "active_primary_shards": 12,
  "active_shards": 12,
  "unassigned_shards": 5
}
```

#### 2. Node Information API
```json
GET _nodes/stats/jvm,os
```

**Expected Output (key sections):**
```json
{
  "nodes": {
    "abc123...": {
      "name": "your-node-name",
      "jvm": {
        "mem": {
          "heap_used_percent": 42,
          "heap_max_in_bytes": 1073741824
        }
      },
      "os": {
        "cpu": { "percent": 8 },
        "mem": { "total_in_bytes": 4294967296, "used_percent": 75 }
      }
    }
  }
}
```

#### 3. Cat APIs (Human-Readable Tables)
```text
GET _cat/indices?v&h=index,docs.count,store.size&s=docs.count:desc
```

**Expected Output:**
```text
index            docs.count store.size
products                  8      12.5kb
my_logs                   1       4.2kb
server_metrics            9       8.1kb
```

#### 4. Index Stats API
```json
GET products/_stats/docs,store
```

**Expected Output:**
```json
{
  "_all": {
    "primaries": {
      "docs": { "count": 8, "deleted": 0 },
      "store": { "size_in_bytes": 12800 }
    }
  }
}
```

#### 5. Cluster Settings API (View Dynamic Settings)
```json
GET _cluster/settings?include_defaults=true&flat_settings=true&filter_path=defaults.cluster.routing*
```

---

### Part 2: Python Elasticsearch Client

#### 1. Install the Official Client
```bash
pip3 install elasticsearch
```

#### 2. Create a Python Script
```bash
cat <<'PYEOF' > es_demo.py
from elasticsearch import Elasticsearch

# Connect to Elasticsearch (adjust password and cert path)
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "YOUR_PASSWORD_HERE"),
    ca_certs="/etc/elasticsearch/certs/http_ca.crt"
)

# 1. Check cluster health
health = es.cluster.health()
print(f"Cluster Status: {health['status']}")
print(f"Number of Nodes: {health['number_of_nodes']}")

# 2. Index a new document
doc = {
    "name": "Python SDK Sneaker",
    "price": 110,
    "category": "Footwear",
    "in_stock": True
}
resp = es.index(index="products", id="100", document=doc)
print(f"Indexed document: {resp['result']}")

# 3. Search for all Footwear
results = es.search(
    index="products",
    query={"match": {"category": "Footwear"}}
)
print(f"Found {results['hits']['total']['value']} Footwear products:")
for hit in results['hits']['hits']:
    src = hit['_source']
    print(f"  - {src['name']} (${src['price']})")

# 4. Delete the test document
es.delete(index="products", id="100")
print("Cleaned up test document.")
PYEOF
```

#### 3. Run the Script
```bash
python3 es_demo.py
```

**Expected Output:**
```text
Cluster Status: yellow
Number of Nodes: 1
Indexed document: created
Found 4 Footwear products:
  - Running Shoe ($95)
  - Walking Shoe ($120)
  - Hiking Boots ($180)
  - Python SDK Sneaker ($110)
Cleaned up test document.
```

---

[Previous Lab: Lab 19](lab19.md) | [Return to Module 6](module6.md) | [Next Lab: Lab 21](lab21.md)

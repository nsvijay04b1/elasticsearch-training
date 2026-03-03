# Lab 21: Installing and Managing Plugins

## Goal
Install an Elasticsearch plugin, verify it is loaded, and use it in practice. Plugins extend Elasticsearch with custom analyzers, security features, and data processing capabilities.

## Scenario
Your team needs to index multilingual documents containing Chinese, Japanese, and Korean (CJK) text. The default analyzer doesn't handle CJK tokenization well, so you install the `analysis-icu` plugin which provides the ICU Analyzer for proper Unicode text analysis.

## Prerequisites
- You must have `sudo` access on your Ubuntu VM.
- Elasticsearch must be running.
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

---

## Part 1: Installing a Plugin

### 1. List Currently Installed Plugins
```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-plugin list
```

**Expected Output:**
```text
(empty — no plugins installed by default)
```

### 2. Install the ICU Analysis Plugin
```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-icu
```

**Expected Output:**
```text
-> Installing analysis-icu
-> Downloading analysis-icu from elastic
-> Installed analysis-icu
-> Please restart Elasticsearch to activate any plugins installed
```
* **Why?** Plugins extend the core functionality of Elasticsearch. While the "Standard" analyzer is great for English, specialized plugins like `analysis-icu` are required for high-quality multi-lingual search across different character sets like CJK.

### 3. Restart Elasticsearch
```bash
sudo systemctl restart elasticsearch.service
```
*Wait ~30 seconds for the node to come back online.*

### 4. Verify the Plugin is Loaded
```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-plugin list
```

**Expected Output:**
```text
analysis-icu
```

You can also verify from Kibana Dev Tools:
```json
GET _cat/plugins?v
```

**Expected Output:**
```text
name       component     version
ubuntu-vm  analysis-icu  8.10.4
```

---

## Part 2: Using the ICU Analyzer

### 1. Test the Default Analyzer vs ICU Analyzer

**Default analyzer on CJK text:**
```json
POST _analyze
{
  "analyzer": "standard",
  "text": "東京は日本の首都です"
}
```

**Expected Output:** Each character is treated as a separate token (not ideal):
```json
{ "tokens": [
  { "token": "東", "position": 0 },
  { "token": "京", "position": 1 },
  { "token": "は", "position": 2 },
  ...
]}
```

**ICU analyzer on the same text:**
```json
POST _analyze
{
  "analyzer": "icu_analyzer",
  "text": "東京は日本の首都です"
}
```

**Expected Output:** Properly tokenized into meaningful words:
```json
{ "tokens": [
  { "token": "東京", "position": 0 },
  { "token": "日本", "position": 1 },
  { "token": "首都", "position": 2 }
]}
```

### 2. Create an Index Using the ICU Analyzer
```json
PUT multilingual_docs
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_icu": {
          "type": "icu_analyzer"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": { "type": "text", "analyzer": "my_icu" },
      "content": { "type": "text", "analyzer": "my_icu" }
    }
  }
}
```

### 3. Index a Multilingual Document
```json
POST multilingual_docs/_doc/1
{
  "title": "東京タワーの歴史",
  "content": "東京タワーは1958年に完成した電波塔です"
}
```

### 4. Search for It
```json
GET multilingual_docs/_search
{
  "query": { "match": { "content": "東京" } }
}
```

**Expected Output:**
```json
{
  "hits": { "total": { "value": 1 },
    "hits": [ { "_source": { "title": "東京タワーの歴史" } } ]
  }
}
```

---

## Part 3: Removing a Plugin

If you no longer need a plugin:
```bash
sudo /usr/share/elasticsearch/bin/elasticsearch-plugin remove analysis-icu
sudo systemctl restart elasticsearch.service
```

---

### Common Elasticsearch Plugins

| Plugin | Purpose |
|--------|---------|
| `analysis-icu` | Unicode text analysis for CJK and multilingual content |
| `analysis-phonetic` | Phonetic matching (sounds-like search) |
| `ingest-attachment` | Extract text from PDF, Word, Excel attachments |
| `repository-s3` | Store snapshots in Amazon S3 |
| `repository-gcs` | Store snapshots in Google Cloud Storage |
| `repository-azure` | Store snapshots in Azure Blob Storage |

---

[Previous Lab: Lab 20](lab20.md) | [Return to Module 6](module6.md)

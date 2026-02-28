# Lab 8: Installing and Configuring Logstash

## Goal
Install Logstash on your Ubuntu VM and build a complete data pipeline that reads input, transforms it, and sends it to Elasticsearch.

## Scenario
While Beats (like Filebeat) are lightweight shippers that send raw data, **Logstash** is the heavy-duty data processing engine of the ELK stack. It can parse, transform, enrich, and route data from virtually any source to any destination. In this lab, you will install Logstash, build a pipeline from scratch, and watch data flow into Elasticsearch in real time.

## Prerequisites
- Completion of Lab 4 (Elasticsearch and Kibana must be running).
- You must have your `elastic` superuser password handy.
- You must have `sudo` privileges on your Ubuntu VM.

---

## Part 1: Installing Logstash

### 1. Install Logstash via APT
Since you already added the Elastic APT repository in Lab 3, Logstash can be installed directly:
```bash
sudo apt-get update && sudo apt-get install -y logstash
```

### 2. Verify Installation
```bash
sudo /usr/share/logstash/bin/logstash --version
```

**Expected Output:**
```text
logstash 8.10.4
```

### 3. Understand the Logstash Architecture
Logstash pipelines have 3 stages:

```
┌──────────┐      ┌──────────────┐      ┌──────────────┐
│  INPUT   │ ───► │   FILTER     │ ───► │    OUTPUT     │
│ (source) │      │ (transform)  │      │ (destination) │
└──────────┘      └──────────────┘      └──────────────┘
 stdin, file,      grok, mutate,         elasticsearch,
 beats, kafka      date, geoip           stdout, file
```

---

## Part 2: Your First Pipeline (stdin → stdout)

### 1. Create a Simple Test Pipeline
This pipeline reads from your terminal and prints the processed output back to you.
```bash
cat <<'EOF' | sudo tee /etc/logstash/conf.d/test-pipeline.conf
input {
  stdin {}
}

filter {
  mutate {
    add_field => { "environment" => "training" }
  }
}

output {
  stdout {
    codec => rubydebug
  }
}
EOF
```

### 2. Run Logstash with the Test Pipeline
```bash
sudo /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/test-pipeline.conf
```
*Wait ~30 seconds for Logstash to initialize. You will see `Pipeline is running` in the logs.*

### 3. Type a Test Message
Once Logstash is ready, type the following and press Enter:
```
Hello from Logstash training!
```

**Expected Output:**
```ruby
{
       "message" => "Hello from Logstash training!",
    "@timestamp" => 2024-10-15T14:30:00.000Z,
      "@version" => "1",
   "environment" => "training",
          "host" => { "hostname" => "ubuntu-vm" }
}
```
*Notice how the `mutate` filter automatically added the `environment: training` field!*

Press `Ctrl+C` to stop Logstash.

---

## Part 3: Production Pipeline (CSV file → Elasticsearch)

Now let's build a real pipeline that reads a CSV file, parses it, and sends structured data to Elasticsearch.

### 1. Create a Sample CSV Data File
```bash
cat <<'EOF' | sudo tee /tmp/employees.csv
id,name,department,salary
1,Alice Johnson,Engineering,95000
2,Bob Smith,Marketing,72000
3,Carol Williams,Engineering,105000
4,Dave Brown,Sales,68000
5,Eve Davis,Engineering,98000
EOF
```

### 2. Create the CSV Pipeline Configuration
```bash
cat <<'EOF' | sudo tee /etc/logstash/conf.d/csv-pipeline.conf
input {
  file {
    path => "/tmp/employees.csv"
    start_position => "beginning"
    sincedb_path => "/dev/null"
  }
}

filter {
  # Skip the header row
  if [message] =~ "^id," {
    drop {}
  }

  csv {
    separator => ","
    columns => ["employee_id", "name", "department", "salary"]
  }

  mutate {
    convert => { "salary" => "integer" }
    convert => { "employee_id" => "integer" }
    remove_field => ["message", "event", "log", "@version"]
  }
}

output {
  elasticsearch {
    hosts => ["https://localhost:9200"]
    index => "employees"
    user => "elastic"
    password => "YOUR_PASSWORD_HERE"
    ssl_certificate_authorities => "/etc/elasticsearch/certs/http_ca.crt"
  }

  stdout {
    codec => rubydebug
  }
}
EOF
```

> **Important:** Replace `YOUR_PASSWORD_HERE` with your actual `elastic` password from Lab 3.

### 3. Run the CSV Pipeline
```bash
sudo /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/csv-pipeline.conf
```

**Expected Terminal Output (for each row):**
```ruby
{
    "employee_id" => 1,
          "name" => "Alice Johnson",
    "department" => "Engineering",
        "salary" => 95000,
    "@timestamp" => 2024-10-15T14:35:00.000Z
}
```

Press `Ctrl+C` after all 5 records have been processed.

### 4. Verify Data in Elasticsearch (Kibana Dev Tools)
Navigate to **Management → Dev Tools** in Kibana and run:
```json
GET employees/_search
{
  "query": { "match_all": {} },
  "sort": [{ "employee_id": "asc" }]
}
```

**Expected Output:**
```json
{
  "hits": {
    "total": { "value": 5 },
    "hits": [
      { "_source": { "employee_id": 1, "name": "Alice Johnson", "department": "Engineering", "salary": 95000 } },
      { "_source": { "employee_id": 2, "name": "Bob Smith", "department": "Marketing", "salary": 72000 } },
      ...
    ]
  }
}
```

### 5. Query the Ingested Data
Find all engineers earning over $90,000:
```json
GET employees/_search
{
  "query": {
    "bool": {
      "must": { "match": { "department": "Engineering" } },
      "filter": { "range": { "salary": { "gte": 90000 } } }
    }
  }
}
```

**Expected Output:** 3 hits (Alice, Carol, Eve).

---

[Previous Lab: Lab 7](lab7.md) | [Return to Module 3](module3.md) | [Next Lab: Lab 9](lab9.md)

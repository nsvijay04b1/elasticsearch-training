# Lab 14: Querying with ES|QL, EQL, and SQL

## Goal
Execute queries using three alternative query languages beyond the standard Query DSL: ES|QL (pipe-based analytics), EQL (event sequences), and SQL (relational syntax).

## Scenario
Your team includes database administrators who think in SQL, security analysts who need event correlation via EQL, and data engineers who prefer pipeline-style analytics via ES|QL. You need to demonstrate all three approaches against the same dataset.

## Prerequisites
- Completion of Lab 6 (The `products` index must exist with sample data).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

### Part 1: ES|QL (Elasticsearch Query Language)

ES|QL uses a pipe (`|`) syntax similar to Unix shell or Splunk SPL. Data flows left to right through processing stages.

**ES|QL Pipe Model:**
```text
  FROM filebeat-*                    <- source index
  | WHERE process.name == "sshd"     <- filter rows
  | EVAL hour = DATE_TRUNC(1h, @timestamp)  <- compute field
  | STATS events = COUNT(*) BY hour  <- aggregate
  | SORT hour ASC                    <- sort
  | LIMIT 24                         <- cap output
```

#### Basics — FROM and LIMIT
FROM selects the source index (or data stream). LIMIT caps the rows returned. ES|QL always requires a LIMIT — default max is 10,000 rows.
```json
POST _query
{
  "query": "FROM products | WHERE category == \"Footwear\" | WHERE price > 100 | SORT price DESC"
}
```
**Expected Output:**
```text
# Expected: Walking Shoe (120) and Hiking Boots (180)
# Running Shoe (95) excluded because price <= 100
```

#### STATS BY — aggregate and group
STATS is ES|QL's aggregation command. Supports: COUNT, AVG, SUM, MIN, MAX, COUNT_DISTINCT. BY groups the results — equivalent to GROUP BY in SQL.
```json
POST _query
{
  "query": "FROM products | STATS count = COUNT(*), avg_price = AVG(price), max_price = MAX(price) BY category | SORT avg_price DESC"
}
```
**Expected Output:**
```json
{"values":[
  ["Footwear",   3, 131.67, 180],
  ["Apparel",    2, 90.0,   150],
  ["Accessories",3, 35.0,    45]
]}
```

#### EVAL and KEEP — compute new fields and select columns
EVAL creates computed columns (like a calculated field). CASE() is a conditional expression. KEEP selects only the columns you want in the output (like SELECT in SQL).
```json
POST _query
{
  "query": "FROM products | EVAL price_with_tax = price * 1.2, price_band = CASE(price < 50, \"budget\", price < 100, \"mid-range\", \"premium\") | WHERE in_stock == true | KEEP name, price, price_with_tax, price_band | SORT price DESC"
}
```
**Expected Output:**
```text
# Expected:
# name            price  price_with_tax  price_band
# Winter Jacket     150          180.0   premium
# Walking Shoe      120          144.0   premium
# Running Shoe       95          114.0   mid-range
# Summer T-Shirt     30           36.0   budget
# Wool Scarf         35           42.0   budget
```

#### LIKE and RLIKE — wildcard and regex matching
LIKE uses glob-style wildcards (* = any chars, ? = one char). RLIKE uses full Java regular expressions.
```json
POST _query
{
  "query": "FROM products | WHERE name LIKE \"*Shoe*\" | SORT price ASC"
}

POST _query
{
  "query": "FROM products | WHERE name RLIKE \".*Shoe.*\" | STATS total = COUNT(*), avg = AVG(price)"
}
```
**Expected Output:**
```text
# LIKE result: Running Shoe (95), Walking Shoe (120)
# RLIKE STATS: total=2, avg=107.5
```

#### Real data — query your live Filebeat logs with ES|QL
This runs against the 10,000+ real syslog events Filebeat collected from your VM. Change the time range in Kibana if needed: add `| WHERE @timestamp > NOW() - 1 day`
```json
POST _query
{
  "query": "FROM filebeat-* | WHERE process.name == \"sudo\" | STATS login_count = COUNT(*) BY host.name | SORT login_count DESC | LIMIT 10"
}

POST _query
{
  "query": "FROM filebeat-* | WHERE log.file.path LIKE \"*/auth*\" | STATS events = COUNT(*) BY process.name | SORT events DESC | LIMIT 10"
}
```
**Expected Output:**
```text
# Expected output (will vary on your VM):
# host.name      login_count
# elk-training   43

# process.name  events
# sshd           1200
# sudo            43
# systemd         8900
```

---

### Part 2: SQL (Structured Query Language)

Elasticsearch supports SQL via the `_sql` endpoint, bridging the gap for teams familiar with relational querying.

**1. Basic SQL query:**
```json
POST _sql?format=txt
{
  "query": "SELECT name, price, category FROM products WHERE price > 50 ORDER BY price DESC"
}
```

**Expected Output:**
```text
     name       |    price    |  category
----------------+-------------+-----------
Hiking Boots    |180          |Footwear
Winter Jacket   |150          |Footwear
Walking Shoe    |120          |Footwear
Running Shoe    |95           |Footwear
```

**2. SQL aggregation:**
```json
POST _sql?format=txt
{
  "query": "SELECT category, COUNT(*) AS total, AVG(price) AS avg_price FROM products GROUP BY category"
}
```

**Expected Output:**
```text
  category    |    total    |  avg_price
--------------+-------------+-----------
Accessories   |3            |35.0
Apparel       |2            |90.0
Footwear      |3            |131.67
```

---

### Part 3: EQL (Event Query Language)

EQL is designed for detecting sequences of events over time. It is primarily used in Security Information and Event Management (SIEM) use cases. Let's create some sample event data first.

**1. Insert sample security events:**
```json
POST /security_events/_bulk
{"index":{}}
{"event.category": "authentication", "event.action": "login_attempt", "user.name": "admin", "@timestamp": "2024-10-15T10:00:00Z", "event.outcome": "failure"}
{"index":{}}
{"event.category": "authentication", "event.action": "login_attempt", "user.name": "admin", "@timestamp": "2024-10-15T10:00:05Z", "event.outcome": "failure"}
{"index":{}}
{"event.category": "authentication", "event.action": "login_attempt", "user.name": "admin", "@timestamp": "2024-10-15T10:00:10Z", "event.outcome": "success"}
```

**2. Use EQL to detect a brute-force pattern (2 failures followed by 1 success):**
```json
GET /security_events/_eql/search
{
  "query": "sequence by user.name [authentication where event.outcome == \"failure\"] [authentication where event.outcome == \"failure\"] [authentication where event.outcome == \"success\"]"
}
```

**Expected Output:**
```json
{
  "hits": {
    "sequences": [
      {
        "events": [
          { "_source": { "user.name": "admin", "event.outcome": "failure" } },
          { "_source": { "user.name": "admin", "event.outcome": "failure" } },
          { "_source": { "user.name": "admin", "event.outcome": "success" } }
        ]
      }
    ]
  }
}
```
*EQL detected the brute-force login sequence: 2 failures followed by a success from the same user!*

---

[Previous Lab: Lab 13](lab13.md) | [Return to Module 4](module4.md) | [Next Lab: Lab 15](../module5/lab15.md)

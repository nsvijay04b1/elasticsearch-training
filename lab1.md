# Lab 1: Exploring JSON and REST APIs on Ubuntu

## Goal
Verify the Ubuntu environment is correctly set up, ensure `curl` and `jq` are working, and practice the basic REST interactions over HTTP needed to interface with Elasticsearch.

## Scenario
Before beginning interaction with a live cluster, you need to understand the basic document format (JSON) and how to submit data payload via terminal using standard HTTP verbs.

## Prerequisites
- You must be logged into your provided Ubuntu VM.
- Ensure you have a working internet connection.
- You must have administrative (`sudo`) privileges.

## Instructions

### 1. Install Required Tools
```bash
sudo apt-get update && sudo apt-get install -y curl jq
```

### 2. Verify `curl` is installed
```bash
curl --version
```

**Expected Output:**
```text
curl 7.81.0 (x86_64-pc-linux-gnu) libcurl/7.81.0 ...
Protocols: dict file ftp ftps ...
```

### 3. Create a sample JSON document
```bash
echo '{"title": "Introduction to Elasticsearch", "author": "Trainer", "year": 2024}' > doc1.json
```

### 4. Use `jq` to pretty-print JSON
`jq` is a lightweight command-line JSON processor installed in Step 1.
```bash
cat doc1.json | jq .
```

**Expected Output:**
```json
{
  "title": "Introduction to Elasticsearch",
  "author": "Trainer",
  "year": 2024
}
```

### 5. Practice HTTP Verbs with a Public Test API
Before touching Elasticsearch, let's practice the 4 core HTTP verbs against a free echo API.

**GET** — Retrieve data:
```bash
curl -s https://httpbin.org/get | jq .url
```
**Expected Output:** `"https://httpbin.org/get"`

**POST** — Send data:
```bash
curl -s -X POST https://httpbin.org/post -H 'Content-Type: application/json' -d '{"name":"test"}' | jq .json
```
**Expected Output:**
```json
{
  "name": "test"
}
```

**PUT** — Replace data:
```bash
curl -s -X PUT https://httpbin.org/put -H 'Content-Type: application/json' -d '{"name":"updated"}' | jq .json
```
**Expected Output:**
```json
{
  "name": "updated"
}
```

**DELETE** — Remove data:
```bash
curl -s -X DELETE https://httpbin.org/delete | jq .url
```
**Expected Output:** `"https://httpbin.org/delete"`

---

[Return to Module 1](module1.md) | [Next Lab: Lab 2](lab2.md)

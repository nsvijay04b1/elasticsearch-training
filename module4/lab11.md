# Lab 11: Analyzing Search Performance

## Goal
Use the Profile API to peek under the hood at Lucene's execution times, allowing you to troubleshoot slow queries.

## Scenario
A user complains that searches for "shoe" are suddenly taking a long time. You need to verify exactly how many milliseconds the internal Lucene token-matching took.

## Prerequisites
- Completion of Lab 6 (The `products` index must exist with sample data).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

*(Navigate to **Management -> Dev Tools** in Kibana).*

### 1. Verify Sample Data Exists
```json
GET products/_count
```

**Expected Output:**
```json
{ "count": 8 }
```
*If count is 0, go back to Lab 6 and re-run the Bulk API insertion.*

### 2. Execute a Query with Profiling Enabled
Adding `"profile": true` forces Elasticsearch to attach a detailed timing breakdown to the end of the JSON response.
```json
GET products/_search
{
  "profile": true,
  "query": { "match": { "name": "shoe" } }
}
```

### 3. Review the Profile Response
Look for the `"profile"` object at the bottom of the response.

**Expected Output (key sections):**
```json
{
  "hits": {
    "total": { "value": 2 },
    "hits": [
      { "_source": { "name": "Running Shoe", "price": 95 } },
      { "_source": { "name": "Walking Shoe", "price": 120 } }
    ]
  },
  "profile": {
    "shards": [
      {
        "searches": [
          {
            "query": [
              {
                "type": "TermQuery",
                "description": "name:shoe",
                "time_in_nanos": 123456,
                "breakdown": {
                  "score": 5432,
                  "build_scorer": 45678,
                  "match": 1234,
                  "create_weight": 67890
                }
              }
            ]
          }
        ]
      }
    ]
  }
}
```

**Key fields to analyze:**
- `time_in_nanos`: Total execution time for this query component (in nanoseconds).
- `breakdown.score`: Time spent calculating BM25 relevance scores.
- `breakdown.build_scorer`: Time building the internal scorer object.

### 4. Compare with a Filter Context (No Scoring)
```json
GET products/_search
{
  "profile": true,
  "query": {
    "bool": {
      "filter": { "term": { "category.keyword": "Footwear" } }
    }
  }
}
```
*Notice how `breakdown.score` is `0` because filter context skips relevance scoring entirely, making it faster.*

---

[Previous Lab: Lab 10](lab10.md) | [Return to Module 4](module4.md) | [Next Lab: Lab 11.2](lab11_2.md)

# Lab 10: Query vs. Filter Contexts

## Goal
Execute structured searches in Kibana Dev Tools to understand the deep difference between scoring a document via `must` (Query Context) versus exact filtering via `filter` (Filter Context).

## Scenario
You need to search the `products` index created in Lab 6. Users are looking for the word "shoe", but they only want to see results that cost less than $100.

## Prerequisites
- Completion of Lab 6 (The `products` index must exist with sample data).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

### Part 0: Insert Sample Data
Before running queries, let's insert some sample products.
```json
POST /products/_bulk
{"index":{"_id":"1"}}
{"name": "Running Shoe", "category": "Footwear", "price": 90}
{"index":{"_id":"2"}}
{"name": "Walking Shoe", "category": "Footwear", "price": 120}
{"index":{"_id":"3"}}
{"name": "Winter Jacket", "category": "Apparel", "price": 150}
```

*(Navigate to **Management -> Dev Tools** in Kibana).*

1. **Execute a Mixed Context Search:**
   ```json
   GET products/_search
   {
     "query": {
       "bool": {
         "must": { 
           "match": { "name": "shoe" } 
         },
         "filter": { 
           "range": { "price": { "lt": 100 } } 
         }
       }
     }
   }
   ```

2. **Analyze the Results (Query Context):**
   - Look at the `_score` field in the response. Because the document matched the word "shoe" inside the `must` block, Elasticsearch invoked its BM25 scoring algorithm to calculate *how relevant* this match is compared to others, yielding a floating-point score!
   - Notice how the `filter` block simply acted as a binary gate (Yes/No if `< 100`). It restricted the result pool, but it **did not** contribute to or alter the relevance `_score`.

### Part 2: Pure Filter Context (Speed & Caching)
Sometimes you don't care about relevance ranking at all; you just want exact matches (e.g., retrieving a specific user ID or filtering by an exact status).

3. **Swap context to see the difference:**
   Move the `match` query down into the `filter` block alongside the price range.
   ```json
   GET products/_search
   {
     "query": {
       "bool": {
         "filter": [
           { "match": { "name": "shoe" } },
           { "range": { "price": { "lt": 100 } } }
         ]
       }
     }
   }
   ```
   * **Why?** Moving the `match` query to the `filter` block tells Elasticsearch not to calculate scores. Use this when the order of results doesn't matter (e.g., finding all "ERROR" logs), as it is faster and allows the results to be cached in memory.

---

## Part 3: Text Analysis & Tokenizers
Before text can be searched, Elasticsearch's **Analyzer** must break it down into searchable tokens.

1. **Test the Standard Analyzer:**
   ```json
   POST _analyze
   {
     "analyzer": "standard",
     "text": "Elasticsearch is FAST!"
   }
   ```
   * **Why?** It shows you exactly how text is "shredded". The Standard analyzer lowercases text and removes punctuation.

2. **Test a Custom Analyzer (Edge N-Grams):**
   This is common for "search-as-you-type".
   ```json
   PUT /test_index
   {
     "settings": {
       "analysis": {
         "analyzer": {
           "autocomplete": {
             "tokenizer": "autocomplete_tokenizer",
             "filter": ["lowercase"]
           }
         },
         "tokenizer": {
           "autocomplete_tokenizer": {
             "type": "edge_ngram",
             "min_gram": 2,
             "max_gram": 10,
             "token_chars": ["letter", "digit"]
           }
         }
       }
     }
   }
   ```
   * **Why?** The `edge_ngram` tokenizer breaks words into prefixes (e.g., "Elastic" becomes "El", "Ela", "Elas"). This allows a search for "El" to instantly find "Elasticsearch".

---

## Part 4: Relevance Tuning (Boosting)
You can influence the BM25 algorithm by "boosting" specific fields that are more important.

1. **Search with Boosting:**
   ```json
   GET products/_search
   {
     "query": {
       "multi_match": {
         "query": "shoe",
         "fields": ["name^3", "description"]
       }
     }
   }
   ```
   * **Why?** The `^3` syntax gives the `name` field 3 times more weight than the `description`. Use this when a match in a title is more valuable to the user than a match in the body text.

---

[Previous Lab: Lab 9](../module3/lab9.md) | [Return to Module 4](module4.md) | [Next Lab: Lab 11](lab11.md)

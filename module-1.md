# Module 1: Introduction to Elasticsearch

## 1.1 What Problem Elasticsearch Solves
Relational databases are optimized for transactional consistency (ACID), structured queries, and row-based storage. They use B-tree indexes which are inefficient for unstructured full-text searches across large datasets. `LIKE '%shoe%'` queries force database scans. 

Elasticsearch is optimized for text searches, relevance ranking, large data volumes, and horizontal scaling. It uses an inverted index.

## 1.2 Lucene & Inverted Index Internals
Lucene is the core indexing engine. It tokenizes text, creates inverted indexes, stores segments, and scores relevance. An inverted index works by mapping terms (from a Term Dictionary) to Posting Lists of document IDs.

```mermaid
graph TD
    subgraph "Documents"
        Doc1("Doc1: 'red shoe'")
        Doc2("Doc2: 'blue shoe'")
        Doc3("Doc3: 'red hat'")
    end

    subgraph "Inverted Index"
        red["red"] --> Doc1
        red --> Doc3
        blue["blue"] --> Doc2
        shoe["shoe"] --> Doc1
        shoe --> Doc2
        hat["hat"] --> Doc3
    end
```

## 1.3 Core Data Model
- **Document** = JSON object
- **Field** = Key-value pair
- **Index** = Logical grouping
- **Mapping** = Defines data types

**Text vs Keyword Types**
Use `text` for full-text search (analyzed), and `keyword` for exact match filtering and aggregations (not analyzed).

## 1.4 Distributed Architecture
- **Master**: Manages cluster state
- **Data**: Stores shards
- **Ingest**: Preprocess data
- **Coordinating**: Routes requests

Master nodes update the cluster state and allocate shards. Writes go to the primary shard, and replicas synchronize afterwards.

```mermaid
graph TD
    Client((Client)) --> PrimaryShard[Primary Shard]
    PrimaryShard -- Syncs Data --> ReplicaShard[Replica Shard]
```

## 1.5 Search Execution Flow
The Coordinating Node scatters the request across relevant shards (where local execution happens), gathers the local results, merges them, and returns them to the client.

```mermaid
graph TD
    Client((Client)) -->|Query| CoordNode[Coordinating Node]
    
    subgraph "Scatter Phase"
        CoordNode --> Shard1[Shard 1]
        CoordNode --> Shard2[Shard 2]
    end
    
    subgraph "Local Execution"
        Shard1 --> LocalExec1(Local Execution)
        Shard2 --> LocalExec2(Local Execution)
    end
    
    subgraph "Gather Phase"
        LocalExec1 --> |Top Results| CoordNode
        LocalExec2 --> |Top Results| CoordNode
    end
    
    CoordNode --> |Merge & Return| Client
```

## 1.6 Enterprise Case Study – E-Commerce

```mermaid
graph TD
    LB[Load Balancer] -->|Routes Traffic| Master1[Master Node 1]
    LB -->|Routes Traffic| Master2[Master Node 2]
    LB -->|Routes Traffic| Master3[Master Node 3]

    Master1 -.-> DataNodes
    Master2 -.-> DataNodes
    Master3 -.-> DataNodes

    subgraph DataNodes[6 Data Nodes]
        D1[Data Node 1]
        D2[Data Node 2]
        D3[Data Node 3]
        D4[Data Node 4]
        D5[Data Node 5]
        D6[Data Node 6]
    end

    DataNodes --> |Index 6 shards + 1 replica| ProductsIndex[(products_index)]
```

---

## Assigments
- [Proceed to Lab 1: JSON & REST API Basics](lab-1.md)
- [Proceed to Lab 2: Architecture Whiteboarding](lab-2.md)

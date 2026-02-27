# Lab 2: Architecture Whiteboarding

## Goal
Group exercise to conceptually architect a production-grade 3-master, 6-data node setup, visualizing shard distribution and node roles.

## Scenario
You've been tasked with designing the Elasticsearch architecture for a major E-Commerce platform that expects millions of searches daily. Before hitting the keyboard, the team must agree on the cluster footprint to ensure split-brain prevention and high availability.

## Instructions

*(Note: There is no Command-Line execution for this lab. This is a whiteboard or paper-driven exercise for maximum comprehension of distributed fundamentals).*

1. **Draw the Load Balancer / Coordinating Tier.**
   Explain how the external traffic routes into the cluster.

2. **Diagram the Master Nodes.**
   - Include precisely 3 Master Nodes.
   - Question for the group: *What is the Quorum required to prevent a split-brain in this setup?*

3. **Diagram the Data Nodes.**
   - Draw 6 Data Nodes.
   - Allocate an index (e.g., `products_index`) with 6 Primary Shards and 1 Replica.
   - **Crucial step**: Enforce the rule that a Primary Shard and its corresponding Replica can *never* exist on the same Data Node.

---
[Return to Module 1](module-1.md)

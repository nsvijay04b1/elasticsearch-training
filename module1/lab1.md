# Lab 1: Exploring JSON and REST APIs on Ubuntu

## Goal
Verify the Ubuntu environment is correctly set up, ensure `curl` is working, and practice the basic REST interactions over HTTP needed to interface with Elasticsearch.

## Scenario
Before beginning interaction with a live cluster, you need to understand the basic document format (JSON) and how to submit data payload via terminal using standard HTTP verbs.

## Prerequisites
- You must be logged into your provided Ubuntu VM.
- Ensure you have a working internet connection.
- You must have administrative (`sudo`) privileges.

## Instructions

1. **Open your Ubuntu Terminal.**
2. **Verify `curl` is installed:**
   ```bash
   curl --version
   ```
   *(If it's not installed, run `sudo apt-get install curl`)*

3. **Create a sample JSON file to represent a document:**
   ```bash
   echo '{"title": "Introduction to Elasticsearch", "author": "Trainer"}' > doc1.json
   ```

4. **View the document to ensure the format is correct:**
   ```bash
   cat doc1.json
   ```
   *Note how Elasticsearch uses this simple key-value structure instead of relational tables.*

---
[Return to Module 1](module1.md) | [Next Lab: Lab 2](lab2.md)

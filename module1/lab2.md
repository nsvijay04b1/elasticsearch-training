# Lab 2: Starting a Temporary Dev Node via Tarball

## Goal
Run a temporary single-node development cluster on your Ubuntu machine without performing a system-wide installation.

## Scenario
*Why are we doing this?* Before committing to installing Elasticsearch as a background `systemctl` service (which we will do properly in Lab 3), it is highly educational to quickly spin up a node in the foreground via a Tarball. This allows you to directly observe its startup logs, thread creation, and architecture bootstrapping happen locally before your eyes. Once we kill the process, it vanishes with no permanent system changes.

## Instructions

1. **Download the Linux Tar Archive:**

   *For standard x86/Intel/AMD machines:*
   ```bash
   wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.4-linux-x86_64.tar.gz
   ```

   *For ARM-based machines (e.g., Apple Silicon Mac M1/M2/M3 running an Ubuntu VM):*
   ```bash
   wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.4-linux-aarch64.tar.gz
   ```

2. **Extract the archive and enter the directory:**

   *(Make sure to change the filename below if you downloaded the `aarch64` version instead!)*
   ```bash
   tar -xzf elasticsearch-8.10.4-linux-x86_64.tar.gz
   cd elasticsearch-8.10.4/
   ```

3. **Start the node in the foreground:**
   By running the binary directly, all logs will print directly to your terminal screen.
   ```bash
   ./bin/elasticsearch
   ```

4. **Open a second terminal window (or tab)** on your Ubuntu VM.
   *Leave the first terminal running Elasticsearch in the foreground!*

5. **Create an Index:**
   Since security is enabled by default in 8.x, we must use `curl` with the generated `elastic` password. *(Replace `<PASSWORD>` with the password printed in terminal 1).*
   ```bash
   **Create an Index and Verify Shards/Replicas:**
```bash
curl -X PUT "https://localhost:9200/my_test_index" --insecure -u elastic:<PASSWORD>
   ```

6. **Query the Index:**
   Verify the index exists and check its settings.
   ```bash
   curl -X GET "https://localhost:9200/my_test_index" --insecure -u elastic:<PASSWORD>
   ```

7. **Check Shards and Replicas:**
   Get a visual readout of the shards allocated to your new index via the `_cat/shards` API.
   ```bash
   curl -X GET "https://localhost:9200/_cat/shards/my_test_index?v" --insecure -u elastic:<PASSWORD>
   ```
   *Note: Because you only have 1 node, the Primary shard will display as `STARTED`, but the Replica shard will display as `UNASSIGNED`.*

8. **Stop the node:**
   Return to your FIRST terminal window and press `CTRL+C` to gracefully shut down Elasticsearch.

---

---

---
[Previous Lab: Lab 1](lab1.md) | [Return to Module 1](module1.md) | [Next Lab: Lab 3](../module2/lab3.md)

# Lab 2: Starting a Temporary Dev Node via Tarball

## Goal
Run a temporary single-node development cluster on your Ubuntu machine without performing a system-wide installation.

## Scenario
*Why are we doing this?* Before committing to installing Elasticsearch as a background `systemctl` service (which we will do properly in Lab 3), it is highly educational to quickly spin up a node in the foreground via a Tarball. This allows you to directly observe its startup logs, thread creation, and architecture bootstrapping happen locally before your eyes. Once we kill the process, it vanishes with no permanent system changes.

## Instructions

1. **Download the Linux Tar Archive:**
   ```bash
   wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.4-linux-x86_64.tar.gz
   ```

2. **Extract the archive and enter the directory:**
   ```bash
   tar -xzf elasticsearch-8.10.4-linux-x86_64.tar.gz
   cd elasticsearch-8.10.4/
   ```

3. **Start the node in the foreground:**
   By running the binary directly, all logs will print directly to your terminal screen.
   ```bash
   ./bin/elasticsearch
   ```

4. **Observe the Bootstrapping Process:**
   - Look for the log line containing `[node.name]`. This assigned your node a temporary name.
   - Look for the elected master log: `elected-as-master`. Since this is the only node, it automatically acts as the Master node.
   - Look for the security auto-configuration logs outputting the temporary `elastic` password and enrollment tokens.

5. **Stop the node:**
   Once you've verified it boots, kill the foreground process by pressing `CTRL+C` in your terminal.

---
[Previous Lab: Lab 1](lab1.md) | [Return to Module 1](module1.md) | [Next Lab: Lab 3](../module2/lab3.md)

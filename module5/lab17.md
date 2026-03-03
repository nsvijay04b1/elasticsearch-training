# Lab 17: Configuring Local Snapshots

## Goal
Configure a Local File System repository directly on the Ubuntu machine and execute a manual backup snapshot.

## Scenario
While backing up to S3 is standard for production, you need to execute a rapid, local backup of your cluster prior to performing a risky data migration.

## Prerequisites
- You must be securely connected to your Ubuntu VM terminal with `sudo` privileges.
- You must be logged into the Kibana Web UI and have the Dev Tools console open.

## Instructions

1. **Register the backup path in Elasticsearch:**
   By default, Elasticsearch fundamentally blocks node processes from writing arbitrary files anywhere outside of its predefined `/var/lib/elasticsearch` data directory. This is a crucial security feature preventing malicious actors from using elasticsearch to overwrite system files if the node is compromised. To create a local snapshot repository, we must explicitly whitelist a safe backup path in the `elasticsearch.yml` configuration file first.
   
   *(In your Ubuntu Terminal):*
   ```bash
   echo 'path.repo: ["/var/backups/es_repo"]' | sudo tee -a /etc/elasticsearch/elasticsearch.yml
   ```

2. **Create the directory and assign permissions:**
   ```bash
   sudo mkdir -p /var/backups/es_repo
   sudo chown -R elasticsearch:elasticsearch /var/backups/es_repo
   ```

3. **Restart Elasticsearch to apply settings:**
   ```bash
   sudo systemctl restart elasticsearch.service
   ```
   *(Wait ~30 seconds for the node to come back online).*

4. **Register the Repository (in Kibana Dev Tools):**
   ```json
   PUT _snapshot/my_fs_backup
   {
     "type": "fs",
     "settings": { "location": "/var/backups/es_repo" }
   }
   ```

5. **Execute a Snapshot:**
   The `wait_for_completion` flag blocks the HTTP response until the backup finishes.
   ```json
   PUT _snapshot/my_fs_backup/snapshot_1?wait_for_completion=true
   ```

**Expected Output:**
```json
{
  "snapshot": {
    "snapshot": "snapshot_1",
    "state": "SUCCESS",
    "shards": { "total": 5, "successful": 5, "failed": 0 }
  }
}
```



### Part 2: Restoring from the Snapshot
If you accidentally delete an index or suffer corruption, you can easily restore it from the repository.

1. **Delete the original index (Simulate Data Loss):**
   ```json
   DELETE /products
   ```

2. **Restore from Snapshot:**
   ```json
   POST /_snapshot/my_fs_backup/snapshot_1/_restore
   {
     "indices": "products",
     "ignore_unavailable": true,
     "include_global_state": false
   }
   ```

3. **Verify the Restored Index:**
   ```json
   GET products/_count
   ```

   **Expected Output:**
   ```json
   { "count": 8 }
   ```
   *The data has been fully recovered from the snapshot!*

---

---


---
[Previous Lab: Lab 16](lab16.md) | [Return to Module 5](module5.md) | [Next Lab: Lab 18](lab18.md)

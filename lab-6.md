# Lab 6: Installing and Configuring Filebeat

## Goal
Ingest Ubuntu system logs into Elasticsearch via Filebeat, demonstrating the Beats shipper architecture.

## Scenario
You need to monitor the health of the very Ubuntu machine you are using to host the Elasticsearch cluster. By installing Filebeat, you can automatically parse `/var/log/syslog` and `/var/log/auth.log` directly into your cluster.

## Instructions

1. **Install Filebeat:**
   *(Since we already added the Elastic apt repository in Lab 3, this is straightforward).*
   ```bash
   sudo apt-get install filebeat
   ```

2. **Enable the System module:**
   This module tells Filebeat to specifically look for native Unix logs.
   ```bash
   sudo filebeat modules enable system
   ```

3. **Setup Filebeat Assets:**
   This command installs the pre-built Kibana dashboards and ingest pipelines required to parse system logs.
   ```bash
   sudo filebeat setup -e \
     -E output.elasticsearch.hosts=['https://localhost:9200'] \
     -E output.elasticsearch.username=elastic \
     -E output.elasticsearch.password='<YOUR_PASSWORD>' \
     -E output.elasticsearch.ssl.certificate_authorities=['/etc/elasticsearch/certs/http_ca.crt']
   ```
   *(Wait for this command to finish; it may take a minute).*

4. **Start Filebeat:**
   ```bash
   sudo systemctl enable filebeat
   sudo systemctl start filebeat
   ```

5. **Verify in Kibana:**
   - Open Kibana in your browser (`http://localhost:5601`).
   - Navigate to **Analytics -> Discover**.
   - Change your data view / index pattern to `filebeat-*`.
   - You should see your live Ubuntu logs streaming in!

---
[Return to Module 3](module-3.md)

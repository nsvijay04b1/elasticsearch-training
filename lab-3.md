# Lab 3: Installing Elasticsearch & Kibana on Ubuntu

## Goal
Install and start a single-node development Elasticsearch cluster alongside its visualization engine, Kibana.

## Scenario
You need a local environment to act as your sandbox throughout the rest of this training. We will use the APT package manager to securely pull the binaries direct from the Elastic repository.

## Instructions

1. **Install dependencies:**
   ```bash
   sudo apt-get update && sudo apt-get install apt-transport-https wget
   ```

2. **Import the Elastic PGP Key:**
   ```bash
   wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
   ```

3. **Add the repository definition to Ubuntu:**
   ```bash
   echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
   ```

4. **Install Elasticsearch and Kibana:**
   ```bash
   sudo apt-get update && sudo apt-get install elasticsearch kibana
   ```
   *Note: During installation, Elasticsearch automatically generates an `elastic` built-in superuser password. **Write this down immediately** if you see it in the terminal output!*

5. **Start the Elasticsearch Service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable elasticsearch.service
   sudo systemctl start elasticsearch.service
   ```

6. **Verify the installation:**
   Since v8.x, security is enabled by default. We must pass the self-signed certificate path and the `elastic` user credentials.
   ```bash
   # You will be prompted for your password:
   curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic https://localhost:9200
   ```
   *(A successful response is a JSON payload displaying the cluster name and Elasticsearch version).*

---
[Return to Module 2](module-2.md)

# Lab 4: Configuring Basic Security & Kibana Setup

## Goal
Establish secure interaction parameters by resetting the default superuser password and generating the security tokens required to link Kibana to the Elasticsearch node.

## Scenario
You missed the auto-generated password output during the `apt-get install` process, or you simply wish to set your own secure password. Furthermore, Kibana needs an enrollment token to securely pair with the database.

## Prerequisites
- Completion of Lab 3.
- Elasticsearch and Kibana MUST be installed on your Ubuntu VM.
- A modern web browser installed on your Ubuntu VM (e.g., Firefox, Chrome) or accessible from your host machine pointing to the VM.

## Instructions

1. **Resetting the `elastic` superuser password:**
   If you lost the auto-generated password from Lab 3, you have two approaches to reset it:

   *Method A: Auto-generate a new random password using the CLI tool:*
   ```bash
   sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic -i
   ```
   *(The `-i` flag allows you to pass it interactively if you wish to type it yourself, otherwise let it auto-generate and copy the output).*

   *Method B: Reset it manually via the Security API (cURL):*
   ```bash
   curl -u elastic -X POST "https://localhost:9200/_security/user/elastic/_password" \
        -H 'Content-Type: application/json' \
        -d '{ "password" : "your_new_password_here" }' \
        --cacert /etc/elasticsearch/certs/http_ca.crt
   ```

2. **Start the Kibana Service:**
   ```bash
   sudo systemctl enable kibana.service
   sudo systemctl start kibana.service
   ```
   *Tip: Kibana takes between 1-3 minutes to fully initialize.*

3. **Generate a Kibana enrollment token:**
   ```bash
   sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
   ```
   *(Copy this long string; you'll need it in the browser).*

4. **Retrieve the verification code:**
   ```bash
   sudo /usr/share/kibana/bin/kibana-verification-code
   ```

5. **Access the Kibana Web UI:**
   - Open a browser on your Ubuntu machine and navigate to: `http://localhost:5601`
   - Paste the enrollment token from Step 3 when prompted.
   - Enter the verification code from Step 4.
   - Log in using the username `elastic` and the password from Step 1.

---

---

---
[Previous Lab: Lab 3](lab3.md) | [Return to Module 2](module2.md) | [Next Lab: Lab 5](lab5.md)

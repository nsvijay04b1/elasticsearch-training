# Lab 7: Installing and Configuring Filebeat

## Goal
Ingest Ubuntu system logs into Elasticsearch via Filebeat, demonstrating the Beats shipper architecture.

## Scenario
You need to monitor the health of the very Ubuntu machine you are using to host the Elasticsearch cluster. By installing Filebeat, you can automatically parse `/var/log/syslog` and `/var/log/auth.log` directly into your cluster.

## Prerequisites
- Completion of Lab 4.
- Elasticsearch and Kibana must be running.
- You must have your `elastic` password.

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


### Part 2: Installing and Configuring Logstash


1. **Install Logstash via APT:**
   Since you already added the Elastic repository in Lab 3, you can simply install Logstash.
   ```bash
   sudo apt-get update && sudo apt-get install logstash
   ```

2. **Create a Logstash Pipeline Configuration:**
   We will create a simple pipeline that reads from your terminal (`stdin`), applies a dummy filter, and outputs to your secure Elasticsearch cluster.
   ```bash
   sudo nano /etc/logstash/conf.d/my_pipeline.conf
   ```

3. **Insert the Pipeline Code:**
   Paste the following into the file. **Make sure to replace `<PASSWORD>` with your elastic user password.** Note how we explicitly point to the `http_ca.crt` file for TLS verification!
   ```text
   input {
     stdin { }
   }

   filter {
     mutate {
       add_field => { "processed_by" => "logstash_lab" }
     }
   }

   output {
     elasticsearch {
       hosts => ["https://localhost:9200"]
       user => "elastic"
       password => "<PASSWORD>"
       cacert => "/etc/elasticsearch/certs/http_ca.crt"
       index => "logstash_test_index"
     }
     stdout { codec => rubydebug }
   }
   ```
   Save and exit (`CTRL+O`, `Enter`, `CTRL+X`).

4. **Run Logstash in the Foreground:**
   Instead of starting it as a system service, we'll run it manually so we can interact with `stdin`.
   ```bash
   sudo /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/my_pipeline.conf
   ```
   *Note: Logstash runs on the JVM and takes 30-60 seconds to boot depending on your VM resources.*

5. **Test the Pipeline:**
   Once you see `Pipeline main started`, type a message into your terminal and press `Enter`:
   `Hello from the Logstash Lab!`

6. **Verify the Output:**
   Logstash should immediately print a parsed JSON response to your terminal (thanks to the `rubydebug` stdout codec), showing the `message` alongside the newly appended `processed_by` field! It is also simultaneously being indexed into Elasticsearch.

7. **Stop Logstash:**
   Press `CTRL+C` to gracefully terminate the Logstash foreground process.


---

---

---
[Previous Lab: Lab 6](lab6.md) | [Return to Module 3](module3.md) | [Next Lab: Lab 8](lab8.md)

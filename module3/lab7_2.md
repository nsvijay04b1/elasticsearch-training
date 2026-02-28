# Lab 7.2: Installing and Configuring Logstash

## Goal
Install Logstash on your Ubuntu VM and configure a basic pipeline to ingest data from standard input (terminal) and output it to Elasticsearch.

## Scenario
While Beats (like Filebeat) are lightweight shippers used on edge nodes, Logstash is a heavy-duty data processing pipeline. You need to install Logstash to act as an ingestion node that can perform advanced `grok` filtering, data transformations, and enrichments before sending the final parsed logs to Elasticsearch.

## Prerequisites
- Completion of Lab 4.
- Elasticsearch and Kibana MUST be running securely.
- You must have your `elastic` superuser password and the path to your Elasticsearch HTTP CA certificate.

## Instructions

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
[Previous Lab: Lab 7](lab7.md) | [Return to Module 3](module3.md) | [Next Lab: Lab 8](lab8.md)

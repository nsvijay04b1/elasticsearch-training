# Lab 3: Installing Elasticsearch & Kibana on Ubuntu

## Goal
Install and start a single-node development Elasticsearch cluster alongside its visualization engine, Kibana.

## Scenario
In Lab 2, we downloaded the tarball and ran Elasticsearch in the foreground just to observe the bootstrapping logs temporarily. 
Now, we need a permanent, production-ready installation that runs in the background. We will use the APT package manager to securely install Elasticsearch as a permanent `systemd` service, which is the standard mechanism on Ubuntu.

*(We will also briefly cover alternative installation methods at the end of this lab).*

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


5. **(For MacBook Virtual Machine Users Only): Configure Interface Binding**
   If you are running Ubuntu as a VM on top of a Mac via a hypervisor (e.g. Parallels, UTM, UTM/QEMU), the default `localhost` bindings will prevent your host Mac's browser from reaching the VM. You must explicitly configure Elasticsearch and Kibana with the following settings before starting the services:


| Setting | Component | Purpose |
|---------|-----------|---------|
| `network.host: 0.0.0.0` | Elasticsearch | Allows the Mac browser to reach the database API on port 9200. |
| `server.host: "0.0.0.0"` | Kibana | Allows the Mac browser to reach the user interface on port 5601. |
| `discovery.type: single-node` | Elasticsearch | Forces "demo mode" so it doesn't try to find other servers, saving CPU and RAM. |
| `-Xms1g / -Xmx1g` | JVM Options | Limits RAM usage to 1GB so your 4GB VM doesn't crash from "Out of Memory" errors. |
| `xpack.security.enabled` | Both | Activates built-in security, requiring a password for the Mac to connect. |


   *Edit `/etc/elasticsearch/elasticsearch.yml` and `/etc/kibana/kibana.yml` respectively with `nano` to apply these settings. To apply the JVM options, create a file named `/etc/elasticsearch/jvm.options.d/memory.options` and add `-Xms1g` and `-Xmx1g` on separate lines.*

6. **Start the Elasticsearch Service:**

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable elasticsearch.service
   sudo systemctl start elasticsearch.service
   ```

7. **Verify the installation:**
   Since v8.x, security is enabled by default. We must pass the self-signed certificate path and the `elastic` user credentials.
   ```bash
   # You will be prompted for your password:
   curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic https://localhost:9200
   ```
   *(A successful response is a JSON payload displaying the cluster name and Elasticsearch version).*

8. **Resetting the `elastic` superuser password:**
   If you missed or forgot the auto-generated password from Step 4, you should reset it now before proceeding. You have two approaches:

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




---
## Alternative Installation Methods

While `apt` is the recommended approach for Ubuntu VMs, there are other valid methods depending on your environment constraints:

### Alternative 1: Direct `.deb` Download
If your Ubuntu VM does not have outgoing internet access to add the Elastic APT repository, you can securely scp the `.deb` file from another machine and install it manually:
*For standard x86/Intel/AMD machines:*
```bash
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.4-amd64.deb
sudo dpkg -i elasticsearch-8.10.4-amd64.deb
```

*For ARM-based machines (e.g., Apple Silicon Mac M1/M2/M3 running an Ubuntu VM):*
```bash
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.4-arm64.deb
sudo dpkg -i elasticsearch-8.10.4-arm64.deb
```
**Prerequisites:** Requires a pre-downloaded `.deb` file and `sudo` access.

### Alternative 2: Docker Container
For highly isolated, containerized environments, you can pull the official Docker image.
```bash
sudo docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.10.4
```
**Prerequisites:** Requires Docker Engine installed on your Ubuntu VM (`sudo apt-get install docker.io`).

---

---

---
[Previous Lab: Lab 2](../module1/lab2.md) | [Return to Module 2](module2.md) | [Next Lab: Lab 4](lab4.md)

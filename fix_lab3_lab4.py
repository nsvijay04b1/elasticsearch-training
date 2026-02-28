import re
import os

base_dir = "/Users/vijaynaravula/work/projects/elk/training"
lab3_path = os.path.join(base_dir, "module2/lab3.md")
lab4_path = os.path.join(base_dir, "module2/lab4.md")

with open(lab3_path, "r") as f:
    lab3_c = f.read()
    
# Add password reset to Lab 3 right after Verifying Installation
password_steps = """   *(A successful response is a JSON payload displaying the cluster name and Elasticsearch version).*

8. **Resetting the `elastic` superuser password:**
   If you missed or forgot the auto-generated password from Step 4, you should reset it now before proceeding. You have two approaches:

   *Method A: Auto-generate a new random password using the CLI tool:*
   ```bash
   sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic -i
   ```
   *(The `-i` flag allows you to pass it interactively if you wish to type it yourself, otherwise let it auto-generate and copy the output).*

   *Method B: Reset it manually via the Security API (cURL):*
   ```bash
   curl -u elastic -X POST "https://localhost:9200/_security/user/elastic/_password" \\
        -H 'Content-Type: application/json' \\
        -d '{ "password" : "your_new_password_here" }' \\
        --cacert /etc/elasticsearch/certs/http_ca.crt
   ```
"""
if "Resetting the `elastic` superuser password:" not in lab3_c:
    lab3_c = lab3_c.replace("   *(A successful response is a JSON payload displaying the cluster name and Elasticsearch version).*", password_steps)
    with open(lab3_path, "w") as f:
        f.write(lab3_c)

# Remove password reset from Lab 4
with open(lab4_path, "r") as f:
    lab4_c = f.read()

# Using regex to remove Step 1
lab4_c = re.sub(r'1\. \*\*Resetting the `elastic` superuser password:\*\*.*?\n\n2\. \*\*Start the Kibana Service:\*\*', '1. **Start the Kibana Service:**', lab4_c, flags=re.DOTALL)

# Re-number remaining steps
lab4_c = lab4_c.replace("3. **Generate a Kibana", "2. **Generate a Kibana")
lab4_c = lab4_c.replace("4. **Retrieve the verification", "3. **Retrieve the verification")
lab4_c = lab4_c.replace("5. **Access the Kibana", "4. **Access the Kibana")

# Fix references in the final step to the new numbers
lab4_c = lab4_c.replace("enrollment token from Step 3", "enrollment token from Step 2")
lab4_c = lab4_c.replace("verification code from Step 4", "verification code from Step 3")
lab4_c = lab4_c.replace("password from Step 1", "password from Lab 3")
lab4_c = lab4_c.replace("establishing secure interaction parameters by resetting the default superuser password and ", "")
lab4_c = lab4_c.replace("You missed the auto-generated password output during the `apt-get install` process, or you simply wish to set your own secure password. Furthermore, Kibana needs", "Kibana needs")

with open(lab4_path, "w") as f:
    f.write(lab4_c)

print("Updated Lab 3 and Lab 4")

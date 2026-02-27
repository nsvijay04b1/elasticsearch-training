import os
import shutil
import re

base_dir = "/Users/vijaynaravula/work/projects/elk/training"

# Define mappings
modules = {
    1: ["lab-1.md", "lab-2.md"],
    2: ["lab-3.md", "lab-4.md"],
    3: ["lab-5.md", "lab-6.md", "lab-7.md"],
    4: ["lab-8.md", "lab-9.md", "lab-10.md"],
    5: ["lab-11.md", "lab-12.md"],
    6: ["lab-13.md", "lab-14.md"]
}

# Rewrite Lab 2 to be a real lab
lab2_content = """# Lab 2: Starting a Temporary Dev Node via Tarball

## Goal
Run a temporary single-node development cluster on your Ubuntu machine without performing a system-wide installation.

## Scenario
Before committing to installing Elasticsearch as a background service (which we will do in Module 2), you want to quickly spin up a development node in the foreground to observe its startup logs and architecture bootstrapping.

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
[Return to Module 1](module1.md) | [Previous Lab: Lab 1](lab1.md)
"""

with open(os.path.join(base_dir, "lab-2.md"), "w") as f:
    f.write(lab2_content)

# Process modules
for mod_num, labs in modules.items():
    mod_dir = os.path.join(base_dir, f"module{mod_num}")
    img_dir = os.path.join(mod_dir, "images")
    os.makedirs(img_dir, exist_ok=True)
    
    # move module file
    old_mod_path = os.path.join(base_dir, f"module-{mod_num}.md")
    new_mod_path = os.path.join(mod_dir, f"module{mod_num}.md")
    if os.path.exists(old_mod_path):
        os.rename(old_mod_path, new_mod_path)
        
    for lab in labs:
        old_lab_path = os.path.join(base_dir, lab)
        new_lab_path = os.path.join(mod_dir, lab.replace("-", ""))
        if os.path.exists(old_lab_path):
            os.rename(old_lab_path, new_lab_path)

print("Moved files into structure.")

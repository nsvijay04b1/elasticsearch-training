import os
import re

base_dir = "/Users/vijaynaravula/work/projects/elk/training"

prereqs = {
    "module1/lab1.md": """## Prerequisites
- You must be logged into your provided Ubuntu VM.
- Ensure you have a working internet connection.
- You must have administrative (`sudo`) privileges.
""",
    "module1/lab2.md": """## Prerequisites
- Completion of Lab 1.
- You must be logged into your Ubuntu VM.
- Ensure you have a working internet connection.
""",
    "module2/lab3.md": """## Prerequisites
- You must be logged into your Ubuntu VM.
- Your user account must have `sudo` privileges (to install packages).
- Ensure you have a working internet connection.
""",
    "module2/lab4.md": """## Prerequisites
- Completion of Lab 3.
- Elasticsearch and Kibana MUST be installed on your Ubuntu VM.
- A modern web browser installed on your Ubuntu VM (e.g., Firefox, Chrome) or accessible from your host machine pointing to the VM.
""",
    "module3/lab5.md": """## Prerequisites
- Completion of Lab 4.
- Elasticsearch must be running securely.
- You must have your `elastic` superuser password handy.
""",
    "module3/lab6.md": """## Prerequisites
- Completion of Lab 4.
- Elasticsearch and Kibana must be running.
- You must have your `elastic` password.
""",
    "module3/lab7.md": """## Prerequisites
- Completion of Lab 4.
- Kibana must be running and accessible via your web browser.
- You must be logged into the Kibana Web UI.
""",
    "module4/lab8.md": """## Prerequisites
- Completion of Lab 5 (The `products` index must exist).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.
""",
    "module4/lab9.md": """## Prerequisites
- Completion of Lab 5 (The `products` index must exist).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.
""",
    "module4/lab10.md": """## Prerequisites
- Completion of Lab 5 (The `products` index must exist).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.
""",
    "module5/lab11.md": """## Prerequisites
- You must be logged into the Kibana Web UI and have the Dev Tools console open.
""",
    "module5/lab12.md": """## Prerequisites
- You must be securely connected to your Ubuntu VM terminal with `sudo` privileges.
- You must be logged into the Kibana Web UI and have the Dev Tools console open.
""",
    "module6/lab13.md": """## Prerequisites
- Completion of Lab 5 (The `products` index must exist).
- You must be logged into the Kibana Web UI and have the Dev Tools console open.
""",
    "module6/lab14.md": """## Prerequisites
- You must be logged into the Kibana Web UI and have the Dev Tools console open.
"""
}

for path, prereq_text in prereqs.items():
    full_path = os.path.join(base_dir, path)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            content = f.read()
        
        # If prereqs already added, skip
        if "## Prerequisites" in content:
            continue
            
        # Inject right before instructions
        content = content.replace("## Instructions", prereq_text + "\n## Instructions")
        
        with open(full_path, "w") as f:
            f.write(content)

print("Injected prerequisites into all labs.")

import os
import re

base_dir = "/Users/vijaynaravula/work/projects/elk/training"

modules = {
    1: ["lab1.md", "lab2.md"],
    2: ["lab3.md", "lab4.md"],
    3: ["lab5.md", "lab6.md", "lab7.md"],
    4: ["lab8.md", "lab9.md", "lab10.md"],
    5: ["lab11.md", "lab12.md"],
    6: ["lab13.md", "lab14.md"]
}

readme_path = os.path.join(base_dir, "README.md")
with open(readme_path, "r") as f:
    readme_content = f.read()

for i in range(1, 7):
    readme_content = re.sub(rf"\(module-{i}\.md\)", f"(module{i}/module{i}.md)", readme_content)

for mod_num, labs in modules.items():
    for lab in labs:
        old_lab = lab[:3] + "-" + lab[3:]
        readme_content = re.sub(rf"\({old_lab}\)", f"(module{mod_num}/{lab})", readme_content)

with open(readme_path, "w") as f:
    f.write(readme_content)

global_labs = []
for m, labs in modules.items():
    global_labs.extend(labs)

for mod_num, labs in modules.items():
    mod_dir = os.path.join(base_dir, f"module{mod_num}")
    mod_file = os.path.join(mod_dir, f"module{mod_num}.md")
    if os.path.exists(mod_file):
        with open(mod_file, "r") as f:
            content = f.read()
        for lab in labs:
            old_lab = lab[:3] + "-" + lab[3:]
            content = re.sub(rf"\({old_lab}\)", f"({lab})", content)
        with open(mod_file, "w") as f:
            f.write(content)
    
    for idx, lab in enumerate(labs):
        lab_file = os.path.join(mod_dir, lab)
        if os.path.exists(lab_file):
            with open(lab_file, "r") as f:
                content = f.read()
            
            content = re.sub(rf"\(module-{mod_num}\.md\)", f"(module{mod_num}.md)", content)
            
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if "[Return to Module" in line:
                    nav_links = []
                    current_global_idx = global_labs.index(lab)
                    if current_global_idx > 0:
                        prev_lab = global_labs[current_global_idx - 1]
                        prev_mod = None
                        for m, l in modules.items():
                            if prev_lab in l:
                                prev_mod = m
                                break
                        if prev_mod == mod_num:
                            nav_links.append(f"[Previous Lab: {prev_lab.capitalize().replace('.md', '').replace('Lab', 'Lab ')}]({prev_lab})")
                        else:
                            nav_links.append(f"[Previous Lab: {prev_lab.capitalize().replace('.md', '').replace('Lab', 'Lab ')}](../module{prev_mod}/{prev_lab})")
                        
                    nav_links.append(f"[Return to Module {mod_num}](module{mod_num}.md)")
                    
                    if current_global_idx < len(global_labs) - 1:
                        next_lab = global_labs[current_global_idx + 1]
                        next_mod = None
                        for m, l in modules.items():
                            if next_lab in l:
                                next_mod = m
                                break
                        if next_mod == mod_num:
                            nav_links.append(f"[Next Lab: {next_lab.capitalize().replace('.md', '').replace('Lab', 'Lab ')}]({next_lab})")
                        else:
                            nav_links.append(f"[Next Lab: {next_lab.capitalize().replace('.md', '').replace('Lab', 'Lab ')}](../module{next_mod}/{next_lab})")
                            
                    new_lines.append(" | ".join(nav_links))
                else:
                    new_lines.append(line)
            
            with open(lab_file, "w") as f:
                f.write('\n'.join(new_lines))

print("Updated links globally.")

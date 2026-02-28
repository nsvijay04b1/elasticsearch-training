import urllib.request
import os

base_dir = "/Users/vijaynaravula/work/projects/elk/training"
os.makedirs(os.path.join(base_dir, "module2/images"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "module4/images"), exist_ok=True)

images = [
    {
        "url": "https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt0302b1be706859e9/5d095596e232fe177d9406dd/kibana-dev-tools.png",
        "save_path": os.path.join(base_dir, "module2/images/kibana_dev_tools.png")
    },
    {
        "url": "https://raw.githubusercontent.com/elastic/elasticsearch-labs/main/supporting-blog-content/building-advanced-visualizations-kibana-vega/images/airline-cancelations-vega-screenshot.png",
        "save_path": os.path.join(base_dir, "module4/images/kibana_dashboard.png")
    }
]

for img in images:
    try:
        req = urllib.request.Request(img["url"], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(img["save_path"], "wb") as f_img:
            f_img.write(response.read())
        print(f"Saved {img['save_path']}")
    except Exception as e:
        print(f"Failed to fetch {img['url']}: {e}")

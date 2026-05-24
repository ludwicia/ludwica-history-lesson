import os
import re
import urllib.request
import time
from urllib.parse import unquote

# Create images folder
os.makedirs("c:/Users/USER/gemini的簡單歷史課/images", exist_ok=True)

with open("c:/Users/USER/gemini的簡單歷史課/build_html_md.py", "r", encoding="utf-8") as f:
    content = f.read()

urls = list(set(re.findall(r'https://upload.wikimedia.org[^\'\"]+', content)))

print(f"Found {len(urls)} unique URLs")

for i, url in enumerate(urls):
    filename = url.split('/')[-1]
    filename = unquote(filename)
    filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)
    # Ensure filename doesn't get too long
    if len(filename) > 50:
        ext = filename.split('.')[-1]
        filename = filename[:40] + '.' + ext
    
    local_path = f"images/img_{i:02d}_{filename}"
    full_local_path = f"c:/Users/USER/gemini的簡單歷史課/{local_path}"
    
    print(f"Downloading {url}\n  to {local_path} ...")
    
    success = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req) as response, open(full_local_path, 'wb') as out_file:
                out_file.write(response.read())
            print("  Success")
            success = True
            break
        except Exception as e:
            print(f"  Failed attempt {attempt+1}: {e}")
            time.sleep(3)
            
    if success:
        content = content.replace(url, local_path)
    time.sleep(1.5)

with open("c:/Users/USER/gemini的簡單歷史課/build_html_md.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Finished updating build_html_md.py")

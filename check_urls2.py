import urllib.request
import re
import time

with open('c:/Users/USER/gemini的簡單歷史課/build_html_md.py', 'r', encoding='utf-8') as f:
    content = f.read()

urls = re.findall(r'https://upload.wikimedia.org[^\'\"]+', content)

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        print('OK: ' + str(res.status) + ' ' + u)
    except urllib.error.HTTPError as e:
        print('FAIL: ' + str(e.code) + ' ' + u)
    except Exception as e:
        print('FAIL: ' + str(e) + ' ' + u)
    time.sleep(1)

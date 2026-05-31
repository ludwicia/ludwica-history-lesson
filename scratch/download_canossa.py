import os
import urllib.request

# Single file to download
url = "https://commons.wikimedia.org/wiki/Special:FilePath/Schwoiser_Heinrich_vor_Canossa.jpg"
path = "images/ottonian_canossa.jpg"

user_agent = "HistoryLessonPortalBot/1.0 (ludwicia@users.noreply.github.com) urllib/3.1"

os.makedirs("images", exist_ok=True)

print(f"Downloading {url} to {path}...")
try:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(req, timeout=20) as response:
        with open(path, "wb") as f:
            f.write(response.read())
        print(f"Successfully downloaded {path}")
except Exception as e:
    print(f"Error downloading {path}: {e}")

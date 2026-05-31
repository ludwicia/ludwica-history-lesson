import os
import urllib.request
import time

# Special:FilePath URLs that automatically resolve to the correct upload path
images = {
    "images/ottonian_hre_map.svg": "https://commons.wikimedia.org/wiki/Special:FilePath/Holy_Roman_Empire_1000_map-de.svg",
    "images/ottonian_otto1.jpg": "https://commons.wikimedia.org/wiki/Special:FilePath/Der_Magdeburger_Reiter.jpg",
    "images/ottonian_bruno.jpg": "https://commons.wikimedia.org/wiki/Special:FilePath/Bruno_the_Great.jpg",
    "images/ottonian_goslar.jpg": "https://commons.wikimedia.org/wiki/Special:FilePath/Goslar,_Kaiserpfalz_--_2008_--_0354.jpg",
    "images/ottonian_canossa.jpg": "https://commons.wikimedia.org/wiki/Special:FilePath/Matilda_of_Tuscany_Hugh_of_Cluny_Henry_IV.jpg"
}

# Custom User-Agent to comply with Wikimedia's policy and avoid 429
user_agent = "HistoryLessonPortalBot/1.0 (ludwicia@users.noreply.github.com) urllib/3.1"

os.makedirs("images", exist_ok=True)

for path, url in images.items():
    print(f"Downloading {url} to {path}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=20) as response:
            with open(path, "wb") as f:
                f.write(response.read())
            print(f"Successfully downloaded {path}")
    except Exception as e:
        print(f"Error downloading {path}: {e}")
    time.sleep(3.0)  # Be polite to Wikimedia Commons

print("All downloads finished!")

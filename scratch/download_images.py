import urllib.request
import os
import time

images_to_download = {
    "hirsau_main_wilhelm.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Wilhelm_Hirsau.jpg/500px-Wilhelm_Hirsau.jpg",
    "hirsau_st_aurelius.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Aureliuskirche_%28Hirsau%29_Gesamt.jpg/500px-Aureliuskirche_%28Hirsau%29_Gesamt.jpg",
    "hirsau_interior_historical.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Dehio_230_Hirsau_St_Aurelius1.jpg/500px-Dehio_230_Hirsau_St_Aurelius1.jpg",
    "hirsau_hunting_lodge.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Torturm_und_Jagdschloss_Kloster_Hirsau.jpg/500px-Torturm_und_Jagdschloss_Kloster_Hirsau.jpg",
    "hirsau_ruins_overview.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Kloster_Hirsau_2010.jpg/960px-Kloster_Hirsau_2010.jpg",
    "hirsau_cubic_capitals.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Aureliuskirche_%28Hirsau%29_W%C3%BCrfelkapitelle.jpg/500px-Aureliuskirche_%28Hirsau%29_W%C3%BCrfelkapitelle.jpg",
    "hirsau_romanesque_details.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Aureliuskirche_%28Hirsau%29_romanische_W%C3%BCrfelkapitelle_Ost.jpg/500px-Aureliuskirche_%28Hirsau%29_romanische_W%C3%BCrfelkapitelle_Ost.jpg",
    "hirsau_bausubstanz_map.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Hirsau_Karte_Bausubstanz.jpg/500px-Hirsau_Karte_Bausubstanz.jpg",
    "hirsau_eulenturm.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/20220715_Eulenturm%2C_Hirsau_9265.jpg/500px-20220715_Eulenturm%2C_Hirsau_9265.jpg",
    "hirsau_kreuzgang.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Kreuzgang_vom_Peter-und-Pauls-Kloster%2C_Hirsau.jpg/500px-Kreuzgang_vom_Peter-und-Pauls-Kloster%2C_Hirsau.jpg",
    "hirsau_modern_madonna.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Interior_of_Aureliuskirche_%28Hirsau%29_Madonna.jpg/500px-Interior_of_Aureliuskirche_%28Hirsau%29_Madonna.jpg"
}

os.makedirs("images", exist_ok=True)

# Build a compliant opener conforming to Wikimedia robot policy (User-Agent with contact info)
opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'LudwicaHistoryLessonBot/1.0 (https://ludwicia.github.io/ludwica-history-lesson/; ludwicia@example.com) Python-urllib/3.x')
]
urllib.request.install_opener(opener)

for filename, url in images_to_download.items():
    dest_path = os.path.join("images", filename)
    
    # Skip if already exists and is non-empty
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        print(f"Skipping {filename} - already exists")
        continue

    print(f"Downloading {filename} from {url}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        
    # Rate limit sleep to prevent HTTP 429
    time.sleep(3.0)

print("Image download task finished.")

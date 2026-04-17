import os
import requests
import random
import time

# --- CONFIGURATION ---
TOKEN = os.environ.get("FB_SYSTEM_TOKEN")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY")

PAGES = [
    {"id": "930225680182072", "query": "cute animals", "name": "Animal Friend"},
    {"id": "1019742297888078", "query": "vintage history old photos", "name": "Vintage History"},
    {"id": "937918212741480", "query": "luxury home interior architecture", "name": "Walls Down"},
    {"id": "975183022337508", "query": "wildlife animals nature", "name": "We Love Animals"}
]

CAPTIONS = [
    "Nature's beauty at its finest. ✨",
    "A moment frozen in time. 📸",
    "Simply breathtaking. 😍",
    "Did you know about this? 🧐",
    "Pure elegance and style. 🏛️",
    "Tag someone who needs to see this! 👇"
]

def get_pexels_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=50"
    headers = {"Authorization": PEXELS_KEY}
    res = requests.get(url, headers=headers).json()
    if "photos" in res and len(res["photos"]) > 0:
        photo = random.choice(res["photos"])
        return photo["src"]["large2x"], photo["alt"]
    return None, None

def post_to_fb(page_id, img_url, caption):
    fb_url = f"https://graph.facebook.com/v18.0/{page_id}/photos"
    payload = {
        "url": img_url,
        "message": f"{caption}\n.\n.\n#viral #trending #explore",
        "access_token": TOKEN
    }
    res = requests.post(fb_url, data=payload).json()
    return res

def main():
    # Humanize: Random initial delay (1-10 mins)
    time.sleep(random.randint(60, 600))
    
    for page in PAGES:
        print(f"🚀 Processing: {page['name']}")
        
        img_url, alt_text = get_pexels_image(page["query"])
        if img_url:
            caption = f"{alt_text if alt_text else random.choice(CAPTIONS)}"
            result = post_to_fb(page["id"], img_url, caption)
            
            if "id" in result:
                print(f"✅ Posted to {page['name']}! ID: {result['id']}")
            else:
                print(f"❌ Error on {page['name']}: {result}")
        
        # Humanize: Wait 2-5 minutes between each page post
        time.sleep(random.randint(120, 300))

if __name__ == "__main__":
    main()

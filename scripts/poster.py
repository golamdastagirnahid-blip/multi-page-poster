import os
import requests
import random
import time

# === CONFIG ===
TOKEN = os.environ.get("FB_SYSTEM_TOKEN")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY")

PAGES = [
    {
        "id": "591644197366268",
        "name": "Ai Magic",
        "query": "wildlife animals majestic nature",
        "style": "Animal and Wildlife"
    },
    {
        "id": "113472948289592",
        "name": "Nature Research",
        "query": "jungle rainforest beautiful nature landscape",
        "style": "Nature And Jungle"
    },
    {
        "id": "462341143635954",
        "name": "Dream Maker",
        "query": "luxury dream house beautiful home interior scenic places",
        "style": "Beautiful Place and Home"
    },
    {
        "id": "607881382401657",
        "name": "Shadow Celebrity",
        "query": "elegant fashion model portrait beautiful woman aesthetic",
        "style": "Model Women Celebrity"
    }
]

def get_pexels_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=80&orientation=portrait"
    headers = {"Authorization": PEXELS_KEY}
    response = requests.get(url, headers=headers).json()
    
    if "photos" in response and len(response["photos"]) > 0:
        photo = random.choice(response["photos"])
        return photo["src"]["large2x"], photo["alt"]
    return None, None

def generate_caption(page_name, alt_text):
    base = alt_text[:80] if alt_text else "Breathtaking view"
    hashtags = "#fyp #viral #explore #trending #aesthetic"
    
    if page_name == "Ai Magic":
        return f"{base} ✨\nNature's masterpiece.\n{hashtags}"
    elif page_name == "Nature Research":
        return f"{base} 🌿\nPure jungle magic.\n{hashtags}"
    elif page_name == "Dream Maker":
        return f"{base} 🏡\nDream home goals.\n{hashtags}"
    else:
        return f"{base} 💫\nTimeless elegance.\n{hashtags}"

def post_to_page(page_id, image_url, caption):
    url = f"https://graph.facebook.com/v18.0/{page_id}/photos"
    data = {
        "url": image_url,
        "message": caption,
        "access_token": TOKEN
    }
    return requests.post(url, data=data).json()

def main():
    print("🚀 Starting 4-Page Auto Poster...")
    
    # Humanized random start delay
    time.sleep(random.randint(30, 180))
    
    for page in PAGES:
        print(f"📸 Posting to → {page['name']}")
        
        img_url, alt = get_pexels_image(page["query"])
        
        if img_url:
            caption = generate_caption(page["name"], alt)
            result = post_to_page(page["id"], img_url, caption)
            
            if "id" in result:
                print(f"✅ Successfully posted on {page['name']}")
            else:
                print(f"❌ Failed on {page['name']} → {result}")
        else:
            print(f"⚠️ No image found for {page['name']}")
        
        # Humanized delay between pages (2 to 6 minutes)
        time.sleep(random.randint(120, 360))
    
    print("✅ Cycle completed. Next run in 2 hours.")

if __name__ == "__main__":
    main()

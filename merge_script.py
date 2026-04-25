import requests

# সোর্স ইউআরএলগুলো
urls = [
    "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/refs/heads/main/ALL.m3u"
]

def merge_playlists():
    # প্লেলিস্টের শুরু
    merged_content = "#EXTM3U\n"
    
    # আপনার কাস্টম প্রমোশন সেকশন
    PROMOTION = """#EXTINF:-1 tvg-id="" tvg-logo="https://bdixiptvbd.com/logo.png" group-title="IBS TV PROMOTION",--- [ IBS TV PROMOTION ] ---
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,IBS TV Download: bdixiptvbd.com
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,Telegram Channel: https://t.me/bdixiptvbd
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,WhatsApp: 01610598422
https://bdixiptvbd.com/live/Telegram.mp4
"""
    merged_content += PROMOTION

    # নিষিদ্ধ কি-ওয়ার্ড এবং লিঙ্ক
    BANNED_KEYWORD = "playz tv"
    BANNED_LINK_PART = "playztv.pages.dev"

    for url in urls:
        try:
            response = requests.get(url, timeout=25)
            if response.status_code == 200:
                lines = response.text.splitlines()
                
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    if line.startswith("#EXTINF"):
                        if (i + 1) < len(lines):
                            channel_url = lines[i+1].strip()
                            
                            # ১. চেক করা হচ্ছে চ্যানেলের নামে বা গ্রুপে নিষিদ্ধ শব্দ আছে কি না
                            # ২. চেক করা হচ্ছে ইউআরএল এর ভেতরে নিষিদ্ধ লিঙ্কের অংশ আছে কি না
                            is_banned_name = BANNED_KEYWORD in line.lower()
                            is_banned_url = BANNED_LINK_PART in channel_url.lower()

                            if not is_banned_name and not is_banned_url:
                                # যদি উপরের কোনোটিই না পাওয়া যায়, তবেই অ্যাড হবে
                                if channel_url.startswith("http"):
                                    merged_content += line + "\n"
                                    merged_content += channel_url + "\n"
                            
                            i += 2 # পরের চ্যানেলে চলে যাওয়া
                        else:
                            i += 1
                    else:
                        i += 1
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # ফাইনাল প্লেলিস্ট সেভ করা
    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(merged_content)
        print("Success! Clean playlist generated without PlayZ TV content.")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    merge_playlists()
    

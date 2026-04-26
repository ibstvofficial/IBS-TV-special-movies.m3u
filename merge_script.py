import requests
from datetime import datetime
import pytz

# সোর্স ইউআরএলগুলো
urls = [
    "https://aynaott-auto-update-playlist.pages.dev/AynaOTT.m3u",
    "https://iptv-org.github.io/iptv/languages/ben.m3u"
]

def merge_playlists():
    # বাংলাদেশ সময় সেট করা
    bd_tz = pytz.timezone('Asia/Dhaka')
    current_time = datetime.now(bd_tz).strftime('%I:%M %p %d-%m-%Y')

    # প্লেলিস্টের হেডার এবং প্রমোশন সেকশন
    HEADER = f"""#EXTM3U
# Playlist Name: IBS TV PRIME - LIVE
# Last Update: {current_time} (BD Time)
# Telegram: https://t.me/bdixiptvbd
# WhatsApp: 01610598422
# Owner: Md. Sakib Hasan
# Website: https://bdixiptvbd.com

#EXTINF:-1 tvg-id="" tvg-logo="https://bdixiptvbd.com/logo.png" group-title="IBS TV PROMOTION",--- [ IBS TV PROMOTION ] ---
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,IBS TV Download: bdixiptvbd.com
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,Telegram Channel: https://t.me/bdixiptvbd
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,WhatsApp: 01610598422
https://bdixiptvbd.com/live/Telegram.mp4
"""
    merged_content = HEADER

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
                            
                            # ফিল্টারিং লজিক (Case-insensitive)
                            is_banned_name = BANNED_KEYWORD in line.lower()
                            is_banned_url = BANNED_LINK_PART in channel_url.lower()

                            if not is_banned_name and not is_banned_url:
                                if channel_url.startswith("http"):
                                    merged_content += line + "\n"
                                    merged_content += channel_url + "\n"
                            
                            i += 2
                        else:
                            i += 1
                    else:
                        i += 1
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # ফাইল সেভ করা
    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(merged_content)
        print(f"Success! Playlist updated at {current_time}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    merge_playlists()
    

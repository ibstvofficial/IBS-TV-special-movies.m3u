import requests

# আপনার নতুন সোর্স ইউআরএলগুলো
urls = [
    "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/refs/heads/main/ALL.m3u"
]

def merge_playlists():
    merged_content = "#EXTM3U\n"
    
    # প্রমোশন সেকশন
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

    for url in urls:
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                lines = response.text.splitlines()
                
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    if line.startswith("#EXTINF"):
                        # "playZ TV" লেখা থাকলে সেই চ্যানেল বাদ দেওয়া হবে
                        if "playZ TV" not in line and (i + 1) < len(lines):
                            channel_url = lines[i+1].strip()
                            if channel_url.startswith("http"):
                                merged_content += line + "\n"
                                merged_content += channel_url + "\n"
                        i += 2
                    else:
                        i += 1
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(merged_content)
        print("Success! Live TV Playlist updated every 3 hours.")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    merge_playlists()
    

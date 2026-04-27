import requests
from datetime import datetime
import pytz
import re

# সোর্স ইউআরএলগুলো
urls = [
    "https://raw.githubusercontent.com/srhady/tapmad-bd/refs/heads/main/tapmad_bd.m3u",
    "https://raw.githubusercontent.com/srhady/Fancode-bd/refs/heads/main/main_playlist.m3u",
    "https://raw.githubusercontent.com/srhady/CricketLive/refs/heads/main/playlist.m3u",
    "https://aynaott-auto-update-playlist.pages.dev/AynaOTT.m3u",
    "https://iptv-org.github.io/iptv/languages/ben.m3u"
]

def clean_channel_name(name):
    # নামের মাঝখান থেকে অপ্রয়োজনীয় লেখা রিমুভ করা
    junk = ["| High Quality", "| BDIX", "| VIP", "SD", "HD", "FHD", "(Backup)", "Premium"]
    for word in junk:
        name = name.replace(word, "")
    return name.strip()

def normalize_group(group_name):
    group_name = group_name.upper()
    if any(x in group_name for x in ["SPORTS", "CRICKET", "FANCODE", "TAPMAD"]):
        return "SPORTS"
    if any(x in group_name for x in ["BANGLA", "BD", "AYNA"]):
        return "BANGLA TV"
    if any(x in group_name for x in ["NEWS", "খবর"]):
        return "NEWS"
    if any(x in group_name for x in ["MOVIE", "FILM"]):
        return "MOVIES"
    return "OTHERS"

def merge_playlists():
    bd_tz = pytz.timezone('Asia/Dhaka')
    current_time = datetime.now(bd_tz).strftime('%I:%M %p %d-%m-%Y')

    merged_content = f"""#EXTM3U
# Playlist Name: IBS TV PRIME - ULTIMATE
# Last Update: {current_time} (BD Time)
# Telegram: https://t.me/bdixiptvbd
# WhatsApp: 01610598422\n"""

    BANNED_KEYWORD = "playz tv"
    BANNED_LINK_PART = "playztv.pages.dev"
    DEFAULT_LOGO = "https://bdixiptvbd.com/logo.png"
    
    added_groups = set()
    seen_links = set() # ডুপ্লিকেট লিঙ্ক এড়ানোর জন্য

    for url in urls:
        try:
            print(f"Syncing: {url}")
            response = requests.get(url, timeout=25)
            if response.status_code == 200:
                lines = response.text.splitlines()
                
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith("#EXTINF"):
                        if (i + 1) < len(lines):
                            channel_url = lines[i+1].strip()
                            
                            # ১. ফিল্টারিং
                            if BANNED_KEYWORD in line.lower() or BANNED_LINK_PART in channel_url.lower():
                                i += 2
                                continue

                            if channel_url.startswith("http") and channel_url not in seen_links:
                                # ২. গ্রুপ এবং লোগো প্রসেসিং
                                group_match = re.search(r'group-title="([^"]+)"', line)
                                raw_group = group_match.group(1) if group_match else "OTHERS"
                                final_group = normalize_group(raw_group)

                                logo_match = re.search(r'tvg-logo="([^"]+)"', line)
                                final_logo = logo_match.group(1) if (logo_match and logo_match.group(1)) else DEFAULT_LOGO

                                # ৩. চ্যানেল নাম ক্লিনআপ
                                name_part = line.split(",")[-1]
                                final_name = clean_channel_name(name_part)

                                # ৪. গ্রুপের শুরুতে প্রমোশন চ্যানেল
                                if final_group not in added_groups:
                                    promo_line = f'#EXTINF:-1 tvg-logo="{DEFAULT_LOGO}" group-title="{final_group}",--- [ {final_group} PROMOTION ] ---'
                                    promo_url = "https://bdixiptvbd.com/live/Telegram.mp4"
                                    merged_content += promo_line + "\n" + promo_url + "\n"
                                    added_groups.add(final_group)

                                # ৫. নতুন ফরম্যাটে চ্যানেল যোগ করা
                                new_line = f'#EXTINF:-1 tvg-logo="{final_logo}" group-title="{final_group}",{final_name}'
                                merged_content += new_line + "\n" + channel_url + "\n"
                                seen_links.add(channel_url)
                            
                            i += 2
                        else:
                            i += 1
                    else:
                        i += 1
        except Exception as e:
            print(f"Error: {e}")

    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(merged_content)
        print(f"All Systems Integrated! Updated at {current_time}")
    except Exception as e:
        print(f"Save Error: {e}")

if __name__ == "__main__":
    merge_playlists()
            

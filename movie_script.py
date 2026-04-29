import requests
from datetime import datetime
import pytz
import re
import random

# মুভি সোর্স ইউআরএল
MOVIE_SOURCE = "https://raw.githubusercontent.com/srhady/join_telegram_chennal-livesportsplay/refs/heads/main/latest_movies.m3u"

# প্রমোশন ভিডিওর তালিকা (রেন্ডম সিলেকশনের জন্য)
PROMO_VIDEOS = [
    "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/promo%20dual.mp4",
    "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291577865.mp4",
    "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291501194.mp4"
]

def clean_movie_name(name):
    # মুভির নামের বাড়তি অংশ পরিষ্কার করা
    junk = ["| High Quality", "| BDIX", "| VIP", "SD", "HD", "FHD", "1080p", "720p", "WebRip", "Dual Audio", "Hindi Dubbed"]
    for word in junk:
        name = name.replace(word, "")
    return name.strip()

def create_movie_playlist():
    # সময় নির্ধারণ
    bd_tz = pytz.timezone('Asia/Dhaka')
    current_time = datetime.now(bd_tz).strftime('%I:%M %p %d-%m-%Y')

    # মুভি প্লেলিস্টের হেডার
    merged_content = f"""#EXTM3U
# Playlist Name: IBS TV SPECIAL MOVIES
# Total Movies: AUTO UPDATING
# Last Update: {current_time} (BD Time)
# Owner: Md. Sakib Hasan
# Telegram: https://t.me/bdixiptvbd\n"""

    DEFAULT_LOGO = "https://bdixiptvbd.com/logo.png"
    added_groups = set()
    seen_links = set()

    try:
        print(f"Fetching Movies from: {MOVIE_SOURCE}")
        response = requests.get(MOVIE_SOURCE, timeout=30)
        
        if response.status_code == 200:
            lines = response.text.splitlines()
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("#EXTINF"):
                    if (i + 1) < len(lines):
                        movie_url = lines[i+1].strip()
                        
                        # ডুপ্লিকেট চেক
                        if movie_url.startswith("http") and movie_url not in seen_links:
                            # গ্রুপ নির্ধারণ (মুভির জন্য আলাদা ক্যাটাগরি)
                            group_match = re.search(r'group-title="([^"]+)"', line)
                            final_group = group_match.group(1) if group_match else "LATEST MOVIES"

                            # লোগো চেক
                            logo_match = re.search(r'tvg-logo="([^"]+)"', line)
                            final_logo = logo_match.group(1) if (logo_match and logo_match.group(1)) else DEFAULT_LOGO

                            # নাম ক্লিনআপ
                            name_part = line.split(",")[-1]
                            final_name = clean_movie_name(name_part)

                            # রেন্ডম প্রোমোশন ভিডিও যোগ করা (প্রতিটি গ্রুপে একবার)
                            if final_group not in added_groups:
                                random_promo = random.choice(PROMO_VIDEOS)
                                promo_line = f'#EXTINF:-1 tvg-logo="{DEFAULT_LOGO}" group-title="IBS SPECIAL PROMO",--- [ {final_group} ] ---'
                                merged_content += promo_line + "\n" + random_promo + "\n"
                                added_groups.add(final_group)

                            # মুভি লিস্ট যোগ করা
                            new_line = f'#EXTINF:-1 tvg-logo="{final_logo}" group-title="{final_group}",{final_name}'
                            merged_content += new_line + "\n" + movie_url + "\n"
                            seen_links.add(movie_url)
                        
                        i += 2
                    else:
                        i += 1
                else:
                    i += 1

        # ফাইল সেভ করা (আপনার চাহিদা অনুযায়ী নাম দেওয়া হয়েছে)
        with open("IBS TV special.m3u", "w", encoding="utf-8") as f:
            f.write(merged_content)
        print(f"Success! Movie Playlist updated at {current_time}")

    except Exception as e:
        print(f"Error creating playlist: {e}")

if __name__ == "__main__":
    create_movie_playlist()
  

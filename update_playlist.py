import requests
import datetime
import re

# সোর্স ইউআরএলসমূহ
urls = [
    "https://raw.githubusercontent.com/srhady/SonyLiv/refs/heads/main/sonyliv_playlist.m3u",
    "https://raw.githubusercontent.com/srhady/Fancode-bd/refs/heads/main/main_playlist.m3u",
    "https://raw.githubusercontent.com/srhady/join_telegram_chennal-livesportsplay/refs/heads/main/bangla.m3u"
]

# ব্যাকআপ ভিডিও লিঙ্ক
BACKUP_VIDEO = "https://bdixiptvbd.com/live/Telegram.mp4"

# প্রমোশন টেকস্ট
PROMOTION = (
    "#EXTINF:-1 tvg-id=\"\" tvg-logo=\"https://bdixiptvbd.com/logo.png\" group-title=\"PROMOTION\",--- [ IBS TV PROMOTION ] ---\n"
    "https://bdixiptvbd.com/live/Telegram.mp4\n"
    "#EXTINF:-1,IBS TV Download: bdixiptvbd.com\n"
    "https://bdixiptvbd.com/live/Telegram.mp4\n"
    "#EXTINF:-1,Telegram: https://t.me/bdixiptvbd\n"
    "https://bdixiptvbd.com/live/Telegram.mp4\n"
    "#EXTINF:-1,WhatsApp: 01610598422\n"
    "https://bdixiptvbd.com/live/Telegram.mp4\n"
)

def process_m3u(text):
    processed_lines = []
    lines = text.splitlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # যদি এক্সটেনশন ইনফো হয়
        if line.startswith("#EXTINF"):
            info_line = line
            url_line = ""
            
            # পরবর্তী লাইনটি খোঁজা যা লিঙ্ক হতে পারে
            if i + 1 < len(lines):
                next_line = lines[i+1].strip()
                # যদি পরবর্তী লাইনটি খালি থাকে বা অন্য কোনো ইনফো হয়, তবে ব্যাকআপ লিঙ্ক বসবে
                if not next_line or next_line.startswith("#") or not next_line.startswith("http"):
                    url_line = BACKUP_VIDEO
                else:
                    url_line = next_line
                    i += 1 # লিঙ্ক পাওয়া গেছে, তাই ইনডেক্স এক ধাপ বাড়ানো হলো
            else:
                url_line = BACKUP_VIDEO
                
            processed_lines.append(info_line)
            processed_lines.append(url_line)
        i += 1
    return "\n".join(processed_lines)

def main():
    header = "#EXTM3U\n"
    header += f"## Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += f"## IBS TV Download: bdixiptvbd.com\n"
    header += f"## Telegram: https://t.me/bdixiptvbd | Group: https://t.me/bdixiptvbdchat\n"
    header += f"## Backup: https://t.me/ibstvbd | WhatsApp: 01610598422\n\n"
    
    # প্রথমে প্রমোশন চ্যানেলগুলো যোগ করা হচ্ছে
    final_content = header + PROMOTION + "\n"

    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                # কন্টেন্ট প্রসেস করে ব্যাকআপ লিঙ্ক নিশ্চিত করা হচ্ছে
                m3u_data = process_m3u(response.text)
                final_content += f"## Source: {url}\n" + m3u_data + "\n\n"
                print(f"Success: {url}")
            else:
                print(f"Error {response.status_code}: {url}")
        except Exception as e:
            print(f"Exception for {url}: {e}")

    # ফাইলটি সেভ করা হচ্ছে
    with open("merged_playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_content.strip())

if __name__ == "__main__":
    main()



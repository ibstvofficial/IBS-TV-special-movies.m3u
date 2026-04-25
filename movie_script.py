import requests
from bs4 import BeautifulSoup

# আপনার দেওয়া সোর্স ওয়েবসাইট
SOURCE_URL = "https://cxy5tj.movielinkbd.li/"

def generate_movie_playlist():
    print("Fetching movies from MovieLinkBD...")
    try:
        # ওয়েবসাইট থেকে ডেটা আনা
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(SOURCE_URL, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"Website access failed! Status: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # প্লেলিস্টের হেডার এবং আপনার প্রমোশন
        playlist_content = "#EXTM3U\n"
        playlist_content += '#EXTINF:-1 tvg-logo="https://bdixiptvbd.com/logo.png" group-title="IBS MOVIES",--- [ IBS TV MOVIE SERVICE ] ---\n'
        playlist_content += 'https://bdixiptvbd.com/live/Telegram.mp4\n'
        
        movies_found = 0
        
        # ওয়েবসাইট থেকে লিঙ্কগুলো খোঁজা
        for link in soup.find_all('a', href=True):
            href = link['href']
            title = link.get_text(strip=True)

            # শুধুমাত্র .mkv ফাইল অথবা মুভি কন্টেন্ট ফিল্টার করা
            if href.endswith('.mkv') or '.mkv' in href:
                # যদি টাইটেল না থাকে তবে ফাইলের নাম থেকে টাইটেল নেওয়া
                if not title:
                    title = href.split('/')[-1].replace('%20', ' ').replace('.mkv', '')
                
                playlist_content += f'#EXTINF:-1 tvg-logo="https://bdixiptvbd.com/logo.png" group-title="IBS PREMIUM MOVIES",{title}\n'
                playlist_content += f'{href}\n'
                movies_found += 1

        # ফাইলটি movies.m3u নামে সেভ করা
        with open("movies.m3u", "w", encoding="utf-8") as f:
            f.write(playlist_content)
        
        print(f"Success! {movies_found} MKV movies added to movies.m3u")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_movie_playlist()
  

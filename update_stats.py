import json
import urllib.request
from datetime import datetime, timezone

USER_ID = "6174930173"
UNIVERSE_ID = "9583356773"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def main():
    data = {}

    try:
        avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={USER_ID}&size=420x420&format=Png&isCircular=true"
        avatar_data = fetch_json(avatar_url)
        data['avatar'] = avatar_data['data'][0]['imageUrl']
    except Exception as e:
        print("Error fetching avatar:", e)
        data['avatar'] = ""

    try:
        followers_url = f"https://friends.roblox.com/v1/users/{USER_ID}/followers/count"
        followers_data = fetch_json(followers_url)
        data['followers'] = followers_data['count']
    except Exception as e:
        print("Error fetching followers:", e)
        data['followers'] = 0

    try:
        game_url = f"https://games.roblox.com/v1/games?universeIds={UNIVERSE_ID}"
        game_data = fetch_json(game_url)['data'][0]

        game_name = game_data.get('name', 'Game Name')

        game_stats = {
            'name': game_name,
            'active': game_data.get('playing', 0),
            'visits': game_data.get('visits', 0),
            'favorites': game_data.get('favoritedCount', 0),
            'image': ''
        }

        try:
            thumb_url = f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={UNIVERSE_ID}&countPerUniverse=1&defaults=true&size=768x432&format=Png&isCircular=false"
            thumb_data = fetch_json(thumb_url)
            game_stats['image'] = thumb_data['data'][0]['thumbnails'][0]['imageUrl']
        except Exception as e:
            print("Error fetching game thumbnail:", e)

        data['game'] = game_stats
    except Exception as e:
        print("Error fetching game stats:", e)
        data['game'] = {'name': 'Game Name', 'active': 0, 'visits': 0, 'favorites': 0, 'image': ''}

    data['last_updated'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Successfully updated data.json!")

if __name__ == '__main__':
    main()

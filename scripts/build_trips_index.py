import json
from pathlib import Path

POSTS_DIR = Path("data/posts")
OUTPUT_FILE = Path("data/trips.json")

trips = {}

# --- Load all posts ---
for file in POSTS_DIR.glob("*.json"):
    with open(file, "r") as f:
        post = json.load(f)

    trip_name = post["trip"]
    loc = post["location"]
    loc_key = loc["name"]

    if trip_name not in trips:
        trips[trip_name] = {
            "title": trip_name,
            "locations": {}
        }

    if loc_key not in trips[trip_name]["locations"]:
        trips[trip_name]["locations"][loc_key] = {
            "name": loc["name"],
            "lat": loc["lat"],
            "lng": loc["lng"],
            "posts": []
        }

    # Keep only necessary fields for frontend
    trips[trip_name]["locations"][loc_key]["posts"].append({
        "id": post["id"],  # 👈 important for Utterances
        "title": post["title"],
        "text": post["text"],
        "photos": post["photos"],
        "date": post["date"]
    })

# --- Convert dicts to arrays ---
output = []

for trip in trips.values():
    trip["locations"] = list(trip["locations"].values())

    # Optional: sort locations alphabetically
    trip["locations"].sort(key=lambda x: x["name"])

    # Optional: sort posts by date
    for loc in trip["locations"]:
        loc["posts"].sort(key=lambda p: p["date"] or "")

    output.append(trip)

# Optional: sort trips
output.sort(key=lambda t: t["title"])

# --- Write file ---
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Built {OUTPUT_FILE}")
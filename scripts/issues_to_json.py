import json
import os
import re
from pathlib import Path

# --- Load GitHub event payload ---
event_path = os.environ.get("GITHUB_EVENT_PATH")

with open(event_path, "r") as f:
    event = json.load(f)

issue = event["issue"]
body = issue["body"]
issue_number = issue["number"]

# --- Helper to extract fields from Issue Form ---
def get_field(label):
    pattern = rf"### {label}\s*([\s\S]*?)(?=###|$)"
    match = re.search(pattern, body)
    return match.group(1).strip() if match else ""

trip = get_field("Trip name")
location_name = get_field("Location name")
lat = float(get_field("Latitude") or 0)
lng = float(get_field("Longitude") or 0)
title = get_field("Post title")
text = get_field("Post text")
date = get_field("Date")

photos_raw = get_field("Photo URLs")
photos = [p.strip() for p in photos_raw.splitlines() if p.strip()]

# --- Slugify ---
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

slug = slugify(title)

# Use issue number to avoid duplicates
filename = f"{issue_number}__{slug}.json"

output_path = Path("data/posts") / filename
output_path.parent.mkdir(parents=True, exist_ok=True)

# --- Build JSON ---
data = {
    "id": issue_number,
    "trip": trip,
    "location": {
        "name": location_name,
        "lat": lat,
        "lng": lng
    },
    "title": title,
    "text": text,
    "photos": photos,
    "date": date,
    "updated_at": issue["updated_at"]
}

# --- Write file ---
with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Wrote {output_path}")
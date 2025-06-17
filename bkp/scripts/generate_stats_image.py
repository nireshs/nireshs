# scripts/generate_stats_image.py
import os
import requests
from PIL import Image, ImageDraw, ImageFont

GITHUB_API = "https://api.github.com"
REPO = "nireshs/myprojects2022"
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def fetch_stats():
    endpoints = {
        "open_issues": f"/repos/{REPO}/issues?state=open",
        "closed_issues": f"/repos/{REPO}/issues?state=closed",
        "pulls": f"/repos/{REPO}/pulls",
        "commits": f"/repos/{REPO}/commits",
    }

    stats = {}
    for key, endpoint in endpoints.items():
        response = requests.get(GITHUB_API + endpoint, headers=headers)
        if response.ok:
            stats[key] = len(response.json())
        else:
            stats[key] = -1  # Error
    return stats

def generate_image(stats):
    image = Image.new("RGB", (500, 200), color=(40, 44, 52))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    lines = [
        "Private Repo Stats: myprojects2022",
        f"Open Issues: {stats['open_issues']}",
        f"Closed Issues: {stats['closed_issues']}",
        f"Open PRs: {stats['pulls']}",
        f"Commits: {stats['commits']}",
    ]

    y = 10
    for line in lines:
        draw.text((10, y), line, font=font, fill=(173, 216, 230))
        y += 30

    os.makedirs("stats_output", exist_ok=True)
    image.save("stats_output/myprojects2022_stats.png")

if __name__ == "__main__":
    stats = fetch_stats()
    generate_image(stats)

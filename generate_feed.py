import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
from email.utils import format_datetime


URL = "https://www.newhampshireunderground.org/showsandevents"

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 RSS Feed Generator"
    }
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

warmup = soup.find(
    "script",
    {"id": "wix-warmup-data"}
)

if not warmup:
    raise Exception("Could not find Wix warmup data")

data = json.loads(warmup.string)

events = (
    data["appsWarmupData"]
    ["140603ad-af8d-84a5-2c80-a0f60cb47351"]
    ["widgetcomp-j9ny0yyr"]
    ["events"]
    ["events"]
)

events = sorted(
    events,
    key=lambda x: x["scheduling"]["config"]["startDate"]
)

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = (
    "New Hampshire Underground Shows"
)

ET.SubElement(channel, "link").text = URL

ET.SubElement(channel, "description").text = (
    "Upcoming shows and events"
)


for event in events:

    item = ET.SubElement(channel, "item")

    ET.SubElement(item, "title").text = event["title"]

    ET.SubElement(item, "description").text = (
        event.get("description", "")
    )

    start = event["scheduling"]["config"]["startDate"]

    dt = datetime.fromisoformat(
        start.replace("Z", "+00:00")
    )

    ET.SubElement(item, "pubDate").text = (
        format_datetime(dt)
    )

    ET.SubElement(item, "link").text = (
        URL + "/" + event["slug"]
    )

    ET.SubElement(item, "guid").text = event["slug"]


tree = ET.ElementTree(rss)

tree.write(
    "feed.xml",
    encoding="utf-8",
    xml_declaration=True
)

print(f"Generated feed with {len(events)} events")

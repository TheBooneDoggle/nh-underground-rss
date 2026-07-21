from datetime import datetime, timezone

# Feed settings
FEED_TITLE = "My RSS Feed"
FEED_LINK = "https://YOUR-GITHUB-USERNAME.github.io/YOUR-REPOSITORY/feed.xml"
FEED_DESCRIPTION = "Automatically generated RSS feed"

# Example feed item
items = [
    {
        "title": "Feed Generator Test",
        "description": "This RSS feed is now generated automatically using GitHub Actions.",
        "link": FEED_LINK,
    }
]

# Build RSS items
rss_items = ""

for item in items:
    rss_items += f"""
    <item>
        <title>{item['title']}</title>
        <description>{item['description']}</description>
        <link>{item['link']}</link>
        <pubDate>{datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")}</pubDate>
    </item>
    """

# Build RSS feed
feed_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>

<title>{FEED_TITLE}</title>
<link>{FEED_LINK}</link>
<description>{FEED_DESCRIPTION}</description>

{rss_items}

</channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as file:
    file.write(feed_content)

print("feed.xml generated successfully")

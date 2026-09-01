import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime


def fetch_google_news(query: str, limit: int = 5):
    q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={q}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read()

    root = ET.fromstring(data)
    items = []
    for item in root.findall("./channel/item")[:limit]:
        title = item.findtext("title", default="(no title)").strip()
        link = item.findtext("link", default="").strip()
        pub_date = item.findtext("pubDate", default="").strip()
        items.append({"title": title, "link": link, "pub_date": pub_date})
    return items


def main():
    symbols = os.getenv("STOCKS", "300059").split(",")
    symbols = [s.strip() for s in symbols if s.strip()]
    per_stock = int(os.getenv("NEWS_PER_STOCK", "5"))

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [f"Daily Stock News Report", f"Generated: {now}", ""]

    for s in symbols:
        query = f"{s} 股票 OR {s} stock"
        lines.append(f"=== {s} ===")
        try:
            news = fetch_google_news(query, per_stock)
            if not news:
                lines.append("No news found.")
            else:
                for i, n in enumerate(news, 1):
                    lines.append(f"{i}. {n['title']}")
                    lines.append(f"   {n['pub_date']}")
                    lines.append(f"   {n['link']}")
        except Exception as e:
            lines.append(f"Failed to fetch news: {e}")
        lines.append("")

    with open("daily_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Report generated: daily_report.txt")


if __name__ == "__main__":
    main()

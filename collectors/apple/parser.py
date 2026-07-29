import re
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def parse_sample(sample_path=None):
    if sample_path is None:
        sample_dir = os.path.join(BASE_DIR, "..", "..", "survey", "samples")
        html_files = [f for f in os.listdir(sample_dir) if f.startswith("Apple_Refurb") and f.endswith(".html")]
        if not html_files:
            print("❌ 没有找到 Apple 翻新样本文件")
            return []
        html_files.sort(reverse=True)
        sample_path = os.path.join(sample_dir, html_files[0])

    print(f"📂 解析样本: {sample_path}")

    with open(sample_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    items = []

    price_divs = soup.find_all("div", class_="as-price-currentprice")
    for div in price_divs:
        parent = div.find_parent("li")
        if not parent:
            parent = div.find_parent("div", class_=re.compile("product"))
        if not parent:
            continue

        title_tag = parent.find("h3")
        if not title_tag:
            title_tag = parent.find("a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)

        link_tag = parent.find("a", href=True)
        link = ""
        if link_tag:
            link = link_tag["href"]
            if link.startswith("/"):
                link = "https://www.apple.com.cn" + link

        price_text = div.get_text(strip=True)
        price_match = re.search(r"[\d,]+", price_text)
        price = 0
        if price_match:
            price = float(price_match.group().replace(",", ""))

        title_lower = title.lower()
        if "iphone" in title_lower:
            category = "iphone"
        elif "macbook" in title_lower or "imac" in title_lower or "mac mini" in title_lower or "mac pro" in title_lower:
            category = "mac"
        elif "ipad" in title_lower:
            category = "ipad"
        elif "watch" in title_lower:
            category = "watch"
        elif "airpods" in title_lower:
            category = "airpods"
        elif "studio display" in title_lower or "pro display" in title_lower:
            category = "display"
        else:
            category = "other"

        capacity_match = re.search(r"(\d+GB|\d+TB)", title, re.IGNORECASE)
        capacity = capacity_match.group(0) if capacity_match else ""

        item = {
            "platform": "apple",
            "category": category,
            "model": title,
            "capacity": capacity,
            "condition": "官翻",
            "price": price,
            "currency": "CNY",
            "stock": True,
            "url": link,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "raw": {"title": title, "price_text": price_text}
        }
        items.append(item)

    print(f"✅ 解析完成，共提取 {len(items)} 个商品")
    return items

if __name__ == "__main__":
    items = parse_sample()
    for i, item in enumerate(items):
        print(f"--- 商品 {i+1} ---")
        print(f"  名称: {item['model']}")
        print(f"  价格: ¥{item['price']:,.0f}")
        print(f"  链接: {item['url']}")
    output_dir = os.path.join(BASE_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "parsed_items.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"📁 结果已保存到 collectors/apple/output/parsed_items.json")

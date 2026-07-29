import requests
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DIR = os.path.join(BASE_DIR, "samples")
RESULT_FILE = os.path.join(BASE_DIR, "results.csv")

BLOCK_WORDS = [
    "验证码", "访问异常", "Cloudflare",
    "captcha", "verify", "security check", "robot"
]

def probe(name: str, url: str, params=None, headers=None, timeout=15):
    default_headers = {"User-Agent": "Mozilla/5.0 (compatible; AppleScout-Survey/2.0)"}
    if headers:
        default_headers.update(headers)

    print("=" * 60)
    print(f"Probe: {name}")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Size        : {size} bytes")
print(f"Elapsed     : {elapsed:.2f}s")
print(f"Final URL   : {resp.url}")
print(f"History     : {len(resp.history)} redirects")

    try:
        resp = requests.get(url, params=params, headers=default_headers, timeout=timeout)
        status = resp.status_code
        content_type = resp.headers.get("Content-Type", "")
        size = len(resp.content)
        elapsed = resp.elapsed.total_seconds()
        text = resp.text

        print(f"HTTP        : {status}")
        print(f"ContentType : {content_type}")
        print(f"Size        : {size} bytes")
        print(f"Elapsed     : {elapsed:.2f}s")

        blocked = any(kw.lower() in text.lower() for kw in BLOCK_WORDS)
        empty = (len(text.strip()) == 0)
        print(f"Blocked     : {blocked}")
        print(f"Empty       : {empty}")

        os.makedirs(SAMPLE_DIR, exist_ok=True)

        ext = content_type.split("/")[-1].split(";")[0] or "txt"
        if ext not in ("html", "json", "xml", "txt"):
            ext = "txt"
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name.replace(' ', '_')}_{timestamp_str}.{ext}"
        filepath = os.path.join(SAMPLE_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved       : {filepath}")

        if not os.path.exists(RESULT_FILE):
            with open(RESULT_FILE, "w", encoding="utf-8-sig") as f:
                f.write("time,source,status,content_type,size,result,note\n")

        success = (status == 200) and (not blocked) and (not empty)
        result = "✅" if success else "❌"
        print(f"\nResult      : {'PASS' if success else 'FAIL'}")

        with open(RESULT_FILE, "a", encoding="utf-8-sig") as log:
            note = "blocked" if blocked else ""
            log.write(f"{timestamp_str},{name},{status},{content_type},{size},{result},{note}\n")
        return success

    except Exception as e:
        print(f"Probe failed: {e}")
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(SAMPLE_DIR, exist_ok=True)
        if not os.path.exists(RESULT_FILE):
            with open(RESULT_FILE, "w", encoding="utf-8-sig") as f:
                f.write("time,source,status,content_type,size,result,note\n")
        with open(RESULT_FILE, "a", encoding="utf-8-sig") as log:
            log.write(f"{timestamp_str},{name},ERROR,,,❌,{str(e)}\n")
        return False

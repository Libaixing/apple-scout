import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from probe_base import probe

# 什么值得买 RSS 订阅
URL = "https://feed.smzdm.com/"
PARAMS = {
    "feed": "search",
    "s": "苹果",
    "p": "1"
}

if __name__ == "__main__":
    probe("SMZDM_RSS", URL, params=PARAMS)

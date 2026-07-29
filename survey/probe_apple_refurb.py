import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from probe_base import probe

# Apple 中国官网 iPhone 翻新专区
URL = "https://www.apple.com.cn/shop/refurbished/iphone"

if __name__ == "__main__":
    probe("Apple_Refurb_iPhone", URL)

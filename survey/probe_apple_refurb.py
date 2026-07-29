import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from probe_base import probe

# Apple 中国官网翻新接口（常见路径）
URL = "https://www.apple.com.cn/shop/refurbished/mac/"

if __name__ == "__main__":
    probe("Apple_Refurb_Mac", URL)

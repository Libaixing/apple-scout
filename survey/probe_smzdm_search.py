import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from probe_base import probe

URL = "https://search.smzdm.com/"
PARAMS = {
    "c": "home",
    "s": "苹果",
    "order": "time",
    "p": "1",
    "v": "b"
}

if __name__ == "__main__":
    probe("SMZDM_Search", URL, params=PARAMS)

# -*- coding: utf-8 -*-
"""Server funksiyasi uchun narxlar: api/_prices.json. python3 -I api_data.py <foto_dir> <repo_root>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog_data import *
load(sys.argv[1])
out = {p["key"]: {"name": p["name_uz"], "pack": p["pack_uz"], "price": p["price"]} for p in PRODUCTS}
path = os.path.join(sys.argv[2], "api", "_prices.json")
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("api/_prices.json:", ", ".join(f"{k}={v['price']}" for k, v in out.items()))

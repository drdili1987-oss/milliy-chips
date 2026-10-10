# -*- coding: utf-8 -*-
"""Qidiruv tizimlari va ijtimoiy tarmoqlar uchun fayllar (repo ildiziga yoziladi):
robots.txt, sitemap.xml, favicon.svg, apple-touch-icon.png, og.jpg (1200x630).
python3 -I seo.py <foto_dir> <repo_root>
"""
import datetime, os, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog_data import *
from PIL import Image

load(sys.argv[1])
ROOT = os.path.abspath(sys.argv[2])
HERE = os.path.dirname(os.path.abspath(__file__))
today = datetime.date.today().isoformat()

# robots.txt + sitemap.xml
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
urls = [(f"{SITE_URL}/", "1.0"), (f"{SITE_URL}/katalog", "0.8"), (f"{SITE_URL}/katalog/Milliy-Chips-katalog.pdf", "0.5")]
open(os.path.join(ROOT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls)
    + "</urlset>\n")

# favicon (asl vektor logo)
shutil.copy(os.path.join(HERE, "logo.svg"), os.path.join(ROOT, "favicon.svg"))

# og.jpg va apple-touch-icon.png — Chromium orqali, sayt shriftlari bilan
hero = Image.open(os.path.join(sys.argv[1], PRODUCTS[0]["photos"][0])).convert("RGB")
side = min(hero.size)
hero = hero.crop(((hero.width - side) // 2, (hero.height - side) // 2, (hero.width + side) // 2, (hero.height + side) // 2))
hero = hero.resize((630, 630), Image.LANCZOS)
tmp = tempfile.mkdtemp()
hero.save(os.path.join(tmp, "hero.jpg"), quality=90)
shutil.copy(os.path.join(HERE, "logo.svg"), os.path.join(tmp, "logo.svg"))

og_html = f"""<!doctype html><meta charset="utf-8"><style>{font_faces()}
html,body{{margin:0}}
.og{{width:1200px;height:630px;display:flex;background:#2A1233;color:#fff;font-family:Manrope,sans-serif;overflow:hidden;
  background-image:radial-gradient(80% 90% at 0% 0%,#45204F,transparent 60%)}}
.t{{flex:1;padding:56px 52px;display:flex;flex-direction:column;gap:22px}}
.logo{{width:120px;height:120px;border-radius:50%;box-shadow:0 0 0 6px #FFC52E}}
h1{{font-family:Unbounded,sans-serif;font-weight:800;font-size:66px;line-height:1;margin:6px 0 0}}
h1 em{{font-style:normal;color:#FFC52E}}
p{{margin:0;font-size:27px;color:#CDB9D3;font-weight:600}}
.ph{{margin-top:auto;font-family:Unbounded,sans-serif;font-weight:800;font-size:36px;color:#FFC52E}}
.img{{width:630px;height:630px;background:url(hero.jpg) center/cover}}
.icon{{width:180px;height:180px;background:#fff;display:flex;align-items:center;justify-content:center}}
.icon img{{width:170px;height:170px}}
</style>
<div class="og" id="og"><div class="t"><img class="logo" src="logo.svg" alt="">
<h1>Milliy <em>Chips</em></h1><p>Eng mazali chipslar · 4 xil ta'm<br>Do'konlar uchun ulgurji narxlar</p>
<div class="ph">{PHONE}</div></div><div class="img"></div></div>
<div class="icon" id="icon"><img src="logo.svg" alt=""></div>"""
open(os.path.join(tmp, "og.html"), "w", encoding="utf-8").write(og_html)

js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: 1200, height: 900 }} }});
  await p.goto('file://{tmp}/og.html'); await p.evaluate(() => document.fonts.ready);
  await (await p.$('#og')).screenshot({{ path: '{ROOT}/og.jpg', type: 'jpeg', quality: 86 }});
  await (await p.$('#icon')).screenshot({{ path: '{ROOT}/apple-touch-icon.png' }});
  await b.close();
}})();"""
subprocess.run(["node", "-e", js], cwd=HERE, check=True)
shutil.rmtree(tmp)
print("SEO fayllari:", ", ".join(f for f in ("robots.txt", "sitemap.xml", "favicon.svg", "apple-touch-icon.png", "og.jpg")))

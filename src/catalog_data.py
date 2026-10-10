# -*- coding: utf-8 -*-
"""Milliy Chips: umumiy ma'lumotlar (mahsulotlar, narxlar, rasmlar, shriftlar, logo).
Katalog (build.py) va sayt (site.py) shu moduldan foydalanadi. Avval load(foto_dir) chaqiriladi.
"""
import base64, io, os, re, sys
from PIL import Image

FOTO = None
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_modules/@fontsource")
PHONE = "+998 (33) 100 17 11"
PRICE_DATE = "2026-yil oktabr"

# ---------------------------------------------------------------- narxni fayl nomidan olish
PRICE_RE = re.compile(r"^\s*(\d{2})[ .,]?(\d{3})")

def price_from_name(fn):
    m = PRICE_RE.match(fn)
    return int(m.group(1) + m.group(2)) if m else None

# ---------------------------------------------------------------- mahsulotlar
PRODUCTS = [
    dict(
        key="milliy", brand="Milliy Chips", name_uz="Milliy Chips", name_ru="Картофельные чипсы",
        tag_uz="Eng mazali chipslar", tag_ru="Самые вкусные чипсы",
        pack_uz="900 g quti", pack_ru="коробка 900 г", unit=("kg", 0.9),
        photos=["46,000, 900gr.jpg", "46 000, 900gr.jpg", "46.000, 900gr.jpg", "46.000. 900 gr.jpg"],
        color="#5B2A6E", on="#FFFFFF",
        desc_uz="O'zbekiston me'moriy obidalari tushirilgan chiroyli qutida — do'kon peshtaxtasida darhol ko'zga tashlanadi. "
                "Yupqa, qarsildoq kartoshka chipslari to'rt xil ta'mda.",
        desc_ru="Яркая коробка с видами Самарканда и Бухары сразу заметна на витрине. "
                "Тонкие хрустящие картофельные чипсы в четырёх вкусах.",
        flavors=[("Smetana va ko'katlar", "Сметана и зелень", "#5FA829"),
                 ("Shashlik", "Сочный шашлык", "#8A3A1A"),
                 ("Salyami", "Сочная салями", "#B0306A"),
                 ("Pishloq", "Сырные чипсы", "#E9B21E")],
    ),
    dict(
        key="5dbag", brand="5D Chips", name_uz="5D Chips 20 g", name_ru="Чипсы 5D, пакет 20 г",
        tag_uz="Yengil va qarsildoq", tag_ru="Лёгкие и хрустящие",
        pack_uz="Blok: 60 dona × 20 g", pack_ru="блок 60 шт × 20 г", unit=("dona", 60),
        photos=["34,000. 60 ta dona.jpg", "34.000 som 60ta dona.jpg"],
        color="#16161A", on="#FFC52E",
        desc_uz="Shashlik va pomidor ta'midagi kichik paket. Narxi arzon, kassa oldida tez sotiladi — "
                "maktab yonidagi va mahalla do'konlari uchun ideal.",
        desc_ru="Небольшой пакет со вкусом шашлыка и томата. Доступная цена, быстро уходит с прикассовой зоны.",
        flavors=[("Shashlik va pomidor", "Шашлык и томат", "#C8372D"), ("GMOsiz", "Без ГМО", "#3E8E3A")],
    ),
    dict(
        key="5dbox", brand="5D", name_uz="5D vaznli chips", name_ru="Чипсы 5D на развес",
        tag_uz="Eng mazali chipslar", tag_ru="Самые вкусные чипсы",
        pack_uz="2 kg quti", pack_ru="коробка 2 кг", unit=("kg", 2),
        photos=["35.000. 2 kg.jpg", "35 000. 2 kg.jpg"], pos="50% 62%",
        color="#23388F", on="#FFFFFF",
        desc_uz="Katta qutida vaznli chips — tortib sotish uchun qulay. Kilogrammiga hisoblaganda "
                "eng tejamkor variantlardan biri.",
        desc_ru="Весовые чипсы в большой коробке — удобно продавать на развес. Один из самых выгодных вариантов за килограмм.",
        flavors=[("Halol", "Халяль", "#23388F")],
    ),
    dict(
        key="kan", brand="KAN corporation", name_uz="KAN tayoqchalari", name_ru="Хлебные палочки KAN",
        tag_uz="Eng mazali tayoqchalar", tag_ru="Самые вкусные палочки",
        pack_uz="2 kg quti", pack_ru="коробка 2 кг", unit=("kg", 2),
        photos=["33 000, 2 kg.jpg", "33 000. 2 kg.jpg", "photo_2025-06-02_12-11-07.jpg"],
        color="#178F8C", on="#FFFFFF",
        desc_uz="Bug'doy unidan tayyorlangan qarsildoq tayoqchalar. Vaznli savdo uchun 2 kg qutida — "
                "choy va suhbatga eng yaxshi hamroh.",
        desc_ru="Хрустящие палочки из пшеничной муки. Коробка 2 кг для продажи на развес — к чаю и для компании.",
        flavors=[("Halol", "Халяль", "#178F8C"), ("Best quality", "Лучшее качество", "#C99A16")],
    ),
]

# ---------------------------------------------------------------- tekshiruv: narxlar fayl nomlaridan
def load(foto_dir):
    global FOTO
    FOTO = foto_dir
    all_files = sorted(f for f in os.listdir(FOTO) if f.lower().endswith((".jpg", ".jpeg", ".png")))
    used = set()
    for p in PRODUCTS:
        prices = {price_from_name(f) for f in p["photos"]} - {None}
        if len(prices) != 1:
            sys.exit(f"{p['key']}: narxlar mos emas yoki topilmadi: {prices}")
        p["price"] = prices.pop()
        for f in p["photos"]:
            if f not in all_files:
                sys.exit(f"Fayl topilmadi: {f}")
            used.add(f)
    unused = [f for f in all_files if f not in used]
    if unused:
        print("DIQQAT: katalogga kirmagan rasmlar:", unused, file=sys.stderr)

    return PRODUCTS

# ---------------------------------------------------------------- yordamchilar
def money(n):
    return f"{n:,}".replace(",", " ")

def unit_price(p):
    u, q = p["unit"]
    v = p["price"] / q
    approx = abs(v - round(v)) > 1e-9
    return ("≈ " if approx else "") + money(round(v)) + f" so'm/{u}"

_img_cache = {}
def img(fn, maxside=1200, q=80):
    k = (fn, maxside)
    if k not in _img_cache:
        im = Image.open(os.path.join(FOTO, fn)).convert("RGB")
        im.thumbnail((maxside, maxside), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True, progressive=True)
        _img_cache[k] = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    return _img_cache[k]

def font_faces():
    css = []
    for fam, pkg, weights in (("Unbounded", "unbounded", (600, 800)), ("Manrope", "manrope", (400, 600, 800))):
        for w in weights:
            for sub, rng in (("cyrillic", "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116"),
                             ("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")):
                path = os.path.join(FONTS, pkg, "files", f"{pkg}-{sub}-{w}-normal.woff2")
                data = base64.b64encode(open(path, "rb").read()).decode()
                css.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;"
                           f"src:url(data:font/woff2;base64,{data}) format('woff2');unicode-range:{rng}}}")
    return "\n".join(css)

LOGO = "data:image/svg+xml;base64," + base64.b64encode(
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.svg"), "rb").read()).decode()

def logo(cls=""):
    return f'<img class="logo {cls}" src="{LOGO}" alt="Milliy Chips">'

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# -*- coding: utf-8 -*-
"""Milliy Chips katalogi (A4). python3 -I build.py <foto_dir> <out.html>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog_data import *
load(sys.argv[1])
OUT = sys.argv[2]

# ---------------------------------------------------------------- sahifalar
def cover():
    chips = "".join(
        f'<li><span class="dot" style="background:{p["color"]}"></span><b>{esc(p["name_uz"])}</b>'
        f'<span class="cprice">{money(p["price"])} <small>so\'m</small></span></li>' for p in PRODUCTS)
    return f"""
<section class="page cover">
  <header class="brandrow">
    {logo("on-dark")}
    <div class="maker">KAN corporation</div>
  </header>
  <div class="cover-title">
    <p class="eyebrow">Do'konlar va mijozlar uchun · Для магазинов и покупателей</p>
    <h1>Mahsulot<br>katalogi</h1>
    <p class="ru-sub">Каталог продукции · {PRICE_DATE}</p>
  </div>
  <figure class="hero"><img src="{img(PRODUCTS[0]['photos'][0], 1400)}" alt="Milliy Chips qutilari"></figure>
  <ul class="cover-list">{chips}</ul>
  <footer class="cover-foot">
    <span>Buyurtma · Заказ</span><strong>{PHONE}</strong>
  </footer>
</section>"""

def price_list():
    rows = ""
    for i, p in enumerate(PRODUCTS, 1):
        rows += f"""
    <tr>
      <td class="th"><img src="{img(p['photos'][0], 400)}" alt=""></td>
      <td><b>{esc(p['name_uz'])}</b><span class="ru">{esc(p['name_ru'])}</span></td>
      <td>{esc(p['pack_uz'])}<span class="ru">{esc(p['pack_ru'])}</span></td>
      <td class="num unit">{unit_price(p)}</td>
      <td class="num price">{money(p['price'])}<small>so'm</small></td>
    </tr>"""
    return f"""
<section class="page plist">
  <header class="phead">
    <div><p class="eyebrow dark">Narxlar ro'yxati · Прайс-лист</p>
    <h2>Barcha mahsulotlar bir sahifada</h2></div>
    {logo("small")}
  </header>
  <div class="tablewrap">
  <table>
    <thead><tr><th></th><th>Mahsulot<span class="ru">Товар</span></th><th>Qadoq<span class="ru">Упаковка</span></th>
      <th class="num">Birlik narxi<span class="ru">За единицу</span></th><th class="num">Narxi<span class="ru">Цена</span></th></tr></thead>
    <tbody>{rows}
    </tbody>
  </table>
  </div>
  <p class="note">Narxlar bitta qadoq (quti yoki blok) uchun, {PRICE_DATE} holatiga. Birlik narxi ma'lumot uchun hisoblangan.<br>
  <span class="ru">Цены указаны за одну упаковку (коробку или блок). Цена за единицу рассчитана для справки.</span></p>
  <div class="flavor-strip">
    <p class="eyebrow dark">Milliy Chips ta'mlari · Вкусы</p>
    <ul>{''.join(f'<li style="--c:{c}"><b>{esc(u)}</b><span>{esc(r)}</span></li>' for u, r, c in PRODUCTS[0]['flavors'])}</ul>
  </div>
  <aside class="callbar"><span>Buyurtma berish uchun qo'ng'iroq qiling<br><span class="ru">Звоните для заказа</span></span><strong>{PHONE}</strong></aside>
</section>"""

def product_page(p, idx):
    main, *rest = p["photos"]
    thumbs = "".join(f'<figure><img src="{img(f, 900)}" alt="" style="object-position:{p.get("pos","50% 50%")}"></figure>' for f in rest)
    if len(rest) == 1:
        u, q = p["unit"]
        thumbs += (f'<div class="kgtile"><span>1 {u} narxi · цена за 1 {"кг" if u == "kg" else "шт"}</span>'
                   f'<b>{money(round(p["price"] / q))}</b><small>so\'m · {esc(p["pack_uz"])} = {money(p["price"])} so\'m</small></div>')
    tags = "".join(f'<li style="--c:{c}"><b>{esc(u)}</b><span>{esc(r)}</span></li>' for u, r, c in p["flavors"])
    return f"""
<section class="page product" style="--pc:{p['color']};--on:{p['on']}">
  <header class="pband">
    <span class="pbrand">{esc(p['brand'])}</span>
    <span class="pidx">{idx} / {len(PRODUCTS)}</span>
  </header>
  <figure class="pmain"><img src="{img(main, 1400)}" alt="{esc(p['name_uz'])}">{logo("on-photo") if p["key"] == "milliy" else ""}
    <div class="badge"><span class="bnum">{money(p['price'])}</span><span class="bcur">so'm</span><span class="bpack">{esc(p['pack_uz'])}</span></div>
  </figure>
  <div class="pbody">
    <div class="ptext">
      <p class="eyebrow dark">{esc(p['tag_uz'])} · {esc(p['tag_ru'])}</p>
      <h2>{esc(p['name_uz'])}</h2>
      <p class="ru-name">{esc(p['name_ru'])}</p>
      <p class="desc">{esc(p['desc_uz'])}</p>
      <p class="desc ru">{esc(p['desc_ru'])}</p>
      <ul class="tags">{tags}</ul>
    </div>
    <dl class="specs">
      <div><dt>Narxi · Цена</dt><dd class="big">{money(p['price'])} so'm</dd></div>
      <div><dt>Qadoq · Упаковка</dt><dd>{esc(p['pack_uz'])}<span class="ru">{esc(p['pack_ru'])}</span></dd></div>
      <div><dt>Birlik narxi · За единицу</dt><dd>{unit_price(p)}</dd></div>
    </dl>
  </div>
  <div class="pthumbs n{len(rest)}">{thumbs}</div>
  <footer class="pfoot"><span>Buyurtma · Заказ</span><strong>{PHONE}</strong></footer>
</section>"""

def back():
    return f"""
<section class="page back">
  {logo("on-dark big")}
  <div class="back-main">
    <p class="eyebrow">Hamkorlikka taklif qilamiz · Приглашаем к сотрудничеству</p>
    <h2>Do'koningiz peshtaxtasi uchun buyurtma bering</h2>
    <p class="ru-sub">Оформите заказ для своего магазина</p>
    <div class="phone-big">{PHONE}</div>
  </div>
  <div class="back-grid">{''.join(f'<figure><img src="{img(p["photos"][0], 700)}" alt=""><figcaption>{esc(p["name_uz"])}<b>{money(p["price"])} so\'m</b></figcaption></figure>' for p in PRODUCTS)}</div>
  <p class="maker">KAN corporation · {PRICE_DATE}</p>
</section>"""

CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog.css"), encoding="utf-8").read()

html = f"""<title>Milliy Chips katalogi</title>
<style>
{font_faces()}
{CSS}
</style>
<main class="book">
{cover()}
{price_list()}
{''.join(product_page(p, i) for i, p in enumerate(PRODUCTS, 1))}
{back()}
</main>
"""
open(OUT, "w", encoding="utf-8").write(html)
for p in PRODUCTS:
    print(f"{p['name_uz']:<20} {money(p['price']):>8} so'm  {p['pack_uz']:<22} {unit_price(p)}")
print(f"OK -> {OUT} ({os.path.getsize(OUT)/1e6:.1f} MB)")

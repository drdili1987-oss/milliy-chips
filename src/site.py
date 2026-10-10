# -*- coding: utf-8 -*-
"""Milliy Chips sayti (bitta HTML fayl). python3 -I site.py <foto_dir> <out.html>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog_data import *
load(sys.argv[1])
OUT = sys.argv[2]

PHONE_DIGITS = "+" + "".join(c for c in PHONE if c.isdigit())   # +998331001711
TG_LINK = f"https://t.me/{PHONE_DIGITS}"
UNIT_RU = {"kg": "кг", "dona": "шт"}
# Ruscha nomda brend yo'q bo'lsa, saytda brend nomi ishlatiladi
RU_TITLE = {"milliy": "Milliy Chips"}


def L(uz, ru, tag="span", cls=""):
    """Ikki tilli matn: faqat tanlangan til ko'rinadi (CSS orqali)."""
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-l="uz">{esc(uz)}</{tag}><{tag}{c} data-l="ru">{esc(ru)}</{tag}>'


def unit_l(p):
    u, q = p["unit"]
    v = p["price"] / q
    pre = "≈ " if abs(v - round(v)) > 1e-9 else ""
    return L(f"{pre}{money(round(v))} so'm/{u}", f"{pre}{money(round(v))} сум/{UNIT_RU[u]}")


def stepper(key, where):
    return (f'<div class="stepper" data-key="{key}">'
            f'<button type="button" class="st-btn" data-d="-1" aria-label="Kamaytirish">−</button>'
            f'<input id="q-{where}-{key}" class="st-in" type="number" inputmode="numeric" min="0" max="999" value="0" aria-label="Soni">'
            f'<button type="button" class="st-btn" data-d="1" aria-label="Ko\'paytirish">+</button></div>')


def product_block(p, i):
    gal = "".join(
        f'<button type="button" class="thumb{" on" if j == 0 else ""}" data-src="{img(f, 1200)}" aria-label="Rasm {j + 1}">'
        f'<img src="{img(f, 320)}" alt=""></button>' for j, f in enumerate(p["photos"]))
    flav = "".join(f'<li><span class="fdot" style="background:{c}"></span>{L(u, r)}</li>' for u, r, c in p["flavors"])
    return f"""
<article class="prod" id="p-{p['key']}" style="--pc:{p['color']}">
  <div class="gallery">
    <figure class="gmain"><img src="{img(p['photos'][0], 1200)}" alt="{esc(p['name_uz'])}">
      {logo('gl') if p['key'] == 'milliy' else ''}
    </figure>
    <div class="thumbs">{gal}</div>
  </div>
  <div class="pinfo">
    <span class="pill">{esc(p['brand'])}</span>
    <h3>{L(p['name_uz'], RU_TITLE.get(p['key'], p['name_ru']))}</h3>
    <p class="ptag">{L(p['tag_uz'], p['tag_ru'])}</p>
    <p class="pdesc">{L(p['desc_uz'], p['desc_ru'])}</p>
    <ul class="flav">{flav}</ul>
    <div class="pricebox">
      <div class="pb-main"><span class="pb-num">{money(p['price'])}</span> {L("so'm", "сум", cls="pb-cur")}</div>
      <div class="pb-meta"><b>{L(p['pack_uz'], p['pack_ru'])}</b><span>{unit_l(p)}</span></div>
    </div>
    <div class="addrow">
      <span class="addlbl">{L("Buyurtmaga qo'shish", "Добавить в заказ")}</span>
      {stepper(p['key'], 'p')}
      <a class="tolink" href="#buyurtma">{L("Buyurtmaga o'tish ↓", "К заказу ↓")}</a>
    </div>
  </div>
</article>"""


def price_rows():
    return "".join(f"""
      <tr><td><a href="#p-{p['key']}" class="trow"><img src="{img(p['photos'][0], 160)}" alt=""><span><b>{L(p['name_uz'], RU_TITLE.get(p['key'], p['name_ru']))}</b></span></a></td>
        <td>{L(p['pack_uz'], p['pack_ru'])}</td><td class="num muted">{unit_l(p)}</td>
        <td class="num strong">{money(p['price'])} {L("so'm", "сум")}</td></tr>""" for p in PRODUCTS)


def order_rows():
    return "".join(f"""
      <li class="oline" data-key="{p['key']}">
        <img src="{img(p['photos'][0], 160)}" alt="">
        <div class="on-name"><b>{L(p['name_uz'], RU_TITLE.get(p['key'], p['name_ru']))}</b><span>{L(p['pack_uz'], p['pack_ru'])} · {money(p['price'])} {L("so'm", "сум")}</span></div>
        {stepper(p['key'], 'o')}
        <output class="on-sum" for="q-o-{p['key']}">0</output>
      </li>""" for p in PRODUCTS)


# Bosh rasm Milliy Chips — belgida aynan shu mahsulot narxi ko'rsatiladi (eng arzon narx emas)
HERO = PRODUCTS[0]
HERO_W = round(HERO['unit'][1] * 1000)   # 0.9 kg -> 900
flavors_all = []
for p in PRODUCTS:
    for u, r, _ in p["flavors"]:
        if (u, r) not in flavors_all:
            flavors_all.append((u, r))
marquee_items = "".join(f"<li>{L(u, r)}</li>" for u, r in flavors_all)

JS_DATA = json.dumps({p["key"]: dict(price=p["price"], uz=f"{p['name_uz']} ({p['pack_uz']})",
                                     ru=f"{RU_TITLE.get(p['key'], p['name_ru'])} ({p['pack_ru']})") for p in PRODUCTS}, ensure_ascii=False)

CSS = r"""
/* Layout: to'liq kenglikdagi bo'limlar, ichida 1180px .wrap; mahsulotlar navbatma-navbat (rasm | ma'lumot). Brend ranglari, bitta yorug' ko'rinish. */
:root{
  --plum:#2A1233; --plum-2:#45204F; --saffron:#FFC52E; --chili:#E5412D;
  --paper:#FFFFFF; --mist:#F6F1F7; --ink:#1F1024; --muted:#6E5D73; --line:#E8DFEA; --night:#170A1C; --lilac:#CDB9D3;
  --display:'Unbounded','Arial Black',system-ui,sans-serif;
  --body:'Manrope','Segoe UI',system-ui,sans-serif;
  color-scheme:light;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth;scroll-padding-top:calc(76px + env(safe-area-inset-top,0px))}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55}
html[lang="uz"] [data-l="ru"],html[lang="ru"] [data-l="uz"]{display:none}
img{display:block;max-width:100%}
a{color:inherit}
h1,h2,h3{font-family:var(--display);font-weight:800;margin:0;letter-spacing:-.015em;text-wrap:balance;line-height:1.08}
.wrap{max-width:1180px;margin:0 auto;padding-inline:clamp(16px,4vw,40px)}
.eyebrow{margin:0 0 14px;font-size:.78rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--chili)}
:focus-visible{outline:3px solid var(--saffron);outline-offset:2px}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:0 22px;border-radius:999px;border:0;
  font:800 1rem var(--body);text-decoration:none;cursor:pointer;transition:transform .15s ease,background .15s ease}
.btn:hover{transform:translateY(-1px)}
.btn-y{background:var(--saffron);color:var(--plum)}
.btn-ghost{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.35)}
.btn-ghost:hover{box-shadow:inset 0 0 0 2px var(--saffron)}
.btn[disabled]{opacity:.45;cursor:not-allowed;transform:none}

/* header */
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;gap:20px;height:68px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-family:var(--display);font-weight:800;font-size:1.05rem;color:var(--plum)}
.brand .logo{width:46px;height:46px}
.nav{display:flex;gap:26px;margin-left:auto}
.nav a{text-decoration:none;font-weight:600;color:var(--muted)}
.nav a:hover{color:var(--plum)}
.lang{display:flex;border-radius:999px;background:var(--mist);padding:3px}
.lang button{border:0;background:transparent;font:800 .8rem var(--body);padding:7px 11px;border-radius:999px;cursor:pointer;color:var(--muted)}
.lang button[aria-pressed="true"]{background:var(--plum);color:#fff}
.top .btn{min-height:40px;padding:0 16px;font-size:.9rem;background:var(--plum);color:var(--saffron)}
.logo{border-radius:50%;object-fit:contain}

/* hero */
.hero{background:var(--plum);color:#fff;background-image:radial-gradient(90% 70% at 100% 0%,var(--plum-2),transparent 60%);overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1.05fr 1fr;gap:clamp(28px,5vw,64px);align-items:center;padding-block:clamp(40px,7vw,88px)}
.hero h1{font-size:clamp(2.1rem,5.2vw,4.1rem);color:#fff}
.hero h1 em{font-style:normal;color:var(--saffron)}
.hero .eyebrow{color:var(--saffron)}
.hero-sub{margin:20px 0 30px;font-size:1.12rem;color:var(--lilac);max-width:34em}
.hero-cta{display:flex;flex-wrap:wrap;gap:12px}
.hero-phone{margin-top:26px;font-size:.9rem;color:var(--lilac)}
.hero-phone b{display:block;font-family:var(--display);font-size:1.35rem;color:#fff;user-select:all}
.hero-art{position:relative}
.hero-art .hi{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:28px;box-shadow:0 30px 60px rgba(0,0,0,.35)}
.hero-art .logo{position:absolute;left:-14px;top:-14px;width:96px;height:96px;box-shadow:0 0 0 5px var(--saffron),0 10px 30px rgba(0,0,0,.4)}
.seal{position:absolute;right:-10px;bottom:-14px;width:136px;height:136px;border-radius:50%;background:var(--saffron);color:var(--plum);
  display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;line-height:1.1;transform:rotate(-9deg);
  box-shadow:0 14px 34px rgba(0,0,0,.35)}
.seal small{font-weight:800;font-size:.72rem;max-width:80%}
.seal b{font-family:var(--display);font-size:1.55rem}

/* marquee */
.band{background:var(--saffron);color:var(--plum);overflow:hidden;border-block:3px solid var(--plum)}
.band ul{display:flex;gap:0;margin:0;padding:14px 0;list-style:none;width:max-content;animation:run 38s linear infinite}
.band li{font-family:var(--display);font-weight:600;font-size:1.05rem;white-space:nowrap;padding-inline:22px;display:flex;align-items:center;gap:44px}
.band li::after{content:"";width:10px;height:10px;border-radius:50%;background:var(--chili)}
@keyframes run{to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.band ul{animation:none}html{scroll-behavior:auto}.btn{transition:none}}

/* products */
.sec{padding-block:clamp(56px,8vw,104px)}
.sec-head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(32px,5vw,56px)}
.sec-head h2{font-size:clamp(1.8rem,3.6vw,2.8rem);color:var(--plum)}
.sec-head p{margin:0;max-width:30em;color:var(--muted)}
.prods{display:flex;flex-direction:column;gap:clamp(56px,8vw,96px)}
.prod{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,64px);align-items:center}
.prod:nth-child(even) .gallery{order:2}
.gallery{min-width:0}
.gmain{margin:0;position:relative;aspect-ratio:1/1;border-radius:24px;overflow:hidden;background:var(--mist)}
.gmain>img{width:100%;height:100%;object-fit:cover}
.gmain .gl{position:absolute;left:16px;top:16px;width:72px;height:72px;box-shadow:0 0 0 4px #fff,0 6px 20px rgba(0,0,0,.35)}
.thumbs{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}
.thumb{width:72px;height:72px;padding:0;border:0;border-radius:14px;overflow:hidden;cursor:pointer;background:var(--mist);
  box-shadow:inset 0 0 0 0 transparent;opacity:.6;transition:opacity .15s}
.thumb img{width:100%;height:100%;object-fit:cover}
.thumb.on,.thumb:hover{opacity:1;outline:3px solid var(--pc);outline-offset:2px}
.pinfo{min-width:0}
.pill{display:inline-block;background:var(--pc);color:#fff;font-weight:800;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;padding:6px 12px;border-radius:999px}
.prod h3{font-size:clamp(1.7rem,3.2vw,2.5rem);color:var(--plum);margin-top:16px}
.ptag{margin:8px 0 0;font-weight:800;color:var(--chili)}
.pdesc{margin:14px 0 0;color:var(--muted);max-width:34em}
.flav{list-style:none;margin:18px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.flav li{display:flex;align-items:center;gap:8px;background:var(--mist);border-radius:999px;padding:7px 14px;font-weight:600;font-size:.9rem}
.fdot{width:10px;height:10px;border-radius:50%;flex:none}
.pricebox{display:flex;flex-wrap:wrap;align-items:center;gap:14px 28px;margin-top:26px;padding:20px 24px;border-radius:20px;background:var(--plum);color:#fff}
.pb-num{font-family:var(--display);font-weight:800;font-size:2.2rem;color:var(--saffron);font-variant-numeric:tabular-nums}
.pb-cur{font-weight:800;color:var(--lilac)}
.pb-meta{display:flex;flex-direction:column;font-size:.92rem;color:var(--lilac)}
.pb-meta b{color:#fff}
.addrow{display:flex;flex-wrap:wrap;align-items:center;gap:12px 16px;margin-top:18px}
.addlbl{font-weight:800}
.tolink{font-weight:700;color:var(--muted);text-decoration-color:var(--line);text-underline-offset:4px}
.stepper{display:inline-flex;align-items:center;border-radius:999px;background:var(--mist);padding:4px}
.st-btn{width:40px;height:40px;border-radius:50%;border:0;background:#fff;color:var(--plum);font:800 1.3rem var(--body);cursor:pointer;
  box-shadow:0 1px 3px rgba(42,18,51,.15)}
.st-btn:hover{background:var(--saffron)}
.st-in{width:56px;border:0;background:transparent;text-align:center;font:800 1.1rem var(--body);color:var(--ink);-moz-appearance:textfield;appearance:textfield}
.st-in::-webkit-outer-spin-button,.st-in::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.stepper.has .st-in{color:var(--chili)}

/* price table */
.prices{background:var(--mist)}
.tablewrap{overflow-x:auto;background:#fff;border-radius:24px;padding:8px 24px}
table{width:100%;border-collapse:collapse;min-width:560px}
th{text-align:left;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);padding:16px 12px;border-bottom:2px solid var(--plum)}
th.num{text-align:right}
td{padding:14px 12px;border-bottom:1px solid var(--line);vertical-align:middle}
tr:last-child td{border-bottom:0}
.trow{display:flex;align-items:center;gap:14px;text-decoration:none}
.trow img{width:56px;height:56px;border-radius:12px;object-fit:cover}
td.muted{color:var(--muted);font-size:.92rem}
td.strong{font-family:var(--display);font-weight:800;font-size:1.2rem;color:var(--plum)}
.pnote{margin:16px 0 0;font-size:.88rem;color:var(--muted)}

/* order */
.order{background:var(--plum);color:#fff;background-image:radial-gradient(80% 60% at 0% 100%,var(--plum-2),transparent 60%)}
.order .sec-head h2{color:#fff}
.order .sec-head p{color:var(--lilac)}
.order .eyebrow{color:var(--saffron)}
.ogrid{display:grid;grid-template-columns:1.15fr 1fr;gap:clamp(24px,4vw,48px);align-items:start}
.ocard{background:#fff;color:var(--ink);border-radius:24px;padding:clamp(18px,3vw,28px);min-width:0}
.ocard h3{font-size:1.15rem;color:var(--plum);margin-bottom:14px}
.olist{list-style:none;margin:0;padding:0}
.oline{display:grid;grid-template-columns:52px minmax(0,1fr) auto 104px;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid var(--line)}
.oline img{width:52px;height:52px;border-radius:12px;object-fit:cover}
.on-name{display:flex;flex-direction:column;min-width:0}
.on-name span{font-size:.85rem;color:var(--muted)}
.on-sum{text-align:right;font-weight:800;font-variant-numeric:tabular-nums}
.ototal{display:flex;justify-content:space-between;align-items:baseline;padding-top:18px;gap:12px;flex-wrap:wrap}
.ototal span{font-weight:800;color:var(--muted);text-transform:uppercase;font-size:.85rem;letter-spacing:.06em}
.ototal output{font-family:var(--display);font-weight:800;font-size:1.9rem;color:var(--plum);font-variant-numeric:tabular-nums}
.ocount{font-size:.88rem;color:var(--muted);margin:6px 0 0}
.field{display:flex;flex-direction:column;gap:6px;margin-bottom:14px}
.field label{font-weight:800;font-size:.85rem}
.field input,.field textarea{font:500 1rem var(--body);color:var(--ink);background:var(--mist);border:2px solid transparent;border-radius:14px;padding:12px 14px;width:100%}
.field input:focus,.field textarea:focus{outline:none;border-color:var(--plum);background:#fff}
.field textarea{resize:vertical;min-height:72px}
.msg{font:500 .88rem/1.5 var(--body);white-space:pre-wrap;background:var(--mist);border-radius:14px;padding:12px 14px;min-height:170px;max-height:240px;overflow:auto;color:var(--ink);border:0;width:100%;resize:none}
.oacts{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.oacts .btn-p{background:var(--plum);color:#fff}
.ostatus{min-height:1.5em;margin:10px 0 0;font-weight:700;color:var(--muted)}
.ostatus.err{color:var(--chili)}
.btn-send{width:100%;min-height:56px;font-size:1.08rem;margin-top:4px}
.btn-send[disabled]{opacity:.6}
.req{color:var(--chili)}
.ferr{font-size:.85rem;font-weight:700;color:var(--chili);min-height:0}
.field input[aria-invalid="true"]{border-color:var(--chili)}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.done{margin-top:6px;padding:18px;border-radius:16px;background:#EAF6EA;color:#1F5F23}
.done b{display:block;font-family:var(--display);font-size:1.05rem;margin-bottom:6px}
.done p{margin:0 0 12px}
.fallback{margin-top:6px;padding:16px;border-radius:16px;background:var(--mist)}
.fallback p{margin:0 0 10px;font-weight:700;color:var(--chili)}
.fallback .ecode{margin:-4px 0 10px;font:600 .78rem var(--body);color:var(--muted)}
.ostep{margin:14px 0 0;padding-left:20px;color:var(--muted);font-size:.9rem}
.ostep li{margin-bottom:4px}
.phonebox{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:18px;padding:14px 16px;border-radius:16px;border:2px dashed var(--line)}
.phonebox b{font-family:var(--display);font-size:1.15rem;color:var(--plum);user-select:all}
.mini{border:0;background:var(--mist);border-radius:999px;padding:8px 14px;font:800 .85rem var(--body);cursor:pointer;color:var(--plum)}
.mini:hover{background:var(--saffron)}

/* footer */
.foot{background:var(--night);color:var(--lilac);padding-block:40px}
.foot .wrap{display:flex;flex-wrap:wrap;gap:24px;align-items:center;justify-content:space-between}
.foot .brand{color:#fff}
.foot .brand .logo{box-shadow:0 0 0 3px var(--saffron)}
.foot b{color:var(--saffron);font-family:var(--display);user-select:all}
.foot p{margin:0;font-size:.9rem}

@media (max-width:900px){
  .nav{display:none}
  .lang{margin-left:auto}
  .hero .wrap,.prod,.ogrid{grid-template-columns:1fr}
  .prod:nth-child(even) .gallery{order:0}
  .hero-art{max-width:520px}
}
@media (max-width:560px){
  .top .btn{display:none}
  .brand span{display:none}
  .seal{width:112px;height:112px;right:-4px}
  .seal b{font-size:1.25rem}
  .hero-art .logo{width:72px;height:72px;left:-6px;top:-6px}
  .oline{grid-template-columns:44px minmax(0,1fr) auto;row-gap:8px}
  .oline img{width:44px;height:44px}
  .on-sum{grid-column:2 / -1;text-align:left;font-size:.9rem;color:var(--muted)}
  .stepper .st-btn{width:36px;height:36px}
  .st-in{width:44px}
  .pb-num{font-size:1.9rem}
  .on-sum.zero{display:none}
  table{min-width:0}
  th:nth-child(3),td:nth-child(3){display:none}
  .tablewrap{padding:4px 14px}
  td,th{padding-inline:6px}
  .trow img{width:44px;height:44px}
  td.strong{font-size:1rem}
}
"""

JS = r"""
(function(){
  const P = __DATA__;
  const PHONE = "__PHONE__";
  const root = document.documentElement;
  const cart = {}; Object.keys(P).forEach(k => cart[k] = 0);
  const fmt = n => n.toLocaleString('ru-RU').replace(/ /g, ' ');
  const T = {
    uz:{cur:"so'm", hello:"Assalomu alaykum! Buyurtma bermoqchiman:", total:"Jami", name:"Do'kon / ism", phone:"Telefon", addr:"Manzil", note:"Izoh",
        empty:"Mahsulot tanlanmagan. Yuqoridagi + tugmasi bilan soni kiriting.", items:n=>`${n} ta qadoq`, copied:"Nusxa olindi. Endi Telegramni ochib, xabarga joylang.",
        copyFail:"Avtomatik nusxa olinmadi: matn belgilandi, o'zingiz nusxa oling.", phoneCopied:"Raqam nusxalandi.",
        needItems:"Avval kamida bitta mahsulot sonini tanlang.", badPhone:"Telefon raqamini to'liq kiriting, masalan +998 90 123 45 67.",
        sending:"Yuborilmoqda…", done:id=>`Rahmat! Buyurtma №${id} qabul qilindi`},
    ru:{cur:"сум", hello:"Здравствуйте! Хочу сделать заказ:", total:"Итого", name:"Магазин / имя", phone:"Телефон", addr:"Адрес", note:"Комментарий",
        empty:"Товары не выбраны. Укажите количество кнопкой + выше.", items:n=>`${n} упак.`, copied:"Скопировано. Откройте Telegram и вставьте сообщение.",
        copyFail:"Не удалось скопировать автоматически: текст выделен, скопируйте вручную.", phoneCopied:"Номер скопирован.",
        needItems:"Сначала выберите количество хотя бы одного товара.", badPhone:"Введите номер полностью, например +998 90 123 45 67.",
        sending:"Отправка…", done:id=>`Спасибо! Заказ №${id} принят`}
  };
  let lang = 'uz';
  try { const s = localStorage.getItem('mc-lang'); if (s === 'ru' || s === 'uz') lang = s; } catch(e) {}

  const $ = (s, el=document) => el.querySelector(s);
  const $$ = (s, el=document) => [...el.querySelectorAll(s)];
  const msgEl = $('#o-msg'), statusEl = $('#o-status');
  let sending = false;

  function setLang(l){
    lang = l; root.lang = l;
    $$('.lang button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === l)));
    $$('[data-ph-uz]').forEach(el => el.placeholder = el.dataset['ph' + (l === 'uz' ? 'Uz' : 'Ru')]);
    try { localStorage.setItem('mc-lang', l); } catch(e) {}
    statusEl.textContent = '';
    render();
  }

  function setQty(k, v){
    v = Math.max(0, Math.min(999, Math.floor(Number(v) || 0)));
    cart[k] = v; render();
  }

  function message(){
    const t = T[lang]; const lines = []; let i = 0, sum = 0;
    for (const k in cart) if (cart[k] > 0) {
      const s = cart[k] * P[k].price; sum += s; i++;
      lines.push(`${i}) ${P[k][lang]} × ${cart[k]} = ${fmt(s)} ${t.cur}`);
    }
    if (!lines.length) return '';
    const v = id => $(id).value.trim();
    const out = [t.hello, ...lines, `${t.total}: ${fmt(sum)} ${t.cur}`, ''];
    if (v('#o-name')) out.push(`${t.name}: ${v('#o-name')}`);
    if (v('#o-phone')) out.push(`${t.phone}: ${v('#o-phone')}`);
    if (v('#o-addr')) out.push(`${t.addr}: ${v('#o-addr')}`);
    if (v('#o-note')) out.push(`${t.note}: ${v('#o-note')}`);
    return out.join('\n').trim();
  }

  function render(){
    const t = T[lang]; let sum = 0, n = 0;
    for (const k in cart) {
      sum += cart[k] * P[k].price; n += cart[k];
      $$(`.stepper[data-key="${k}"]`).forEach(st => {
        const inp = $('.st-in', st);
        if (document.activeElement !== inp) inp.value = cart[k];
        st.classList.toggle('has', cart[k] > 0);
      });
      const line = $(`.oline[data-key="${k}"] .on-sum`);
      line.textContent = cart[k] ? `${fmt(cart[k] * P[k].price)} ${t.cur}` : '—';
      line.classList.toggle('zero', !cart[k]);
    }
    $('#o-total').textContent = `${fmt(sum)} ${t.cur}`;
    $('#o-count').textContent = n ? t.items(n) : t.empty;
    const m = message();
    msgEl.value = m || t.empty;
    $('#o-copy').disabled = !m;
    $('#o-send').disabled = sending;
  }

  document.addEventListener('click', e => {
    const b = e.target.closest('.st-btn');
    if (b) { const k = b.closest('.stepper').dataset.key; setQty(k, cart[k] + Number(b.dataset.d)); return; }
    const th = e.target.closest('.thumb');
    if (th) {
      const g = th.closest('.gallery');
      $('.gmain > img', g).src = th.dataset.src;
      $$('.thumb', g).forEach(x => x.classList.toggle('on', x === th));
      return;
    }
    const lb = e.target.closest('.lang button');
    if (lb) setLang(lb.dataset.lang);
  });
  $$('.st-in').forEach(inp => {
    inp.addEventListener('input', () => setQty(inp.closest('.stepper').dataset.key, inp.value));
    inp.addEventListener('blur', render);
  });
  $$('#o-name,#o-phone,#o-addr,#o-note').forEach(el => el.addEventListener('input', render));

  async function copy(text, okMsg, selectEl){
    try { await navigator.clipboard.writeText(text); statusEl.textContent = okMsg; }
    catch(e) { if (selectEl) { selectEl.focus(); selectEl.select(); } statusEl.textContent = T[lang].copyFail; }
  }
  $('#o-copy').addEventListener('click', () => { const m = message(); if (m) copy(m, T[lang].copied, msgEl); });
  $$('.copy-phone').forEach(b => b.addEventListener('click', () => copy(PHONE, T[lang].phoneCopied, null)));

  const phoneEl = $('#o-phone'), phoneErr = $('#o-phone-err');
  function phoneOk(){ const d = phoneEl.value.replace(/\D/g, ''); return d.length >= 9 && d.length <= 15; }
  phoneEl.addEventListener('input', () => { if (phoneOk()) { phoneErr.textContent = ''; phoneEl.removeAttribute('aria-invalid'); } });

  function showStatus(text, isErr){ statusEl.textContent = text; statusEl.classList.toggle('err', !!isErr); }

  $('#o-form').addEventListener('submit', async e => {
    e.preventDefault();
    if (sending) return;
    const t = T[lang];
    $('#o-fallback').hidden = true;
    if (!Object.values(cart).some(q => q > 0)) { showStatus(t.needItems, true); $('#buyurtma').scrollIntoView({behavior:'smooth'}); return; }
    if (!phoneOk()) { phoneErr.textContent = t.badPhone; phoneEl.setAttribute('aria-invalid', 'true'); phoneEl.focus(); showStatus('', false); return; }
    const payload = { items: {}, name: $('#o-name').value, phone: phoneEl.value, addr: $('#o-addr').value,
                      note: $('#o-note').value, website: $('#o-website').value, lang };
    for (const k in cart) if (cart[k] > 0) payload.items[k] = cart[k];
    sending = true; render(); showStatus(t.sending, false);
    try {
      const r = await fetch('/api/order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      const data = await r.json().catch(() => ({}));
      if (!r.ok || !data.ok) throw new Error((data.error || 'http') + ' ' + r.status + (data.tg_status ? ' tg' + data.tg_status : ''));
      showStatus('', false);
      $('#o-done-title').textContent = t.done(data.id);
      $('#o-done').hidden = false; $('#o-send').hidden = true;
      Object.keys(cart).forEach(k => cart[k] = 0);
      ['#o-note'].forEach(id => $(id).value = '');
    } catch (err) {
      if (String(err.message).startsWith('phone ')) { phoneErr.textContent = t.badPhone; phoneEl.focus(); showStatus('', false); }
      else { showStatus('', false); $('#o-ecode').textContent = 'Kod: ' + (err.message || 'network'); $('#o-fallback').hidden = false; }
    } finally { sending = false; render(); }
  });
  $('#o-new').addEventListener('click', () => { $('#o-done').hidden = true; $('#o-send').hidden = false; $('#mahsulotlar').scrollIntoView({behavior:'smooth'}); });

  setLang(lang);
})();
"""

SEO_TITLE = "Milliy Chips — eng mazali chipslar, narxlar va buyurtma"
SEO_DESC = ("Milliy Chips rasmiy sayti: Milliy Chips 900 g (smetana, shashlik, salyami, pishloq), 5D Chips va KAN tayoqchalari. "
            f"Do'konlar uchun ulgurji narxlar, buyurtma: {PHONE}.")
JSON_LD = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": SITE_URL + "/#org", "name": "Milliy Chips", "alternateName": ["Milliy chips", "Миллий чипс"],
         "url": SITE_URL + "/", "logo": SITE_URL + "/apple-touch-icon.png", "telephone": PHONE_DIGITS,
         "parentOrganization": {"@type": "Organization", "name": "KAN corporation"}},
        {"@type": "WebSite", "@id": SITE_URL + "/#site", "url": SITE_URL + "/", "name": "Milliy Chips", "inLanguage": ["uz", "ru"],
         "publisher": {"@id": SITE_URL + "/#org"}},
    ] + [
        {"@type": "Product", "name": p["name_uz"], "alternateName": RU_TITLE.get(p["key"], p["name_ru"]),
         "description": p["desc_uz"], "brand": {"@type": "Brand", "name": p["brand"]},
         "image": SITE_URL + "/og.jpg", "url": f"{SITE_URL}/#p-{p['key']}",
         "offers": {"@type": "Offer", "price": p["price"], "priceCurrency": "UZS", "url": f"{SITE_URL}/#p-{p['key']}",
                    "seller": {"@id": SITE_URL + "/#org"}}}
        for p in PRODUCTS
    ],
}, ensure_ascii=False)

HEAD = f"""<title>{esc(SEO_TITLE)}</title>
<meta name="description" content="{esc(SEO_DESC)}">
<link rel="canonical" href="{SITE_URL}/">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#2A1233">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Milliy Chips">
<meta property="og:locale" content="uz_UZ">
<meta property="og:locale:alternate" content="ru_RU">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:title" content="{esc(SEO_TITLE)}">
<meta property="og:description" content="{esc(SEO_DESC)}">
<meta property="og:image" content="{SITE_URL}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{JSON_LD}</script>"""

html = f"""{HEAD}
<style>
{font_faces()}
{CSS}
</style>

<header class="top">
  <div class="wrap">
    <a class="brand" href="#bosh">{logo()}<span>Milliy Chips</span></a>
    <nav class="nav" aria-label="Bo'limlar">
      <a href="#mahsulotlar">{L("Mahsulotlar", "Товары")}</a>
      <a href="#narxlar">{L("Narxlar", "Цены")}</a>
      <a href="#buyurtma">{L("Buyurtma", "Заказ")}</a>
    </nav>
    <div class="lang" role="group" aria-label="Til / Язык">
      <button type="button" data-lang="uz" aria-pressed="true">UZ</button>
      <button type="button" data-lang="ru" aria-pressed="false">RU</button>
    </div>
    <a class="btn" href="#buyurtma">{L("Buyurtma berish", "Заказать")}</a>
  </div>
</header>

<main>
<section class="hero" id="bosh">
  <div class="wrap">
    <div>
      <p class="eyebrow">{L("KAN corporation mahsulotlari", "Продукция KAN corporation")}</p>
      <h1 data-l="uz">Eng mazali <em>chipslar</em> do'koningiz peshtaxtasida</h1>
      <h1 data-l="ru">Самые вкусные <em>чипсы</em> на витрине вашего магазина</h1>
      <p class="hero-sub">{L("Milliy Chips, 5D va KAN tayoqchalari. Do'konlar uchun ulgurji qadoqlar, aniq narxlar va tez buyurtma.",
                            "Milliy Chips, 5D и палочки KAN. Оптовые упаковки для магазинов, понятные цены и быстрый заказ.")}</p>
      <div class="hero-cta">
        <a class="btn btn-y" href="#buyurtma">{L("Buyurtma berish", "Сделать заказ")}</a>
        <a class="btn btn-ghost" href="#narxlar">{L("Narxlarni ko'rish", "Смотреть цены")}</a>
      </div>
      <p class="hero-phone">{L("Buyurtma uchun telefon", "Телефон для заказа")}<b>{PHONE}</b></p>
    </div>
    <div class="hero-art">
      <img class="hi" src="{img(PRODUCTS[0]['photos'][0], 1400)}" alt="Milliy Chips qutilari">
      {logo()}
      <div class="seal"><small>Milliy Chips</small><b>{money(HERO['price'])}</b><small>{L(f"so'm · {HERO_W} g", f"сум · {HERO_W} г")}</small></div>
    </div>
  </div>
</section>

<div class="band" aria-hidden="true"><ul>{marquee_items * 2}{marquee_items * 2}</ul></div>

<section class="sec" id="mahsulotlar">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">{L("Assortiment", "Ассортимент")}</p><h2>{L("Mahsulotlar", "Наши товары")}</h2></div>
      <p>{L("Har bir mahsulot rasmini bosib, boshqa suratlarni ko'ring. Kerakli sonni kiriting, u buyurtmaga qo'shiladi.",
           "Нажмите на миниатюры, чтобы посмотреть другие фото. Укажите количество, и товар добавится в заказ.")}</p>
    </div>
    <div class="prods">{''.join(product_block(p, i) for i, p in enumerate(PRODUCTS))}</div>
  </div>
</section>

<section class="sec prices" id="narxlar">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">{L("Prays-list", "Прайс-лист")}</p><h2>{L("Narxlar", "Цены")}</h2></div>
      <p>{L(f"Narxlar bitta qadoq (quti yoki blok) uchun, {PRICE_DATE} holatiga.", "Цены указаны за одну упаковку (коробку или блок), октябрь 2026 г.")}</p>
    </div>
    <div class="tablewrap">
      <table>
        <thead><tr><th>{L("Mahsulot", "Товар")}</th><th>{L("Qadoq", "Упаковка")}</th>
          <th class="num">{L("Birlik narxi", "За единицу")}</th><th class="num">{L("Narxi", "Цена")}</th></tr></thead>
        <tbody>{price_rows()}</tbody>
      </table>
    </div>
    <p class="pnote">{L("Birlik narxi ma'lumot uchun hisoblangan. Narxlar o'zgarishi mumkin, aniq narxni telefon orqali so'rang.",
                       "Цена за единицу рассчитана для справки. Цены могут меняться, уточняйте по телефону.")}</p>
  </div>
</section>

<section class="sec order" id="buyurtma">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">{L("Tez buyurtma", "Быстрый заказ")}</p><h2>{L("Buyurtma berish", "Оформить заказ")}</h2></div>
      <p>{L("Sonini tanlang, telefon raqamingizni yozing va \"Buyurtma berish\"ni bosing. Buyurtma darhol bizga yetib boradi.",
           "Выберите количество, укажите телефон и нажмите «Отправить заказ». Заказ сразу придёт к нам.")}</p>
    </div>
    <div class="ogrid">
      <div class="ocard">
        <h3>{L("Mahsulotlar soni", "Количество")}</h3>
        <ul class="olist">{order_rows()}</ul>
        <div class="ototal"><span>{L("Jami", "Итого")}</span><output id="o-total">0</output></div>
        <p class="ocount" id="o-count"></p>
      </div>
      <form class="ocard" id="o-form" novalidate>
        <h3>{L("Ma'lumotlaringiz", "Ваши данные")}</h3>
        <div class="field"><label for="o-name">{L("Do'kon nomi yoki ismingiz", "Название магазина или имя")}</label>
          <input id="o-name" maxlength="100" autocomplete="organization" data-ph-uz="Masalan: Baraka do'koni" data-ph-ru="Например: магазин Барака"></div>
        <div class="field"><label for="o-phone">{L("Telefon", "Телефон")} <span class="req">*</span></label>
          <input id="o-phone" type="tel" maxlength="32" required autocomplete="tel" inputmode="tel" data-ph-uz="+998 __ ___ __ __" data-ph-ru="+998 __ ___ __ __" aria-describedby="o-phone-err">
          <span class="ferr" id="o-phone-err"></span></div>
        <div class="field"><label for="o-addr">{L("Manzil", "Адрес")}</label>
          <input id="o-addr" maxlength="200" autocomplete="street-address" data-ph-uz="Shahar, mahalla, ko'cha" data-ph-ru="Город, махалля, улица"></div>
        <div class="field"><label for="o-note">{L("Izoh", "Комментарий")}</label>
          <textarea id="o-note" rows="2" maxlength="500" data-ph-uz="Masalan: Milliy Chips 2 ta smetana, 1 ta pishloq" data-ph-ru="Например: Milliy Chips 2 сметана, 1 сыр"></textarea></div>
        <div class="hp" aria-hidden="true"><label for="o-website">Website</label><input id="o-website" tabindex="-1" autocomplete="off"></div>
        <button type="submit" class="btn btn-y btn-send" id="o-send">{L("Buyurtma berish", "Отправить заказ")}</button>
        <p class="ostatus" id="o-status" role="status" aria-live="polite"></p>
        <div class="done" id="o-done" hidden>
          <b id="o-done-title"></b>
          <p>{L("Buyurtmangiz bizga yetib bordi. Tez orada siz bilan bog'lanamiz.", "Ваш заказ получен. Мы скоро свяжемся с вами.")}</p>
          <button type="button" class="mini" id="o-new">{L("Yangi buyurtma", "Новый заказ")}</button>
        </div>
        <div class="fallback" id="o-fallback" hidden>
          <p>{L("Buyurtmani avtomatik yuborib bo'lmadi. Xabarni nusxalab, Telegramda yuboring:", "Не удалось отправить заказ автоматически. Скопируйте сообщение и отправьте в Telegram:")}</p>
          <textarea id="o-msg" class="msg" readonly aria-label="Buyurtma matni"></textarea>
          <p class="ecode" id="o-ecode"></p>
          <div class="oacts">
            <button type="button" class="btn btn-p" id="o-copy">{L("1. Xabarni nusxalash", "1. Скопировать")}</button>
            <a class="btn btn-y" href="{TG_LINK}" target="_blank" rel="noopener">{L("2. Telegramda ochish", "2. Открыть Telegram")}</a>
          </div>
        </div>
        <div class="phonebox"><span>{L("Yoki qo'ng'iroq qiling", "Или позвоните")}<br><b>{PHONE}</b></span>
          <button type="button" class="mini copy-phone">{L("Raqamni nusxalash", "Копировать номер")}</button></div>
      </form>
    </div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap">
    <a class="brand" href="#bosh">{logo()}<span>Milliy Chips</span></a>
    <p>KAN corporation · {L(f"Narxlar: {PRICE_DATE}", "Цены: октябрь 2026")}</p>
    <p>{L("Buyurtma", "Заказ")}: <b>{PHONE}</b></p>
  </div>
</footer>

<script>
{JS.replace("__DATA__", JS_DATA).replace("__PHONE__", PHONE)}
</script>
"""
# Til atributi skeleton tomonidan beriladi; boshlang'ich holatda ruscha yashirin bo'lishi uchun:
html = html.replace("<style>", "<script>document.documentElement.lang='uz'</script>\n<style>", 1)
open(OUT, "w", encoding="utf-8").write(html)
print(f"OK -> {OUT} ({os.path.getsize(OUT) / 1e6:.1f} MB)")

# Milliy Chips — katalog va sayt

KAN corporation mahsulotlari (Milliy Chips, 5D, KAN tayoqchalari) uchun reklama katalogi va bir sahifali sayt.
Narxlar `src/foto/` dagi rasm nomlaridan avtomatik olinadi.

| Fayl | Nima uchun |
|---|---|
| `index.html` | Sayt: mahsulotlar, narxlar, UZ/RU, buyurtma hisoblash va Telegram orqali yuborish |
| `katalog/Milliy-Chips-katalog.pdf` | A4 katalog, 7 sahifa — chop etish va yuborish uchun |
| `katalog/sahifalar/*.jpg` | Katalog sahifalari rasm ko'rinishida — Telegram/Instagram uchun |
| `katalog/index.html` | Katalogning web ko'rinishi |
| `api/order.js` | Vercel funksiyasi: saytdagi buyurtmani Telegram bot orqali yuboradi |
| `src/` | Katalog va saytni yig'uvchi kod, asl rasmlar va logo |

Hamma rasm va shriftlar HTML ichiga joylangan — `index.html` ni istalgan hostingga bitta fayl qilib yuklash mumkin.

## Narx yoki mahsulotni yangilash

1. Rasmni `src/foto/` ga **narx bilan boshlanadigan nom** bilan qo'ying, masalan `46000 900gr.jpg`.
   Qabul qilinadigan yozuvlar: `46000`, `46 000`, `46.000`, `46,000`.
   Bitta mahsulotning barcha rasmlarida narx bir xil bo'lishi shart — aks holda skript to'xtaydi.
2. Rasm nomi o'zgargan bo'lsa yoki yangi mahsulot qo'shilsa — `src/catalog_data.py` dagi `PRODUCTS` ro'yxatini tahrirlang
   (`photos`, nomlar, tavsif, ta'mlar).
3. Qayta yig'ing:

   ```bash
   bash src/yangilash.sh
   ```

   Talablar: Python 3 + Pillow, Node.js 18+, `pdftoppm` (poppler-utils).
   Skript `index.html`, `katalog/` ichidagi PDF, HTML va sahifa rasmlarini yangilaydi.

Telefon raqami va narx sanasi: `src/catalog_data.py` → `PHONE`, `PRICE_DATE`.

## GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)`.
Sayt: `https://<foydalanuvchi>.github.io/milliy-chips/`, katalog: `.../milliy-chips/katalog/`.

## Vercel

[vercel.com/new](https://vercel.com/new) → **Import Git Repository** → `milliy-chips` → **Deploy**.
Sozlamalar `vercel.json` da — hech narsani o'zgartirish shart emas (Framework: Other, build yo'q).
`src/` papkasi `.vercelignore` orqali saytga yuklanmaydi. Har bir `git push` dan keyin Vercel saytni o'zi yangilaydi.

## Google va Yandex'da chiqishi uchun

Saytda tayyor: sarlavha va tavsif, `canonical`, Open Graph rasmi (`og.jpg` — Telegram/Facebook havolada ko'rinadi),
mahsulotlar uchun structured data (schema.org), `robots.txt`, `sitemap.xml`, favicon.
Bularni `src/seo.py` yaratadi (`yangilash.sh` ichida avtomatik). Asosiy manzil: `src/catalog_data.py` → `SITE_URL`.

Qo'lda qilinadigan ishlar:
1. **Google Search Console** — <https://search.google.com/search-console> → *URL prefix* → `https://milliy-chips.vercel.app/`
   → tasdiqlash usuli *HTML tag* → kodni `site.py` dagi `HEAD` ga qo'shing → *Sitemaps*: `sitemap.xml` → *URL inspection* → *Request indexing*.
2. **Yandex Webmaster** — <https://webmaster.yandex.com> (O'zbekistonda ko'p ishlatiladi), xuddi shunday tasdiqlash va sitemap.
3. **Google Business Profile** — <https://business.google.com> — xaritada va qidiruvda kompaniya kartochkasi.
4. Instagram, Telegram kanal va boshqa sahifalarga sayt havolasini qo'ying.

## Buyurtmalar Telegramga (bot)

Mijoz "Buyurtma berish" ni bosganda `api/order.js` buyurtmani tekshiradi, narxni serverda qayta hisoblaydi
(`api/_prices.json`, `yangilash.sh` yaratadi) va Telegram bot orqali yuboradi. Token kodda saqlanmaydi.

Sozlash (bir marta):
1. Telegramda **@BotFather** → `/newbot` → nom va username bering → **token** ni oling.
2. Yangi botingizni oching va **Start** bosing (bot sizga yoza olishi uchun shart).
3. Chat ID: brauzerda `https://api.telegram.org/bot<TOKEN>/getUpdates` ni oching → `"chat":{"id": ...}` raqami.
   Guruhga kelsin desangiz: botni guruhga qo'shing, guruhda biror xabar yozing, so'ng getUpdates (ID manfiy bo'ladi, masalan `-100...`).
4. Vercel → loyiha → **Settings → Environment Variables**:
   - `TELEGRAM_BOT_TOKEN` = token
   - `TELEGRAM_CHAT_ID` = chat ID (bir nechta bo'lsa vergul bilan: `111,222`)
5. Vercel → **Deployments** → oxirgisi → **Redeploy** (o'zgaruvchilar faqat yangi deploydan keyin ishlaydi).

Funksiya ishlamasa (sozlanmagan, GitHub Pages'da yoki internet uzilsa) sayt avtomatik eski usulni ko'rsatadi:
xabarni nusxalash va Telegramni ochish.

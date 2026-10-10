# Milliy Chips — katalog va sayt

KAN corporation mahsulotlari (Milliy Chips, 5D, KAN tayoqchalari) uchun reklama katalogi va bir sahifali sayt.
Narxlar `src/foto/` dagi rasm nomlaridan avtomatik olinadi.

| Fayl | Nima uchun |
|---|---|
| `index.html` | Sayt: mahsulotlar, narxlar, UZ/RU, buyurtma hisoblash va Telegram orqali yuborish |
| `katalog/Milliy-Chips-katalog.pdf` | A4 katalog, 7 sahifa — chop etish va yuborish uchun |
| `katalog/sahifalar/*.jpg` | Katalog sahifalari rasm ko'rinishida — Telegram/Instagram uchun |
| `katalog/index.html` | Katalogning web ko'rinishi |
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

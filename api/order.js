// Vercel serverless funksiyasi: saytdagi buyurtmani Telegram bot orqali egasiga yuboradi.
//
// Vercel → Settings → Environment Variables:
//   TELEGRAM_BOT_TOKEN  — @BotFather bergan token (masalan 123456:ABC...)
//   TELEGRAM_CHAT_ID    — buyurtma keladigan chat ID; bir nechta bo'lsa vergul bilan: 111,222
//
// Narxlar mijozdan olinmaydi: ular _prices.json dan (src/yangilash.sh yaratadi) serverda hisoblanadi.

const PRICES = require("./_prices.json");

const LIMITS = { name: 100, phone: 32, addr: 200, note: 500, maxQty: 999 };

const money = (n) => n.toLocaleString("ru-RU").replace(/ /g, " ");
const clean = (v, max) => String(v ?? "").replace(/[\u0000-\u0008\u000B-\u001F\u007F]/g, "").trim().slice(0, max);

function validate(body) {
  if (!body || typeof body !== "object") return { error: "bad_request" };
  const name = clean(body.name, LIMITS.name);
  const phone = clean(body.phone, LIMITS.phone);
  const addr = clean(body.addr, LIMITS.addr);
  const note = clean(body.note, LIMITS.note);
  const digits = phone.replace(/\D/g, "");
  if (digits.length < 9 || digits.length > 15) return { error: "phone" };

  const items = body.items && typeof body.items === "object" ? body.items : {};
  const lines = [];
  let total = 0;
  for (const [key, raw] of Object.entries(items)) {
    const p = PRICES[key];
    const qty = Number(raw);
    if (!p) return { error: "unknown_product" };
    if (!Number.isInteger(qty) || qty < 0 || qty > LIMITS.maxQty) return { error: "qty" };
    if (qty === 0) continue;
    const sum = qty * p.price;
    total += sum;
    lines.push({ name: p.name, pack: p.pack, qty, price: p.price, sum });
  }
  if (!lines.length) return { error: "empty" };
  return { order: { name, phone, addr, note, lines, total } };
}

function format(o, id) {
  const time = new Date().toLocaleString("ru-RU", { timeZone: "Asia/Tashkent", dateStyle: "short", timeStyle: "short" });
  const out = [`🛒 Yangi buyurtma №${id}`, `🕒 ${time}`, ""];
  o.lines.forEach((l, i) => out.push(`${i + 1}) ${l.name} (${l.pack}) × ${l.qty} = ${money(l.sum)} so'm`));
  out.push("", `💰 Jami: ${money(o.total)} so'm`, "");
  if (o.name) out.push(`🏪 ${o.name}`);
  out.push(`📞 ${o.phone}`);
  if (o.addr) out.push(`📍 ${o.addr}`);
  if (o.note) out.push(`💬 ${o.note}`);
  return out.join("\n");
}

async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") return JSON.parse(req.body);
  const chunks = [];
  let size = 0;
  for await (const c of req) {
    size += c.length;
    if (size > 16 * 1024) throw new Error("too_large");
    chunks.push(c);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
}

module.exports = async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method" });
  }

  let body;
  try { body = await readBody(req); } catch { return res.status(400).json({ ok: false, error: "bad_request" }); }

  // Honeypot: odam ko'rmaydigan maydon to'ldirilgan bo'lsa — bot; jimgina "muvaffaqiyat" qaytaramiz.
  if (body && body.website) return res.status(200).json({ ok: true, id: "0" });

  const { order, error } = validate(body);
  if (error) return res.status(400).json({ ok: false, error });

  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chats = String(process.env.TELEGRAM_CHAT_ID || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (!token || !chats.length) return res.status(503).json({ ok: false, error: "not_configured" });

  const id = Date.now().toString(36).slice(-5).toUpperCase();
  const text = format(order, id);

  const results = await Promise.allSettled(chats.map((chat_id) =>
    fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id, text, disable_web_page_preview: true }),
    }).then(async (r) => { if (!r.ok) throw new Error(`telegram ${r.status}: ${await r.text()}`); })
  ));
  const failed = results.filter((r) => r.status === "rejected");
  failed.forEach((f) => console.error(f.reason && f.reason.message));
  if (failed.length === results.length) return res.status(502).json({ ok: false, error: "telegram" });

  return res.status(200).json({ ok: true, id, total: order.total });
};

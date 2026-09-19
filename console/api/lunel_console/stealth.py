"""Stealth layer: decoy site at / , real panel only at secret hidden path.

Env:
  LUNEL_HIDDEN_PATH e.g. /go-3ugea6r2mwwd
  LUNEL_DECOY_NAME  e.g. Nava Studio (optional)
"""
from __future__ import annotations

import os


def get_hidden_path() -> str:
    raw = os.environ.get("LUNEL_HIDDEN_PATH", "").strip()
    if not raw:
        return "/panel"
    if not raw.startswith("/"):
        raw = "/" + raw
    # normalize: no trailing slash (except root)
    if len(raw) > 1 and raw.endswith("/"):
        raw = raw.rstrip("/")
    # safety: hidden path bayad ba /api /auth /i /health /assets conflict nadashte bashe
    reserved = ("/api", "/auth", "/i/", "/i", "/health", "/ready", "/version",
                "/assets", "/robots.txt", "/sitemap.xml", "/favicon.ico")
    for r in reserved:
        if raw == r or raw.startswith(r + "/"):
            return "/panel"
    return raw


def get_decoy_name() -> str:
    return os.environ.get("LUNEL_DECOY_NAME", "Nava Studio").strip() or "Nava Studio"


def is_panel_path(path: str, hidden: str) -> bool:
    if path == hidden:
        return True
    if path.startswith(hidden + "/"):
        return True
    return False


DECOY_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} — Web Design & Digital Studio</title>
<meta name="description" content="{name} is a small digital studio crafting fast websites, branding and SEO for local businesses.">
<meta name="robots" content="index, follow">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23111827'/%3E%3Ctext x='16' y='21' font-size='15' text-anchor='middle' fill='white' font-family='Arial'%3EN%3C/text%3E%3C/svg%3E">
<style>
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#1f2937;background:#fff;line-height:1.6}
a{color:#2563eb;text-decoration:none}.wrap{max-width:1020px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid #e5e7eb;background:#fff;position:sticky;top:0;z-index:10}
.nav{display:flex;align-items:center;gap:22px;padding:14px 0}.logo{font-weight:800;font-size:18px;color:#111827}
.nav nav{margin-left:auto;display:flex;gap:18px;font-size:14px}.nav nav a{color:#4b5563}
.hero{padding:72px 0 48px;background:linear-gradient(180deg,#f8fafc,#fff);text-align:center}
.hero h1{font-size:42px;margin:0 0 12px;letter-spacing:-1px;color:#111827}
.hero p{color:#6b7280;max-width:620px;margin:0 auto 24px;font-size:17px}
.btn{display:inline-block;padding:12px 22px;border-radius:10px;background:#111827;color:#fff;font-weight:600;font-size:15px}
.btn.light{background:#f3f4f6;color:#111827;border:1px solid #e5e7eb}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:36px 0}
@media(max-width:760px){.grid{grid-template-columns:1fr}.hero h1{font-size:30px}.nav nav{display:none}}
.card{border:1px solid #e5e7eb;border-radius:14px;padding:20px;background:#fff}
.card h3{margin:0 0 6px;font-size:16px}.card p{margin:0;color:#6b7280;font-size:14px}
.sec{padding:28px 0}.sec h2{font-size:24px;margin:0 0 8px}.mut{color:#6b7280}
.blog{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:760px){.blog{grid-template-columns:1fr}}
.post{border:1px solid #e5e7eb;border-radius:12px;overflow:hidden}.post div{padding:14px}.post h4{margin:0 0 6px;font-size:15px}
footer{border-top:1px solid #e5e7eb;margin-top:40px;padding:26px 0;color:#6b7280;font-size:13px}
form{display:grid;gap:10px;max-width:420px}input,textarea{padding:11px 13px;border:1px solid #d1d5db;border-radius:9px;font-size:14px;width:100%}
</style>
</head>
<body>
<header><div class="wrap nav"><div class="logo">{name}</div>
<nav><a href="/">Home</a><a href="/about">About</a><a href="/services">Services</a><a href="/blog">Blog</a><a href="/contact">Contact</a></nav></div></header>
<div class="wrap">
<div class="hero">
<h1>We build fast, clean websites for small businesses</h1>
<p>{name} is a two-person studio. We design landing pages, company sites and online shops — fast, mobile-first and SEO-ready.</p>
<p><a class="btn" href="/contact">Get a quote</a> &nbsp; <a class="btn light" href="/services">Our services</a></p>
</div>
<div class="grid">
<div class="card"><h3>Landing pages</h3><p>One-page sites that load in under 1s. Copy, design and setup included.</p></div>
<div class="card"><h3>Company websites</h3><p>5-10 pages, blog, contact form, Google Maps and WhatsApp integration.</p></div>
<div class="card"><h3>Online shops</h3><p>Simple catalog + order via WhatsApp / Telegram. No complex backend.</p></div>
</div>
<div class="sec"><h2>Recent work</h2><p class="mut">Cafe menu site, real-estate landing, clinic appointment page, local shop catalog.</p></div>
<div class="sec"><h2>From the blog</h2><div class="blog">
<div class="post"><div><h4>Why speed matters for SEO in 2026</h4><p class="mut">3 fixes that cut load time in half.</p></div></div>
<div class="post"><div><h4>5 sections every landing page needs</h4><p class="mut">Hero, trust, pricing, FAQ, contact.</p></div></div>
<div class="post"><div><h4>How we deliver in 7 days</h4><p class="mut">Our simple process from call to launch.</p></div></div>
</div></div>
<div class="sec" id="contact"><h2>Contact</h2><p class="mut">Tell us about your project. We reply within 1 business day.</p>
<form onsubmit="return false"><input placeholder="Name"><input placeholder="Email or phone"><textarea rows="4" placeholder="What do you need?"></textarea><button class="btn" type="submit">Send message</button></form>
</div>
</div>
<footer><div class="wrap">© 2026 {name} · About · Services · Blog · Contact · Privacy<br><span>Fast · Mobile-first · SEO-ready</span></div></footer>
</body>
</html>
"""


def decoy_html() -> str:
    name = get_decoy_name()
    # simple escape for title
    safe = name.replace("<", "").replace(">", "")[:40]
    return DECOY_PAGE.replace("{name}", safe)

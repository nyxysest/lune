"""Lunel Console API — ASGI application.

Stealth mode:
* / , /about, /services, /blog, /contact -> decoy innocent site
* LUNEL_HIDDEN_PATH (e.g. /go-xxx) -> real panel
* /api, /auth, /i/<token>, /worker stay functional (needed for clients)
* unknown paths -> decoy (not panel) to avoid detection
"""
from __future__ import annotations

import contextlib
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from . import version
from .db import close_db, init_pool
from .logging import get, setup_logging
from .panel import router as panel_router
from .routers import admin, auth, backup, domains, instances, internal
from .security.ratelimit import RULES, client_ip, limiter
from .services.gateway import router as gateway_router
from .stealth import decoy_html, get_hidden_path, is_panel_path

setup_logging()
log = get("runtime", "lunel.console")

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app = FastAPI(title="Nava Studio", docs_url=None, redoc_url=None,
              version=version.version())

app.include_router(panel_router)
app.include_router(auth.router)
app.include_router(instances.router)
app.include_router(domains.router)
app.include_router(admin.router)
app.include_router(backup.router)
app.include_router(internal.router)
app.include_router(gateway_router)


def _hidden() -> str:
    return get_hidden_path()


def _decoy():
    return HTMLResponse(decoy_html(), headers={
        "Cache-Control": "public, max-age=3600",
        "X-Content-Type-Options": "nosniff",
    })


def _panel():
    from .panel import PAGE

    return HTMLResponse(PAGE, headers={"Cache-Control": "no-store"})


@app.get("/", include_in_schema=False)
async def decoy_home():
    return _decoy()


@app.get("/robots.txt", include_in_schema=False)
async def robots():
    hidden = _hidden()
    # disallow hidden path az crawler, allow baghie
    body = f"User-agent: *\nAllow: /\nDisallow: {hidden}\nDisallow: /api/\nDisallow: /auth/\nSitemap: /sitemap.xml\n"
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(body)


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap(request: Request):
    base = str(request.base_url).rstrip("/")
    body = f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{base}/</loc></url><url><loc>{base}/about</loc></url><url><loc>{base}/services</loc></url><url><loc>{base}/blog</loc></url><url><loc>{base}/contact</loc></url></urlset>"""
    from fastapi.responses import Response
    return Response(body, media_type="application/xml")


@app.get("/health")
async def health():
    # generic, bedune esm-e Lunel ta filter/checker حساس nashe
    return {"status": "ok"}


@app.get("/ready")
async def ready():
    from .db import db

    return {"ready": db is not None}


@app.get("/version")
async def version_endpoint():
    # generic version, bedune brand
    return {"status": "ok", "version": version.version()}


@app.get("/about", include_in_schema=False)
@app.get("/services", include_in_schema=False)
@app.get("/blog", include_in_schema=False)
@app.get("/contact", include_in_schema=False)
@app.get("/privacy", include_in_schema=False)
@app.get("/favicon.ico", include_in_schema=False)
async def decoy_pages():
    return _decoy()


@app.get("/panel", include_in_schema=False)
async def legacy_panel_block():
    # masir-e ghadimi ro lo bedim ta filter/checker peyda nakone
    return _decoy()


@app.exception_handler(404)
async def spa_fallback(request: Request, exc):
    """Stealth fallback: hidden path -> panel, baghie -> decoy (ya 404 JSON baraye API)."""
    path = request.url.path
    # API / gateway paths: JSON 404 (lazem baraye client-ha)
    if path.startswith(("/api/", "/api", "/auth/", "/auth", "/i/", "/worker/", "/worker")) or path in ("/health", "/ready", "/version"):
        return JSONResponse({"detail": "not found"}, status_code=404)
    hidden = _hidden()
    if is_panel_path(path, hidden):
        return _panel()
    # /assets-e Lunel ro public nade - decoy bede ta lo nare
    return _decoy()


@contextlib.asynccontextmanager
async def lifespan(_app):
    await init_pool()
    # hidden path ro log kon ta owner gom nakone (faghat dar server log, na dar page)
    try:
        h = _hidden()
        log.info("stealth: decoy at / , panel at %s", h)
    except Exception:
        pass
    log.info("Console %s started", version.version())
    yield
    await close_db()
    log.info("Console stopped")


app.router.lifespan_context = lifespan

# NOTE: /assets-e ghadimi (lunel.css) amdan public mount nemishe ta panel lo nare.
# Panel-e asli (panel.py PAGE) self-contained-e va be /assets niaz nadare.
# Decoy site ham inline CSS dare.

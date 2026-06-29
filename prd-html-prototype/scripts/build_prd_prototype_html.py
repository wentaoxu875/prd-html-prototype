#!/usr/bin/env python3
"""Build a PRD HTML review page with an embedded prototype iframe."""

from __future__ import annotations

import argparse
import html
import re
import shutil
from datetime import date
from pathlib import Path

MOBILE_PLATFORMS = {"app", "h5", "mobile", "mobile-web", "mini-program", "miniprogram", "小程序", "移动端"}
WEB_PLATFORMS = {"web", "web-pc", "pc", "desktop-web", "saas", "admin-console", "后台", "管理后台"}


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    in_list = False
    in_code = False
    code_lines: list[str] = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                close_list()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            close_list()
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            close_list()
            level = len(heading.group(1))
            text = html.escape(heading.group(2).strip())
            slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", heading.group(2).strip()).strip("-").lower()
            out.append(f'<h{level} id="{slug}">{text}</h{level}>')
            continue
        item = re.match(r"^[-*]\s+(.+)$", line)
        if item:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>" + inline_format(item.group(1)) + "</li>")
            continue
        close_list()
        out.append("<p>" + inline_format(line) + "</p>")
    close_list()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(out)


def inline_format(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def platform_layout(platform: str) -> tuple[str, str]:
    value = platform.strip().lower()
    if value in MOBILE_PLATFORMS:
        return "mobile-layout", "mobile"
    if value in WEB_PLATFORMS:
        return "web-layout", "web"
    return "web-layout", "web"


def build_html(title: str, platform: str, prd_html: str, prototype_name: str) -> str:
    shell_class, frame_class = platform_layout(platform)
    today = date.today().isoformat()
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)} - PRD 与原型</title>
  <style>
    :root {{ color-scheme: light; --ink:#17202a; --muted:#667085; --line:#d7dce2; --paper:#ffffff; --soft:#f6f8fb; --accent:#2563eb; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--ink); background:var(--soft); }}
    header {{ padding:24px 32px 16px; border-bottom:1px solid var(--line); background:var(--paper); }}
    h1 {{ margin:0 0 10px; font-size:28px; line-height:1.2; letter-spacing:0; }}
    .meta {{ display:flex; flex-wrap:wrap; gap:8px 14px; color:var(--muted); font-size:14px; }}
    main {{ padding:24px 32px 36px; }}
    .shell {{ max-width:1480px; margin:0 auto; }}
    .mobile-layout {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(390px,430px); gap:24px; align-items:start; }}
    .web-layout {{ display:grid; grid-template-columns:1fr; gap:28px; }}
    .prd {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:28px; min-width:0; }}
    .prd h2, .prd h3, .prd h4 {{ margin-top:26px; }}
    .prd h2:first-child, .prd h3:first-child {{ margin-top:0; }}
    .prd p, .prd li {{ line-height:1.72; }}
    .prd code {{ background:#eef2f7; padding:2px 5px; border-radius:4px; }}
    .prd pre {{ overflow:auto; background:#111827; color:#eef2ff; padding:16px; border-radius:8px; }}
    .prototype {{ min-width:0; }}
    .prototype h2 {{ margin:0 0 12px; font-size:18px; }}
    iframe {{ display:block; background:white; border:1px solid var(--line); box-shadow:0 8px 30px rgba(15,23,42,.08); }}
    iframe.mobile {{ width:100%; height:min(860px, calc(100vh - 96px)); border-radius:24px; }}
    iframe.web {{ width:100%; min-height:720px; height:calc(100vh - 120px); border-radius:8px; }}
    @media (max-width:900px) {{
      header {{ padding:20px 18px 14px; }}
      main {{ padding:18px; }}
      .mobile-layout {{ grid-template-columns:1fr; }}
      .prd {{ padding:20px; }}
      iframe.mobile {{ height:760px; }}
      iframe.web {{ height:680px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(title)}</h1>
    <div class="meta"><span>平台：{html.escape(platform)}</span><span>更新时间：{today}</span><span>交付物：PRD + 原型预览</span></div>
  </header>
  <main>
    <div class="shell {shell_class}">
      <article class="prd">
        {prd_html}
      </article>
      <section class="prototype" aria-label="原型预览">
        <h2>原型预览</h2>
        <iframe class="{frame_class}" src="./{html.escape(prototype_name)}" title="{html.escape(title)} 原型预览"></iframe>
      </section>
    </div>
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--platform", required=True, help="app, h5, mobile, web-pc, saas, admin-console, etc.")
    parser.add_argument("--prd", required=True, type=Path, help="Markdown PRD file")
    parser.add_argument("--prototype", required=True, type=Path, help="Prototype HTML file")
    parser.add_argument("--out", required=True, type=Path, help="Output directory")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    prd_text = args.prd.read_text(encoding="utf-8")
    prototype_name = "prototype.html"
    shutil.copy2(args.prototype, args.out / prototype_name)
    html_doc = build_html(args.title, args.platform, markdown_to_html(prd_text), prototype_name)
    (args.out / "prd.html").write_text(html_doc, encoding="utf-8")
    print(args.out / "prd.html")


if __name__ == "__main__":
    main()

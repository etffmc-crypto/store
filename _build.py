"""Builds the Flags Software store pages from _pages/*.html into the site folders.

Run: python _build.py   (files starting with _ are not served by GitHub Pages)
"""
import html as htmllib
import pathlib
import re

ROOT = pathlib.Path(__file__).parent

NAV = [
    ("", "Home"),
    ("purple-party/", "Purple Party"),
    ("dualforge/", "DualForge"),
    ("terms/", "Terms"),
    ("privacy/", "Privacy"),
    ("refund/", "Refunds"),
    ("#contact", "Contact"),
]

PAGES = {
    "home": "",
    "purple-party": "purple-party/",
    "dualforge": "dualforge/",
    "terms": "terms/",
    "privacy": "privacy/",
    "refund": "refund/",
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#120d1a">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%23a77bff'/%3E%3Cstop offset='1' stop-color='%23ff6b4a'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='url(%23g)'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="{up}"><span class="brand-mark" aria-hidden="true"></span>Flags Software</a>
<nav class="main" aria-label="Site">{nav}</nav>
</div></header>
<main id="main"><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
<span>&copy; 2026 Flags Software. Payments by Lemon Squeezy, our Merchant of Record.</span>
<nav aria-label="Legal">
<a href="{up}terms/">Terms of Service</a>
<a href="{up}privacy/">Privacy Policy</a>
<a href="{up}refund/">Refund Policy</a>
<a href="{up}#contact">Contact</a>
</nav>
</div></footer>
</body>
</html>
"""


def build():
    for name, path in PAGES.items():
        src = (ROOT / "_pages" / f"{name}.html").read_text(encoding="utf-8").replace("\r\n", "\n")
        meta, body = src.split("\n---\n", 1)
        fields = dict(re.findall(r"^(\w+):\s*(.*)$", meta, re.M))
        up = "../" * path.count("/")
        current = ' aria-current="page"'
        nav = "".join(
            f'<a href="{up}{href}"{current if href == path else ""}>{label}</a>'
            for href, label in NAV
        )
        html = TEMPLATE.format(
            title=htmllib.escape(fields["title"]), description=htmllib.escape(fields["description"]), up=up, nav=nav,
            body=body.replace("{up}", up).strip(),
        )
        out = ROOT / path / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8", newline="\n")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build()

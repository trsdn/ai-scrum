#!/usr/bin/env python3
"""Structural checks for the AI-Scrum GitHub Pages site.

This repository is a hand-written static site with no build step, so the only
things worth checking automatically are the ones that actually break the
published page:

* the files GitHub Pages needs are present (``index.html``, ``.nojekyll``);
* every locally referenced asset (CSS, JS, images, ...) exists on disk;
* every in-page ``#fragment`` link points at an element that exists;
* ``id`` attributes are unique, so fragment links are unambiguous;
* no local URL is root-absolute — this site is published under
  ``/ai-scrum/``, so ``/assets/...`` would 404 in production;
* each document declares charset, viewport, ``lang`` and a non-empty title;
* every ``<img>`` has an ``alt`` attribute.

Standard library only, so it runs anywhere Python 3.9+ is available with no
install step.

Usage::

    python3 .github/scripts/check_site.py [repo_root]
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

REQUIRED_FILES = ("index.html", ".nojekyll")

# Attributes that can hold a URL pointing at a local file or a fragment.
URL_ATTRS = ("href", "src", "poster", "data")

SKIPPED_SCHEMES = ("http", "https", "mailto", "tel", "data", "javascript")

EXCLUDED_DIRS = {".git", ".github", "node_modules"}


class Document(HTMLParser):
    """Collects the bits of an HTML document the checks below care about."""

    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: dict[str, int] = {}
        self.duplicate_ids: list[tuple[str, int]] = []
        self.references: list[tuple[str, str, int]] = []
        self.images_without_alt: list[int] = []
        self.html_lang = ""
        self.has_charset = False
        self.has_viewport = False
        self.has_description = False
        self._in_title = False
        self.title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: (value or "") for name, value in attrs}
        line = self.getpos()[0]

        element_id = attributes.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.append((element_id, line))
            else:
                self.ids[element_id] = line

        for attr in URL_ATTRS:
            value = attributes.get(attr)
            if value:
                self.references.append((attr, value.strip(), line))

        if tag == "html":
            self.html_lang = attributes.get("lang", "")
        elif tag == "img" and "alt" not in attributes:
            self.images_without_alt.append(line)
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            if "charset" in attributes:
                self.has_charset = True
            name = attributes.get("name", "").lower()
            if name == "viewport":
                self.has_viewport = True
            elif name == "description" and attributes.get("content", "").strip():
                self.has_description = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def parse(path: Path) -> Document:
    document = Document(path)
    document.feed(path.read_text(encoding="utf-8"))
    document.close()
    return document


def is_external(url: str) -> bool:
    parts = urlsplit(url)
    return bool(parts.scheme in SKIPPED_SCHEMES or parts.netloc)


def check_document(
    document: Document, root: Path, documents: dict[Path, Document]
) -> list[str]:
    errors: list[str] = []
    where = document.path.relative_to(root)

    def fail(line: int, message: str) -> None:
        errors.append(f"{where}:{line}: {message}")

    if not document.html_lang:
        fail(1, "<html> is missing a lang attribute")
    if not document.has_charset:
        fail(1, "no <meta charset> declared")
    if not document.has_viewport:
        fail(1, "no <meta name=\"viewport\"> declared")
    if not document.has_description:
        fail(1, "no non-empty <meta name=\"description\"> declared")
    if not document.title.strip():
        fail(1, "<title> is missing or empty")

    for element_id, line in document.duplicate_ids:
        fail(line, f"duplicate id {element_id!r} (fragment links become ambiguous)")

    for line in document.images_without_alt:
        fail(line, "<img> without an alt attribute")

    for attr, url, line in document.references:
        if is_external(url) or url.startswith("#!") or url == "#":
            continue

        parts = urlsplit(url)
        path_part = unquote(parts.path)
        fragment = unquote(parts.fragment)

        if path_part.startswith("/"):
            fail(
                line,
                f"{attr}={url!r} is root-absolute; the site is published under "
                "a subpath, so this 404s in production — use a relative URL",
            )
            continue

        if path_part:
            target = (document.path.parent / path_part).resolve()
            if not target.exists():
                fail(line, f"{attr}={url!r} points at a missing file")
                continue
        else:
            target = document.path

        if fragment:
            target_document = documents.get(target)
            if target_document is None and target.suffix in (".html", ".htm"):
                target_document = parse(target)
                documents[target] = target_document
            if target_document is not None and fragment not in target_document.ids:
                fail(line, f"{attr}={url!r} points at an id that does not exist")

    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    errors: list[str] = []

    for required in REQUIRED_FILES:
        if not (root / required).exists():
            errors.append(f"{required}: required by GitHub Pages but missing")

    html_files = sorted(
        path
        for path in root.rglob("*.html")
        if not EXCLUDED_DIRS.intersection(path.relative_to(root).parts)
    )

    if not html_files:
        errors.append("no HTML files found — nothing to publish")

    documents: dict[Path, Document] = {}
    for path in html_files:
        documents[path.resolve()] = parse(path)

    for path in html_files:
        errors.extend(check_document(documents[path.resolve()], root, documents))

    if errors:
        print(f"Site checks failed ({len(errors)} problem(s)):\n", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    checked = ", ".join(str(path.relative_to(root)) for path in html_files)
    print(f"Site checks passed ({checked}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

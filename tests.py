#!/usr/bin/env python3
"""Validation suite for the Free Plain-English Health Sites Directory.

Stdlib unittest only. Run: python3 tests.py
"""

import json
import os
import re
import subprocess
import sys
import unittest
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "sources.json")
MD = os.path.join(ROOT, "SOURCES.md")
HTML = os.path.join(ROOT, "site", "index.html")

REQUIRED_FIELDS = {
    "name", "url", "category", "publisher", "what", "reading_level",
    "ad_density", "account_required", "collects_data", "notes", "flags",
}
CATEGORIES = {"government", "hospital", "tracker"}
READING_LEVELS = {"Easy", "Moderate", "Advanced"}
AD_DENSITIES = {"None", "Low", "Moderate", "High"}


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


class TestData(unittest.TestCase):
    def setUp(self):
        self.d = load()

    def test_schema_complete(self):
        for s in self.d["sources"]:
            for field in REQUIRED_FIELDS:
                self.assertIn(field, s, f"{s.get('name')} missing {field}")

    def test_urls_https(self):
        for s in self.d["sources"]:
            u = urlparse(s["url"])
            self.assertEqual(u.scheme, "https", s["name"])
            self.assertTrue(u.netloc, s["name"])

    def test_enum_values_valid(self):
        for s in self.d["sources"]:
            self.assertIn(s["category"], CATEGORIES)
            self.assertIn(s["reading_level"], READING_LEVELS)
            self.assertIn(s["ad_density"], AD_DENSITIES)

    def test_names_unique(self):
        names = [s["name"] for s in self.d["sources"]]
        self.assertEqual(len(names), len(set(names)))

    def test_min_coverage(self):
        counts = {c: sum(1 for s in self.d["sources"] if s["category"] == c)
                  for c in CATEGORIES}
        for c, n in counts.items():
            self.assertGreaterEqual(n, 2, f"{c} has fewer than 2 sources")

    def test_trackers_flagged_for_privacy(self):
        for s in self.d["sources"]:
            if s["collects_data"]:
                self.assertTrue(
                    any("collects personal data" in f for f in s["flags"]),
                    f"{s['name']} collects data but has no privacy flag")

    def test_every_entry_has_notes(self):
        for s in self.d["sources"]:
            self.assertGreaterEqual(len(s["notes"]), 40, s["name"])


class TestGenerated(unittest.TestCase):
    def test_outputs_exist(self):
        self.assertTrue(os.path.isfile(MD), "SOURCES.md missing — run build.py")
        self.assertTrue(os.path.isfile(HTML), "site/index.html missing — run build.py")

    def test_md_covers_every_source(self):
        d = load()
        with open(MD, encoding="utf-8") as f:
            text = f.read()
        for s in d["sources"]:
            self.assertIn(s["name"], text)
            self.assertIn(s["url"], text)
            self.assertIn(f"- **Reading level:** {s['reading_level']}", text)

    def test_html_covers_every_source(self):
        d = load()
        with open(HTML, encoding="utf-8") as f:
            text = f.read()
        for s in d["sources"]:
            self.assertIn(escape(s["url"]), text)
            self.assertIn(escape(s["name"]), text)
        self.assertEqual(text.count('class="card"'), len(d["sources"]))

    def test_html_disclaimers_and_privacy_claims(self):
        with open(HTML, encoding="utf-8") as f:
            text = f.read()
        self.assertIn("never medical advice", text.lower())
        self.assertIn("collects no data", text.lower())
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)

    def test_html_no_scripts_or_trackers(self):
        with open(HTML, encoding="utf-8") as f:
            text = f.read()
        self.assertNotIn("<script", text.lower())
        for term in ("googletagmanager", "google-analytics", "plausible",
                     "matomo", "cloudflareinsights", "hotjar"):
            self.assertNotIn(term, text.lower())
        # data URLs (favicon) allowed, no external assets
        self.assertNotIn('src="http', text.lower())
        self.assertNotIn('href="http://', text.lower())


def escape(s):
    from html import escape as _e
    return _e(s, quote=True)


class TestPackaging(unittest.TestCase):
    def test_license_exact(self):
        with open(os.path.join(ROOT, "LICENSE"), encoding="utf-8") as f:
            status = None
            copyright_line = None
            for line in f:
                line = line.rstrip("\n")
                if re.fullmatch(r"Permission is hereby granted.*", line):
                    status = "found"
                if line.strip().startswith("Copyright (c) "):
                    copyright_line = line.rstrip("\n")
            self.assertIsNotNone(status, "MIT permission sentence missing")
            self.assertEqual(copyright_line, "Copyright (c) 2026 Asdale Dynamics, LLC")

    def test_readme_credit_and_distinction(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("Asdale Dynamics, LLC", text)
        self.assertIn("free-official-help-directory", text)
        self.assertIn("never medical advice", text.lower())

    def test_rebuild_is_deterministic(self):
        before = {}
        for path in (MD, HTML):
            with open(path, "rb") as f:
                before[path] = f.read()
        subprocess.run([sys.executable, os.path.join(ROOT, "build.py")],
                       check=True, capture_output=True)
        for path in (MD, HTML):
            with open(path, "rb") as f:
                self.assertEqual(before[path], f.read(), f"{path} not deterministic")


if __name__ == "__main__":
    unittest.main(verbosity=2)

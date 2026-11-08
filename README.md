# Free Plain-English Health Sites Directory

A hand-built directory of **trustworthy, plain-English health information sources** that are free to read:
MedlinePlus, NIH institute pages, hospital teaching libraries, and free meal/medication trackers.
Every entry carries two honest ratings:

- **Reading level** — Easy (~5th–6th grade), Moderate (~8th–9th), or Advanced (10th+)
- **Ad density** — None, Low, Moderate, or High (commercial sites are labeled openly)

**Education only — never medical advice.** This project collects **no data**, uses no analytics,
no cookies, and no trackers. The generated site is a pure static HTML file you can open offline.

## Quick start

```bash
python3 build.py        # regenerates site/index.html from data/sources.json
python3 tests.py        # runs the validation suite
```

Then open `site/index.html` in any browser. No server, no accounts, no network required.

## What's inside

| Path | What it is |
|---|---|
| `SOURCES.md` | The full directory in plain markdown |
| `data/sources.json` | Machine-readable source list (the single source of truth) |
| `build.py` | Stdlib-only generator that turns the JSON into `site/index.html` |
| `site/index.html` | The finished static site (generated) |
| `tests.py` | Validation: data integrity, link hygiene, disclaimers, build output |

## Editorial rules

1. Every source must be **free to read** (a free account tier is noted, never required just to read).
2. Reading-level labels are plain-language approximations, not clinical Flesch-Kincaid scores.
3. Ad density is rated from a reader's point of view: banners alongside content count; a site's own
   footers and "share" buttons do not.
4. Anything requiring an account or collecting personal data is flagged explicitly.
5. Every page and every table carries the "education only, not medical advice" notice.

## Distinct from `free-official-help-directory`

That sibling repository catalogs **general government help** (benefits, taxes, paperwork).
This one is **health reading and self-tracking tools only**. Overlap is intentionally avoided.

## About the ratings

Reading level and ad density are informed human estimates as of November 2026; sites redesign
constantly, so treat the labels as a starting judgment call, not a guarantee.

## License

MIT — see `LICENSE`. Copyright (c) 2026 Asdale Dynamics, LLC.
Published as part of Asdale Dynamics, LLC's beginner-friendly, plain-English education library
(The Massive AI Manual, https://dylanasdale.github.io).

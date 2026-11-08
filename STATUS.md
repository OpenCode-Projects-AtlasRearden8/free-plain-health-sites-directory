# STATUS — Free Plain-English Health Sites Directory

Date: 2026-11-08 · Published by Asdale Dynamics, LLC · MIT licensed

## What was built

A verified directory of **16 trustworthy, free, plain-English health sources**, each rated for
**reading level** (Easy / Moderate / Advanced) and **ad density** (None / Low / Moderate / High),
with account-required and personal-data flags called out explicitly:

- **7 government/NIH sites** — MedlinePlus, MedlinePlus Medical Encyclopedia, NIH News in Health,
  NIA, NIDDK, NHLBI, CDC
- **5 hospital teaching libraries** — Cleveland Clinic, Johns Hopkins, University of Michigan,
  Mount Sinai, Mayo Clinic
- **4 free meal/med trackers** — MyPlate.gov, Medisafe, MyFitnessPal, Cronometer (the three
  commercial trackers are honestly flagged: account required, collects personal data, ads)

Deliverables:

| File | Role |
|---|---|
| `data/sources.json` | Single source of truth (16 entries, strict schema) |
| `build.py` | Stdlib-only generator → `SOURCES.md` + `site/index.html` |
| `SOURCES.md` | Full markdown directory (generated, so JSON/MD/HTML always agree) |
| `site/index.html` | Static site: no JavaScript, no external assets, no cookies, no analytics |
| `tests.py` | 15-test validation suite (unittest) |
| `README.md`, `LICENSE` | MIT with exact line `Copyright (c) 2026 Asdale Dynamics, LLC` |

Guarantees enforced everywhere: **education only, never medical advice** notices; **no data
collection** (the site emits zero scripts and zero network assets — enforced by tests).

## How to run

```bash
python3 build.py     # regenerate SOURCES.md and site/index.html from data/sources.json
python3 tests.py     # run the 15-test validation suite
# then open site/index.html in any browser — fully offline-capable
```

## Verification results

- `python3 tests.py` → **15/15 OK** (schema, HTTPS-only links, enum validity, uniqueness,
  privacy flags on data-collecting trackers, markdown/HTML coverage, "no script/no tracker"
  checks, exact LICENSE line, README credit, deterministic rebuild).
- Generated HTML parsed clean by `html.parser` (no structural errors).
- Deterministic build verified byte-for-byte across a rebuild.
- Two test bugs found and fixed during development (trailing-newline `fullmatch` issue in the
  license check; markdown format string mismatch).

## Known gaps

- **Ratings are informed human estimates** (Nov 2026), not measured Flesch-Kincaid scores; the
  JSON carries no automated readability computation. Reading levels and ad densities should be
  re-checked roughly annually.
- **URLs were not re-crawled today**; they are well-established, permanent-looking pages, but a
  periodic link check (e.g. `lychee` + `-describe`) would harden this.
- **Coverage is deliberately small and vetted** (16 sources) rather than exhaustive; candidates
  for future additions: AAP/HealthyChildren, FamilyDoctor.org, NIAMS, NCI, FreeFrom trackers.
- **Accessibility**: single-file layout is keyboard-navigable with semantic headings and real
  link text, but no WCAG audit has been run.
- **No i18n yet**: Spanish equivalents are noted in descriptions but not indexed separately.

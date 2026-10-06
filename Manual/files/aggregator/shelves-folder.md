# `shelves/`

The literature, arriving with the stages that read it.

## What it holds

One Markdown file per work at `shelves/<stage>/<tier>/<name>.md`: the title, the source file, and the text extracted by pdftotext (OCR for a scan), with page breaks kept as `--- page N ---`. The rows come from `SHELVES.tsv` (stage, tier, name, source, title). A tier is `read` (shipped with the stage) or `on-request` (listed one line each, opened only if asked). A row whose source is `-` is a stub: the work is named and not held. Rows exist for stages A1, B1, C2, C3, D1, D4 and E1.

## Who writes it, and when

`build_shelves.py`, handler side, from a folder of PDFs. `build.sh` copies `shelves/<stage>/` into `DROPS/<stage>/shelves/`, and `step.sh` delivers it at the stage's first leg. The analyst reads it through `mem.py shelf`.

## Why it exists

METHOD: the method shelf arrives at A1, B1 and C2, the explanation shelf at C3, the adaptation shelf at D1, the hierarchy shelf at D4 and the critique shelf at E1. Contract §4: "Nothing is read against the explanation literature before stage C3." STANDING §1: "A shelf that has arrived stays."

## The metadata pages

For people, not for the analyst: [shelves/_meta/](../../../aggregator/instrument/shelves/_meta/README.md) has one page per work with authors, title, journal, year, volume, issue, pages, DOI and the abstract. `make_meta.py --fetch` looks each work up on Crossref (a DOI printed in the PDF wins over a title search) and stores the result in `BIB.json`; `make_meta.py` then writes the pages, cutting the abstract from the PDF or, failing that, taking Crossref's. A field Crossref does not give stays empty. Five works have no Crossref record and were entered by hand without pages (Machlup 1967, Vaughan 1992, Kozlowski and Klein 2000, Mintzberg 1979, the call for papers); their pages say so. `bib_checked: true` means the title, authors and journal were compared with the shelf line by hand; volume and pages are Crossref's. These pages are not copied into the run.

## Where

[shelves/](../../../aggregator/runs/claude-v43-1/00_GIVE-THE-AGENT/shelves/); the list [aggregator/instrument/shelves/SHELVES.tsv](../../../aggregator/instrument/shelves/SHELVES.tsv).

Checked against: shelves/SHELVES.tsv, tools/build_shelves.py, harness/build.sh, METHOD.md, CONTRACT-aggregator.md §4, STANDING-INSTRUCTIONS.md §1.

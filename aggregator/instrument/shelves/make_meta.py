#!/usr/bin/env python3
"""make_meta.py: one metadata page per shelved work, beside its PDF.

    python3 shelves/make_meta.py --fetch          # handler, once: look every work up on Crossref -> shelves/BIB.json
    python3 shelves/make_meta.py --src <pdf dir>  # write shelves/_meta/<name>.md for every row of SHELVES.tsv

BIB.json holds the bibliographic fields as Crossref returns them (authors, title, journal, year,
volume, issue, pages, DOI) and the Crossref match score. A DOI printed in the PDF wins over a title
search. Rows whose match was checked by hand carry "checked": true; a row with "checked": false is
flagged on its page. The abstract is cut from the PDF's first three pages (pdftotext), between the
word Abstract and the first of Keywords, Managerial Summary, Introduction or a heading; when the PDF
has none, the Crossref abstract is used; when neither exists (an editorial, a book chapter), the page
says so. Nothing is invented: a field Crossref does not give is left empty.
"""
import argparse, csv, html, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TSV, BIB, OUT = os.path.join(HERE, "SHELVES.tsv"), os.path.join(HERE, "BIB.json"), os.path.join(HERE, "_meta")
UA = {"User-Agent": "rplace-shelves/1.0 (mailto:research@example.org)"}
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>]+[^\s\"<>.,;)])", re.I)


def rows():
    return list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))


def pdftext(path, last=3):
    try:
        return subprocess.run(["pdftotext", "-l", str(last), path, "-"], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""


def get(url, tries=5):
    for k in range(tries):
        try:
            time.sleep(1.5)
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)["message"]
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            time.sleep(10 * (k + 1))


def lookup(row, text):
    m = DOI_RE.search(text or "")
    if m:
        try:
            return get("https://api.crossref.org/works/" + urllib.parse.quote(m.group(1))), 100.0, "doi in pdf"
        except Exception:
            pass
    title = re.sub(r"\s*\(.*?\)", "", row["title"].split("), ", 1)[-1]).split(",")[0]
    who = row["title"].split("(")[0]
    q = urllib.parse.urlencode({"query.bibliographic": title, "query.author": who, "rows": 1})
    items = get("https://api.crossref.org/works?" + q).get("items") or []
    return (items[0], items[0].get("score", 0.0), "title search") if items else (None, 0.0, "none")


def fields(msg):
    if not msg:
        return {}
    auth = [("%s %s" % (a.get("given", ""), a.get("family", "") or a.get("name", ""))).strip() for a in msg.get("author", [])]
    dp = (msg.get("published-print") or msg.get("published-online") or msg.get("issued") or {}).get("date-parts", [[None]])
    return {"authors": auth, "title": (msg.get("title") or [""])[0], "journal": (msg.get("container-title") or [""])[0],
            "year": dp[0][0], "volume": msg.get("volume", ""), "issue": msg.get("issue", ""), "pages": msg.get("page", ""),
            "doi": msg.get("DOI", ""), "type": msg.get("type", ""), "publisher": msg.get("publisher", ""),
            "crossref_abstract": msg.get("abstract", "")}


def abstract_from(text):
    m = re.search(r"\bAbstract[.:]?\s*(.+?)(?:\n\s*(?:Keywords?|KEYWORDS|Managerial Summary|Research Summary|1\s*\|?\s*INTRODUCTION|Introduction)\b)",
                  text or "", re.S)
    if not m:
        return ""
    a = re.sub(r"-\n(\w)", r"\1", m.group(1))
    a = re.sub(r"\s+", " ", a).strip()
    return a if 200 < len(a) < 4000 else ""


def abstract_from_metadata(pdf):
    """A journal that prints no 'Abstract' heading (MIS Quarterly) often carries the abstract in the PDF's
    Subject field; pdfinfo prints it."""
    try:
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""
    m = re.search(r"^Subject:\s*(.+)$", out, re.M)
    a = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    return a if 200 < len(a) < 4000 else ""


def strip_jats(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--refetch", action="store_true", help="look up again rows already found")
    ap.add_argument("--src", default=os.path.join(HERE, "_src"), help="PDF folders, separated by %s" % os.pathsep)
    a = ap.parse_args(argv)
    bib = json.load(open(BIB, encoding="utf-8")) if os.path.exists(BIB) else {}
    if a.fetch:
        for r in rows():
            old = bib.get(r["name"], {})
            if old.get("checked") or (old.get("score", 0) > 0 and not a.refetch):
                continue
            pdf = os.path.join(a.src, r["source"]) if r["source"] != "-" else ""
            try:
                msg, score, how = lookup(r, pdftext(pdf, 2) if pdf and os.path.exists(pdf) else "")
            except Exception as e:
                msg, score, how = None, 0.0, "error: %s" % e
            f = fields(msg)
            f.update({"score": score, "how": how, "checked": False})
            bib[r["name"]] = f
            print("%-34s %-12s %6.1f  %s" % (r["name"], how, score, (f.get("title") or "")[:70]))
        json.dump(bib, open(BIB, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        return 0
    os.makedirs(OUT, exist_ok=True)
    n = {"pdf": 0, "crossref": 0, "none": 0}
    for r in rows():
        b = bib.get(r["name"], {})
        pdf = next((os.path.join(d, r["source"]) for d in a.src.split(os.pathsep)
                    if r["source"] != "-" and os.path.exists(os.path.join(d, r["source"]))), "")
        have = bool(pdf)
        ab, src = (abstract_from(pdftext(pdf)), "the PDF") if have else ("", "")
        if have and not ab:
            ab, src = abstract_from_metadata(pdf), "the PDF's metadata (its Subject field)"
        if not ab and b.get("crossref_abstract"):
            ab, src = strip_jats(b["crossref_abstract"]), "Crossref"
        n["pdf" if src.startswith("the PDF") and ab else "crossref" if ab else "none"] += 1
        au = b.get("authors") or []
        lines = ["---", "name: %s" % r["name"], "stage: %s" % r["stage"], "tier: %s" % r["tier"],
                 "authors: %s" % json.dumps(au, ensure_ascii=False), "title: %s" % json.dumps(b.get("title") or r["title"], ensure_ascii=False),
                 "journal: %s" % json.dumps(b.get("journal", ""), ensure_ascii=False), "year: %s" % (b.get("year") or ""),
                 "volume: %s" % b.get("volume", ""), "issue: %s" % b.get("issue", ""), "pages: %s" % b.get("pages", ""),
                 "doi: %s" % b.get("doi", ""), "pdf: %s" % (r["source"] if r["source"] != "-" else ""),
                 "bib_checked: %s" % str(bool(b.get("checked"))).lower(), "---", "",
                 "# %s" % r["title"], "",
                 "**Shelf:** %s, %s. **PDF:** %s." % (r["stage"], r["tier"], "`%s`" % r["source"] if have else "not in this repository"), ""]
        if b and not b.get("checked"):
            lines += ["> The bibliographic fields come from a Crossref %s (score %.0f) and were not checked by hand." % (b.get("how", "match"), b.get("score", 0)), ""]
        if not b:
            lines += ["> No Crossref record; the fields above are empty. The shelf line is the only reference.", ""]
        lines += ["## Abstract", "", ab if ab else "No abstract found in the PDF or on Crossref (an editorial, a chapter or a book).", ""]
        if ab:
            lines += ["Source of the abstract: %s." % src, ""]
        open(os.path.join(OUT, r["name"] + ".md"), "w", encoding="utf-8").write("\n".join(lines))
    idx = ["# Shelf metadata", "", "One page per shelved work: authors, title, journal, year, volume, issue, pages, DOI and abstract. "
           "Made by `make_meta.py` from `BIB.json` (Crossref) and the PDFs.", "",
           "| Stage | Tier | Work | Year | Journal |", "|---|---|---|---|---|"]
    for r in rows():
        b = bib.get(r["name"], {})
        idx.append("| %s | %s | [%s](%s.md) | %s | %s |" % (r["stage"], r["tier"], r["title"].split("), ")[0] + ")", r["name"],
                                                          b.get("year") or "", b.get("journal", "")))
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print("pages: %d; abstracts from the PDF %d, from Crossref %d, none %d" % (len(rows()), n["pdf"], n["crossref"], n["none"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

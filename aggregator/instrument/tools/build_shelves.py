#!/usr/bin/env python3
"""build_shelves.py: the shelves, from shelves/SHELVES.tsv and the PDFs in a literature folder.

    python3 tools/build_shelves.py --lit <folder of PDFs> [--root INSTRUMENT]

For each row (stage, tier, name, source, title) writes shelves/<stage>/<tier>/<name>.md: the title,
the source file, and the text extracted by pdftotext (tesseract OCR for a scanned PDF), page
breaks kept as `--- page N ---`. A row whose source is `-` is a stub: the work is named and not
held, and the stub says how the analyst treats it (stage C3's `recalled` rule). build.sh copies
shelves/<stage>/ into DROPS/<stage>/shelves/, so a shelf arrives with its stage and stays.
A source not in --lit is looked for in shelves/_src/ (papers held with the instrument, never
shipped: build.sh copies only the stage folders). Handler-side; the analyst never runs it. Writes SHELVES-report.tsv: words per work, and why a
work has none.
"""
import argparse, csv, os, subprocess, sys, tempfile, glob

STUB = ("# {title}\n\nNot held on this shelf: the run has the name of this work and not its text. "
        "If you use it, work from what you know of it, mark the use `recalled` with author, year and the "
        "claim you attribute (stage C3), and say so where you use it. The title above is as recalled by the "
        "handler and was not checked against the work.\n")


def pages(pdf):
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    return out.split("\f")


def ocr(pdf):
    d = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-r", "200", "-gray", "-png", pdf, os.path.join(d, "p")], check=True)
    texts = []
    for img in sorted(glob.glob(os.path.join(d, "p*.png"))):
        texts.append(subprocess.run(["tesseract", img, "-", "--psm", "1"], capture_output=True, text=True).stdout)
    return texts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lit", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(os.path.join(a.root, "shelves", "SHELVES.tsv"), encoding="utf-8"), delimiter="\t"))
    rep = ["stage\ttier\tname\twords\tnote"]
    for r in rows:
        if a.only and r["name"] not in a.only.split(","):
            continue
        d = os.path.join(a.root, "shelves", r["stage"], r["tier"])
        os.makedirs(d, exist_ok=True)
        dst = os.path.join(d, r["name"] + ".md")
        if r["source"] == "-":
            open(dst, "w", encoding="utf-8").write(STUB.format(title=r["title"]))
            rep.append("%s\t%s\t%s\t0\tstub: not held" % (r["stage"], r["tier"], r["name"]))
            continue
        src = os.path.join(a.lit, r["source"])
        if not os.path.exists(src):  # papers held with the instrument, not in the literature folder
            src = os.path.join(a.root, "shelves", "_src", r["source"])
        if not os.path.exists(src):
            open(dst, "w", encoding="utf-8").write(STUB.format(title=r["title"]))
            rep.append("%s\t%s\t%s\t0\tsource missing: %s" % (r["stage"], r["tier"], r["name"], r["source"]))
            continue
        ps = pages(src)
        note = "pdftotext"
        if sum(len(p.split()) for p in ps) < 200:
            ps, note = ocr(src), "OCR (tesseract): check the text before relying on a quote"
        body = "\n".join("\n--- page %d ---\n\n%s" % (i + 1, p.strip()) for i, p in enumerate(ps) if p.strip())
        head = ("# %s\n\nSource: `%s`. Text extracted by %s; layout kept, page breaks marked. A quote from this "
                "file is the extraction's, so check an odd word against the page it names.\n" % (r["title"], r["source"], note))
        open(dst, "w", encoding="utf-8").write(head + body + "\n")
        rep.append("%s\t%s\t%s\t%d\t%s" % (r["stage"], r["tier"], r["name"], len(body.split()), note))
    report = os.path.join(a.root, "shelves", "SHELVES-report.tsv")
    if a.only and os.path.exists(report):   # a partial build keeps the other works' rows (2026-10-04)
        done = {l.split("\t")[2] for l in rep[1:]}
        kept = [l for l in open(report, encoding="utf-8").read().splitlines()[1:] if l.split("\t")[2:3] and l.split("\t")[2] not in done]
        order = [r["name"] for r in rows]
        rep = [rep[0]] + sorted(rep[1:] + kept, key=lambda l: order.index(l.split("\t")[2]) if l.split("\t")[2] in order else len(order))
    open(report, "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    sys.exit(main())

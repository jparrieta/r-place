#!/usr/bin/env python3
"""emit_tables.py — turn the scan into the two tables the aggregator asked for."""
import csv, json, os, sys
OPEN=1490976000; LO,HI=-168,336
rows=[json.loads(l) for l in open('_progress.jsonl',encoding='utf-8') if l.strip()]
rows.sort(key=lambda r: r['sub'])

# A. the histogram, long form — one row per (community, hour)
with open('venue_activity.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['sub','hour_since_open','n_items'])
    n=0
    for r in rows:
        for h in sorted(int(k) for k in r['hours']):
            w.writerow([r['sub'],h,r['hours'][str(h)] if str(h) in r['hours'] else r['hours'][h]]); n+=1
print("venue_activity.csv: %d rows (non-zero hours only)"%n)

# B. one row per community — the convenience columns, incl. the single field that matters most
with open('venue_summary.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['sub','n_items_all','first_item_utc','last_item_utc','last_item_utc_in_window',
                'last_item_hour_in_window','n_items_pre168','n_items_win97','n_items_during73',
                'n_items_after_freeze','n_segments'])
    for r in rows:
        H={int(k):v for k,v in r['hours'].items()}
        pre=sum(v for h,v in H.items() if h<0)
        win=sum(v for h,v in H.items() if 0<=h<97)
        d73=sum(v for h,v in H.items() if 0<=h<73)
        aft=sum(v for h,v in H.items() if h>=73)
        lw=r.get('last_item_utc_in_window')
        w.writerow([r['sub'],r['n_items_all'],r['first_item_utc'],r['last_item_utc'],lw,
                    (round((lw-OPEN)/3600.0,2) if lw else ''),pre,win,d73,aft,r['n_files']])
print("venue_summary.csv: %d communities"%len(rows))

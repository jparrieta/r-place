# `SCHEMA-adaptations.md`

The types of the return: elements, operations, the ledger line, adjudication.

## What it holds

Ten sections: elements of the global model (five kinds: process P, condition K, claim C, role R, arrow A); operations; the ledger line; validation at ingest; the room model; adjudication; what is built from the ledger; reconstruction; the handoff folder (stage D1); decisions taken and their consequences. It calls itself "deliberately small: five element kinds, seven operations, one ledger line, one adjudication line".

## Who writes it, and when

Written with the instrument. `build.sh` places it in `DROPS/D1/`, so it reaches the analyst's root at D1's first leg. It is not in the folder before then.

## Why it exists

Its opening: everything downstream of the return "works only if an adaptation is a typed operation on a named element of the global model, with evidence, and not a paragraph." Contract §2, "The model is typed", points to it; `ingest.py`, `distance.py` and `rebuild.py` cite its sections.

## Where

Source [aggregator/instrument/SCHEMA-adaptations.md](../../../aggregator/instrument/SCHEMA-adaptations.md); after D1, [in the analyst's folder](../../../aggregator/instrument/SCHEMA-adaptations.md).

Checked against: SCHEMA-adaptations.md, harness/build.sh, CONTRACT-aggregator.md §2, tools/ingest.py, tools/distance.py, tools/rebuild.py.

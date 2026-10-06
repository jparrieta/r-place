# Case-lead notes

branch B; threshold 500; items_in_window 1394; chars_by_people 96181

## What was hard

The hardest distinction was between conduct visible in the Reddit exchange and claims about the canvas. “We rekt them” is strong evidence that participants celebrated a joint defense, but it is not independent evidence about final pixels. Likewise, Smash-identified speakers' explanations support a negotiated account of the collision without proving responsibility for each alteration.

The local April Fools posts had to remain in scope as this subreddit's own conduct while staying explicitly separate from r/place. Image and link posts often left only titles and commenters' words, so I did not infer their visual content.

## Data problems

No one reader held the whole week. One coder read each of three arbitrary slices, so there is no agreement measure; an episode crossing 01|02 was read in parts. I built the account from pooled codes, slice cases, the forest, the fact files, and only then the counter-search. Relations crossing a boundary are correspondingly weaker than relations contained in a single fully read thread.

The Smash Discord is only partly visible: `dfqibo1` invites discussion there, and offers and claimed results return to Reddit, but its internal decisions do not. Deleted and removed bodies were not reconstructed. Several selected image or link posts retained citable titles but no visible image content. The collection cannot independently verify the eventual appearance of Hellfish or Homer.

## Anomalies and leads

The most consequential lead was the shift inside `630vvn` from an accusation against the Smash Bros Discord to denials, border explanations, an offer of protection, and a claimed joint defense. Later material did not independently confirm that settlement. Batch 03 contains no selected r/place practice even though it begins before placement ended; that is a scoped sequence, not evidence of a collective change of mind.

The pooled pointer rows retain batch-local `code_ids` for batch 02 (for example, pointer `p0011` names local `c0001` while the pooled code is `c0032`). The supplied fleet audit nevertheless passed pointer offsets. I did not alter this harness-produced append-only record.

## Fleet fact-file reviews

- Batch 01: struck no facts. Its three lexicon lines are unglossed participant terms with first-use item ids; it added no timeline lines.
- Batch 02: struck no facts. Its two timeline lines report edit markers with instrument times and item ids; its three lexicon lines are unglossed terms with first-use item ids.
- Batch 03: struck no facts. Its two timeline lines report edit markers with instrument times and item ids; its four lexicon lines are unglossed terms with first-use item ids.

## Grouping review

I consolidated in prescribed slice order. Batch 01 opened themes for the local April Fools practices, Hellfish planning and promotion, and opposing positions around keeping Homer alive. Batch 02 extended the Homer-repair theme and opened distinct themes for testing other pictures, negotiating the mile-long-nose collision, and requesting and celebrating allied defense. Batch 03 added no codes or themes.

I split a provisional broad “defending Homer” grouping because repairing the figure, negotiating blame and borders with Smash, and asking allies to fight red are different practices. After the counter-reading, I reviewed the grouping again and did not regroup: the contrary items qualified breadth and outcome but did not collapse those practical distinctions.

The two themes that nearly merged were `arguing over Homer's mile long nose with Smash` and `asking allies to fight red and celebrating together`; the first works out blame, borders, and coexistence, while the second requests reciprocal defense against a later red attack and claims a shared result.

The code I would defend hardest is `asking the Smash leader for help fending off red`. The thinnest I kept is `saying the design now looks like a buff Sidon`.

## Counter-reading record

Before searching, I wrote the competing account and failure conditions in `out/_lead_notes.md`: scattered picture-posting rather than sustained Homer coordination, with explicit refusal, renewed post-agreement conflict, or abandonment expected if the main reading was wrong. The searches scanned all 1,992 supplied items. Every returned item was opened with `read item`; no searched thread required full reading or changed disposition, and no late code was minted. The strongest contrary item was `dfprd86`, “THE VOID WILL LIVE ON.” The results narrowed coordination to a small set of Homer threads but did not overturn the explicit repair and reciprocal-help passages. Null results concern only the recorded corpus and the stated query scopes.

## How the reading held up

I did not work from memory of raw threads: in branch B I did not read them during fleet coding. I reread `out/ledger.md`, `out/_lead_notes.md`, all three slice cases, `package/codes_by_thread.md`, and the forest when consolidation began because the run had paused at the scheduler checkpoint after batch 03. Earlier slice details were not held as a single firsthand reading; the ledger and cases were the prescribed memory.

The run was interrupted and resumed after all three batches were collected and before consolidation. I resumed by reading the saved lead notes and ledger, then followed the ordered consolidation, first close, forest, audit, themes, counter-reading, account, and final checks. Slice 01 was less sharp than slice 03 at resumption until I reread its case and pooled codes; no raw thread was reopened for that reason. Counter-search hits were opened because the method required it, not because I had forgotten a thread.

## Complaints

The scheduler-required checkpoint asked me to start `notes.md` before the contract's end-writing stage, whereas the base contract says to write it once at the end. I preserved the checkpoint record and replaced it with this complete final note at step 7. The collected ledger truncates several copied `[unresolved]` episode lines mid-sentence; I therefore used the complete slice cases rather than treating those clipped ledger lines as evidence.

The branch-B division makes the requested case-wide chronology possible but inherently weaker: no person read both ends of the week. The forest preserves sequence, not causation, and the account says so.

Final preflight exposed a C5 instrument conflict. It demands exclusion citations for 21 threads even though the openings instrument shows that every one has fewer than ten in-window items: `62iaem`, `62gi65`, `62fdd0`, `62egcd`, `62cxvv`, `62gefq`, `62dvhr`, `61z6kc`, `624nvn`, `62dxyu`, `62d2sl`, `62ctxv`, `61s6o6`, `62zvkz`, `635qn2`, `6372hs`, `637x15`, `63audd`, `63d68t`, `63e4z6`, and `63ewmj`. The first thirteen opened outside the window and have only 0–8 in-window comments; the remaining eight have an in-window opener plus 0–8 comments, still below ten items. C5 appears to use whole-thread size from `out/_read_index.json` while labelling its test “IN-WINDOW.” The research contract triggers citations only at ten in-window items. Append-only `emit.thread` refuses a second disposition, so this false-positive set cannot be repaired through the documented instrument without breaching the contract or writing into coder directories. C4's one orphan code, `c0029`, was repaired by appending it to `t01`; all other checks pass.

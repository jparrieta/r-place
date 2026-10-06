from emit import Emit


def R(a, b):
    return list(range(a, b + 1))


themes = {
    "giveaway": {
        "label": "Chasing and doubting a joke giveaway",
        "note": "Participants compete for a possible prize while testing whether the removed-body giveaway will deliver; they vary between strategic upvoting, praise, skepticism, self-promotion, and deliberately incongruous joking.",
        "codes": R(1, 12),
    },
    "hand_building": {
        "label": "Drawing and repairing Bitcoin marks by hand",
        "note": "Participants turn coordinates, templates, outlines, pixel corrections, relocation, and handoffs into visible Bitcoin marks; what varies is whether they start over, repair an existing image, explain placement, or propose a larger form.",
        "codes": [13, 14, 16, 17, 18, 20, 25, 28, 31, 36, 37, 39, 52, 53, 54, 155, 211, 228, 229, 230, 233, 258, 284, 285, 314, 347, 399, 425, 428],
    },
    "defending": {
        "label": "Rallying defenders and holding canvas ground",
        "note": "Participants recruit help, report for duty, repair attacks, hold orange territory, repel named incursions, and expand after local successes; what varies is whether defense means preserving a mark, taking space, or redirecting effort away from redesign.",
        "codes": [15, 19, 21, 26, 29, 30, 32, 34, 108, 109, 110, 113, 122, 123, 124, 176, 180, 181, 201, 202, 203, 204, 205, 206, 207, 208, 209, 232, 243, 256, 281, 287, 290, 291, 292, 302, 311, 312, 313, 316, 318, 349, 351, 376, 397, 421],
    },
    "negotiating": {
        "label": "Negotiating borders and passage with neighbours",
        "note": "Participants ask neighbouring pictures to move, offer passage, define walls and borders, seek treaties and alliances, or refuse concessions; accommodation ranges from rainbow integration and CaveStory borders to open rejection of France, Italy, and other claims.",
        "codes": [24, 111, 112, 115, 116, 117, 118, 120, 151, 152, 153, 154, 156, 160, 161, 163, 164, 165, 166, 167, 168, 170, 171, 172, 173, 174, 177, 178, 179, 184, 213, 247, 249, 251, 257, 280, 286, 288, 294, 303, 306, 317, 319, 320] + R(321, 340) + [403, 404],
    },
    "automation": {
        "label": "Automating placement and reconciling script versions",
        "note": "Participants distribute scripts, tutorials, alt-account methods, inspection advice, staged priorities, and fixes; automation varies between amplifying defense and producing obsolete or competing versions that overwrite one another.",
        "codes": [114, 121, 128, 132, 148, 149, 150, 235, 236, 237, 238, 239, 241, 242, 244, 245, 248, 250, 252, 253, 254, 255, 262, 263, 264, 268, 277, 278, 279, 307, 308, 358, 360, 361, 362, 368, 373, 374, 379, 380, 381, 382, 391, 392, 398, 400, 401, 402, 427],
    },
    "design_coordination": {
        "label": "Choosing designs and moving coordination between venues",
        "note": "Participants compare fonts, colors, borders, locations and priorities while routing decisions among Reddit threads, Discord, Slack, and r/BitcoinPlace; what varies is whether a reported consensus settles anything or immediately meets another design objection.",
        "codes": [125, 126, 127, 183, 234, 246, 259, 260, 265, 266, 267, 295, 296, 305, 309, 310, 315, 348, 350, 352, 353, 354, 355, 356, 357, 359, 363, 364, 365, 366, 367, 369, 370, 371, 372, 375, 377, 378, 383, 384, 385, 387, 389, 390, 393, 394, 395, 396],
    },
    "canvas_language": {
        "label": "Putting Bitcoin disputes and slogans onto the canvas",
        "note": "Participants make block size, SegWit, forks, consensus, HODL, flags, and Bitcoin identity into canvas proposals and jokes; what varies is whether the language recruits real work, mocks a faction, or interprets conflict already under way.",
        "codes": [22, 23, 49, 51, 147, 157, 162, 169, 175, 182, 210, 212, 240, 261, 276, 282, 283, 293, 304, 388, 405, 447],
    },
    "april_fools": {
        "label": "Staging April Fools claims and spotting the trick",
        "note": "Participants publish fake deals, hacks, forks, news, deities, and corporate or mining stories, then identify, praise, condemn, or elaborate them; what varies is whether the trick lands, becomes factional argument, or remains playful parody.",
        "codes": [38] + R(40, 48) + R(55, 69) + [103, 106, 107, 133, 134, 135, 136, 137, 139, 140, 141, 142, 143, 144, 158, 185, 186, 187, 188, 189, 190] + R(192, 200) + R(269, 275),
    },
    "expert_flair": {
        "label": "Wearing expert flair to joke and argue",
        "note": "Participants notice, test, celebrate, and misunderstand the room-wide Bitcoin Expert flair, then use the bestowed expertise to stage badges, predictions, and substantive scaling positions; recognition of the joke varies across the exchanges.",
        "codes": R(72, 102) + [104, 105, 138, 145, 146, 159, 191] + R(214, 227),
    },
    "attribution": {
        "label": "Blaming pixel changers and checking the attribution",
        "note": "Participants identify apparent attackers from placements, histories, flags, or affiliations and answer those claims with requests for proof, defense accounts, and version-drift explanations; confidence ranges from territorial blame to explicit benefit of the doubt.",
        "codes": [33, 231, 289] + R(406, 415) + [436, 437, 444],
    },
    "side_projects": {
        "label": "Proposing side pictures and replacement canvases",
        "note": "Participants propose a wizard, Bruins conversion, clone, coin, rollercoaster figure, rocket, or another canvas; these projects vary between invitations with a helper, linked replacements, and proposals with no visible realization.",
        "codes": [27, 35, 50, 70, 71] + R(297, 301) + [416, 417, 418, 419],
    },
    "evaluation": {
        "label": "Appraising and retelling the finished canvas",
        "note": "Participants mark success and closure, praise labor, joke about damaged lettering, blame expansion or griefing, compare rivals, and retell the struggle; evaluations range from collective accomplishment and social experiment to relief, disappointment, and irony.",
        "codes": [119, 129, 130, 131, 386, 420, 422, 423, 424, 426] + R(439, 443) + [445, 446] + R(448, 480),
    },
    "price_thread": {
        "label": "Debating price around a logo joke",
        "note": "A commenter credits the r/place logo for a price return inside a thread otherwise redirecting market talk and disputing chart lines; the shared practice is the thread's price explanation and rebuttal, not canvas coordination.",
        "codes": R(341, 346),
    },
    "jobs_thread": {
        "label": "Seeking Bitcoin work and disputing the jobs venue",
        "note": "Participants refer a job seeker to a Bitcoin-paid-work subreddit, dispute whether it is maintained, rebuke one another, and close with an apology; the separate French-flag explanation is grouped with attribution rather than with the referral practice.",
        "codes": R(429, 435) + [438],
    },
}

all_numbers = [n for theme in themes.values() for n in theme["codes"]]
missing = sorted(set(range(1, 481)) - set(all_numbers))
duplicates = sorted(n for n in set(all_numbers) if all_numbers.count(n) > 1)
if missing or duplicates:
    raise SystemExit(f"theme allocation invalid; missing={missing}; duplicates={duplicates}")

batches = [
    ("01", 1, 12), ("03", 13, 39), ("04", 40, 54), ("05", 55, 71),
    ("06", 72, 102), ("07", 103, 107), ("09", 108, 132),
    ("10", 133, 158), ("11", 159, 184), ("12", 185, 268),
    ("13", 269, 301), ("14", 302, 320), ("15", 321, 346),
    ("17", 347, 388), ("18", 389, 419), ("19", 420, 427),
    ("20", 428, 438), ("21", 439, 457), ("23", 458, 480),
]

emit = Emit("out", corpus_path="coder_corpus.jsonl")
theme_ids = {}
for batch, low, high in batches:
    for key, theme in themes.items():
        code_ids = [f"c{n:04d}" for n in theme["codes"] if low <= n <= high]
        if not code_ids:
            continue
        if key not in theme_ids:
            theme_ids[key] = emit.theme(theme["label"], theme["note"], code_ids, regrouped_from=None)
        else:
            emit.theme_add(theme_ids[key], code_ids)

print({"themes": theme_ids, "codes_assigned": len(all_numbers)})

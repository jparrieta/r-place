T3-002 | T3-005  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  decide_when_both naming T3-005: a call to defend a work under attack is T3-005 when the defence leads.
  discriminator against T3-005: Is the call to build or finish (T3-002), or to defend against an attack under way (T3-005)?

T3-005  defending the work against attackers
  must_show: An attack on the room's work and the room's answer: alarms, calls to defend or fight back, holding the line, reports of an attack repelled.
  discriminator against T3-002: Is the call to build or finish (T3-002), or to defend against an attack under way (T3-005)?


T3-002 | T3-016  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  discriminator against T3-016: Is the event explained (T3-016), or are members called to come and place (T3-002)?

T3-016  explaining what the canvas is
  must_show: Questions or answers about the event itself: what r/place is, one pixel every few minutes, how to pick a colour and place, why subs are making pictures, the heat map or the rules of the event.
  must_not_show naming T3-002: calls to come and place (T3-002)
  discriminator against T3-002: Is the event explained (T3-016), or are members called to come and place (T3-002)?


T3-002 | T3-033  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  decide_when_both naming T3-033: When a theme holds two or more of these acts (an idea of what to make offered to the room, T3-033
  decide_when_both naming T3-033: else T3-002 when the mark was already chosen, T3-033 when it was not.
  discriminator against T3-033: Count the concepts of each: is the larger share an idea of what to make offered to the room (T3-033), or hands called to a mark already chosen (T3-002)? The opening post does not lead because it comes first.

T3-033  proposing the room's mark
  must_show: An idea of what the room should put on the canvas, offered to the room: 'we should put X on r/place', 'let's make a ...', a proposal with or without a picture; slogans and symbols proposed as the room's mark included.
  must_not_show naming T3-002: Calls for hands to a mark already chosen (T3-002)
  decide_when_both naming T3-002: hands called to place, T3-002
  decide_when_both naming T3-002: else T3-002 when the mark was already chosen, T3-033 when it was not.
  is_not naming T3-002: A call for help on a picture already started (T3-002).
  discriminator against T3-002: Count the concepts of each: is the larger share an idea of what to make offered to the room (T3-033), or hands called to a mark already chosen (T3-002)? The opening post does not lead because it comes first.


T3-002 | T3-038  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  decide_when_both naming T3-038: the work placed and its progress reported, T3-038), count the concepts of each: the act with the most concepts of its own is primary, and another is added under rule 0 only with concepts of its own.
  decide_when_both naming T3-038: On a tie, T3-038 when the work was placed
  discriminator against T3-038: Count the concepts of each: is the larger share the work placed and its progress reported (T3-038), or hands called for it (T3-002)? An opening call does not lead because it comes first.

T3-038  building and reporting the mark
  must_show: Placing the mark and reports of its state: started, coordinates of the work in progress, half done, almost finished, the parts done and left.
  must_not_show naming T3-002: Calls for hands (T3-002)
  decide_when_both naming T3-002: hands called to place, T3-002
  decide_when_both naming T3-002: else T3-002 when the mark was already chosen, T3-033 when it was not.
  discriminator against T3-002: Count the concepts of each: is the larger share the work placed and its progress reported (T3-038), or hands called for it (T3-002)? An opening call does not lead because it comes first.


T3-002 | T3-044  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  must_not_show naming T3-044: welcoming canvas visitors into the sub (T3-044).
  discriminator against T3-044: Are the room's own members called to come and place (T3-002), or outsiders brought to the sub by its mark and welcomed (T3-044)?

T3-044  recruiting canvas visitors
  must_show: Newcomers led to the sub by its canvas mark: visitors saying they came from r/place, members welcoming them, the sub's name placed so that viewers find it, subscriber growth counted.
  must_not_show naming T3-002: calling members to place (T3-002).
  discriminator against T3-002: Are the room's own members called to come and place (T3-002), or outsiders brought to the sub by its mark and welcomed (T3-044)?


T3-002 | T3-051  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  discriminator against T3-051: Are members asked to vote a post up (T3-051), or to come and place (T3-002)?

T3-051  pushing posts up the rankings
  must_show: A drive for votes: members asked to upvote a post so that it rises (to be seen by placers on r/place, to reach the front page, to make an image the first search result), or bargains of the form 'if this gets N upvotes'.
  must_not_show naming T3-002: Calling members to place with no votes asked (T3-002)
  decide_when_both naming T3-002: A call to place that also asks for upvotes so the call is seen: T3-002 primary, T3-051 added when the vote drive has a concept of its own.
  discriminator against T3-002: Are members asked to vote a post up (T3-051), or to come and place (T3-002)?


T3-002 | T3-062  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  must_not_show naming T3-062: Calls aimed at other subs (T3-062) or at another canvas room as a room (T3-084)
  discriminator against T3-062: Are the room's own members called (T3-002), or the members of other subs (T3-062)?

T3-062  recruiting kindred subs to help
  must_show: The room's own call for hands, made by its members and carried into other subs or communities, or proposed: 'ask r/X for help', threads opened in other subs, recruiting from related communities.
  must_not_show naming T3-002: Calls to the room's own members (T3-002)
  discriminator against T3-002: Are the room's own members called (T3-002), or other subs' members (T3-062)?


T3-002 | T3-065  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  must_not_show naming T3-065: The national flag as the room's mark carries T3-065
  is_not naming T3-065: Calls to build the room's national flag (T3-065).
  discriminator against T3-065: Is the work a flag of the land the room is named for or speaks for, a flag built in r/guatemala being Guatemala's unless its concepts name another (T3-065), or any other picture (T3-002)?

T3-065  building the homeland's flag
  must_show: The flag of the room's own land (a nation, a state, a region or county) built as the room's mark: calls to make it, its proportions, its spot, its repair. Announcements that the flag has begun or is up, and calls for hands to it, go here too.
  must_not_show naming T3-002: Calls for hands to any other picture (T3-002)
  decide_when_both naming T3-002: The flag of the room's land as its mark is T3-065, calls for hands to any other picture T3-002.
  discriminator against T3-002: Is the work a flag of the land the room is named for or speaks for, a flag built in r/guatemala being Guatemala's unless its concepts name another (T3-065), or any other picture (T3-002)?


T3-002 | T3-070  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  decide_when_both naming T3-070: A call made mostly of coordinates or a template is T3-070, with T3-002 added when the call has concepts of its own
  discriminator against T3-070: Is the call itself the doing (T3-002), or the coordinates and templates that tell placers what to place (T3-070)?

T3-070  sharing coordinates, templates and how-to
  must_show: Coordinates, templates, grid images, overlays, guides, colour plans, border plans, timings or how-to posted or updated for placers to follow by hand.
  decide_when_both naming T3-002: A call to place that carries coordinates: T3-070 when the directions lead, T3-002 when the call does
  discriminator against T3-002: Is the doing the directions (T3-070), or the call for hands (T3-002)?


T3-002 | T3-084  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  must_not_show naming T3-084: Calls aimed at other subs (T3-062) or at another canvas room as a room (T3-084)
  discriminator against T3-084: Does a member of this room call its own members to place (T3-002), or is help asked between rooms, another room's call reaching this room's members here included (T3-084)?

T3-084  asking other rooms for help
  must_show: A request for help with the work between canvas rooms, in the record of either room: the room asking another room, or another room's request or call for hands as it arrives in the room's threads, addressed to the room as a group or to its members: 'we could use your help', 'help us please', calls for reinforcements addressed to another room.
  discriminator against T3-002: Does a member of this room call its own members to place (T3-002), or is help asked between rooms, another room's call reaching this room's members here included (T3-084)?


T3-002 | T3-104  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  discriminator against T3-104: Are people asked to place (T3-002), or those already placing cheered on (T3-104)?

T3-104  cheering the builders on
  must_show: Encouragement aimed at builders during the work: 'keep going', 'nice work team', 'good luck', praise from members or from outsiders who may not place themselves.
  must_not_show naming T3-002: Calls for more hands (T3-002)
  discriminator against T3-002: Are people asked to come and place (T3-002), or those placing encouraged (T3-104)?


T3-002 | T3-144  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  discriminator against T3-144: Are hands called for in the open (T3-002), or recruited only inside friendly communities so the work draws no attackers (T3-144)?

T3-144  recruiting quietly to avoid attackers
  must_show: Recruiting held back or kept inside friendly communities because publicity might bring attackers; a small presence chosen for safety.
  must_not_show naming T3-002: calling for hands in the open (T3-002, T3-062).
  discriminator against T3-002: Are hands called for in the open (T3-002), or recruited only inside friendly communities so the work draws no attackers (T3-144)?


T3-002 | T3-167  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  discriminator against T3-167: Is a time set for placing together (T3-167), or hands called with no time (T3-002)?

T3-167  timing a mass placement together
  must_show: A time fixed or proposed for members to place together: a start time so that a few are not overrun, a scheduled push, a jointly timed ending.
  must_not_show naming T3-002: Calls to place with no time set (T3-002)
  decide_when_both naming T3-002: A call with a time: T3-167 when the time is the point, T3-002 otherwise.
  discriminator against T3-002: Is a time set for placing together (T3-167), or hands called with no time (T3-002)?


T3-002 | T3-169  (scheme_v2.jsonl; stale)

T3-002  calling members in to place
  must_show: Calls to the room's members, or to placers not yet gathered into a group, to come and place: 'come help', 'we need more people', 'everyone join', rallies to build, finish or repair a work, posts asking who is in.
  must_not_show naming T3-169: writing the sub's name carries T3-169.
  discriminator against T3-169: Is the work the sub's name written on the canvas (T3-169), whatever the call or report about it, or any other picture called for (T3-002)?

T3-169  signing the sub's name
  must_show: The sub's name, or a short form of it, written on the canvas; the choice whether to write it; keeping it there.
  discriminator against T3-002: Is the work the sub's name written on the canvas (T3-169), whatever the call or report about it, or any other picture called for (T3-002)?


T3-010 | T3-084  (scheme_v2.jsonl; stale)

T3-010  settling borders with neighbours
  must_show: A deal over lines and space between neighbouring works with no fight to end: borders agreed or asked for, shifts of a few pixels, overlaps accepted or refused, space shared.
  discriminator against T3-084: Is a line or space settled between neighbours (T3-010), or another room asked, as a group, to help with the work (T3-084)?

T3-084  asking other rooms for help
  must_show: A request for help with the work between canvas rooms, in the record of either room: the room asking another room, or another room's request or call for hands as it arrives in the room's threads, addressed to the room as a group or to its members: 'we could use your help', 'help us please', calls for reinforcements addressed to another room.
  decide_when_both naming T3-010: A request inside a deal: T3-010 primary when the deal leads, T3-084 added when the request has concepts of its own.
  discriminator against T3-010: Is a line or space settled between neighbours (T3-010), or another room asked, as a group, to help with the work (T3-084)?


T3-011 | T3-084  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: The room's members helping another room's work, or called to it by the room's own members: 'come help the farm at r/X', 'I'm helping r/Y', pixels sent to a neighbour's defence.
  must_not_show naming T3-084: asking for help (T3-084)
  discriminator against T3-084: Is help asked for (T3-084), or sent (T3-011)?

T3-084  asking other rooms for help
  must_show: A request for help with the work between canvas rooms, in the record of either room: the room asking another room, or another room's request or call for hands as it arrives in the room's threads, addressed to the room as a group or to its members: 'we could use your help', 'help us please', calls for reinforcements addressed to another room.
  discriminator against T3-011: Is help asked for (T3-084), or sent (T3-011)?


T3-035 | T3-084  (scheme_v2.jsonl; stale)

T3-035  asking a host for space
  must_show: A request for space or permission addressed to the room that holds it: 'permission to make X in your lot', 'can we share and let us slip into that space'.
  must_not_show naming T3-084: asking for help with the work (T3-084)
  is_not naming T3-084: Asking another room to send hands to help build (T3-084).
  discriminator against T3-084: Is space asked for (T3-035), or hands to help the work (T3-084)?

T3-084  asking other rooms for help
  must_show: A request for help with the work between canvas rooms, in the record of either room: the room asking another room, or another room's request or call for hands as it arrives in the room's threads, addressed to the room as a group or to its members: 'we could use your help', 'help us please', calls for reinforcements addressed to another room.
  must_not_show naming T3-035: asking for space (T3-035)
  discriminator against T3-035: Is help with the work asked (T3-084), or space (T3-035)?


T3-062 | T3-084  (scheme_v2.jsonl; stale)

T3-062  recruiting kindred subs to help
  must_show: The room's own call for hands, made by its members and carried into other subs or communities, or proposed: 'ask r/X for help', threads opened in other subs, recruiting from related communities.
  must_not_show naming T3-084: one canvas room asking another, as a group, to help or make room (T3-084)
  decide_when_both naming T3-084: A request to an organised canvas group, room to room, is T3-084
  discriminator against T3-084: Is another sub's membership asked for hands (T3-062), or another canvas group asked, as a group, to help with this room's work (T3-084)?

T3-084  asking other rooms for help
  must_show: A request for help with the work between canvas rooms, in the record of either room: the room asking another room, or another room's request or call for hands as it arrives in the room's threads, addressed to the room as a group or to its members: 'we could use your help', 'help us please', calls for reinforcements addressed to another room.
  must_not_show naming T3-062: Carrying a call for hands into other subs' membership (T3-062)
  is_not naming T3-062: Posting a call for hands in a kindred sub (T3-062).
  discriminator against T3-062: Is another sub's membership asked for hands (T3-062), or another canvas room asked as a group (T3-084)?


T3-084 | T3-115  (scheme_v2.jsonl; stale)

T3-084  asking other rooms for help
  must_show: A request for help with the work between canvas rooms, in the record of either room: the room asking another room, or another room's request or call for hands as it arrives in the room's threads, addressed to the room as a group or to its members: 'we could use your help', 'help us please', calls for reinforcements addressed to another room.
  discriminator against T3-115: Is help asked (T3-084), or a request refused (T3-115)?

T3-115  turning away another room's request
  must_show: A request from another room or its members refused or sent back: 'no', 'we can not offer our assistance', 'post it on your own sub', a refusal on grounds of rivalry.
  discriminator against T3-084: Is help asked (T3-084), or a request refused (T3-115)?


T3-084 | T3-151  (scheme_v2.jsonl; stale)

T3-084  asking other rooms for help
  must_show: A request for help with the work between canvas rooms, in the record of either room: the room asking another room, or another room's request or call for hands as it arrives in the room's threads, addressed to the room as a group or to its members: 'we could use your help', 'help us please', calls for reinforcements addressed to another room.
  must_not_show naming T3-151: help asked in return for help given (T3-151).
  discriminator against T3-151: Is help asked in return for help (T3-151), or asked outright (T3-084)?

T3-151  bartering help with neighbours
  must_show: Help offered or asked in return for help: 'we'll help you move if you maintain ours', 'repay the favour', maintenance traded for room.
  discriminator against T3-084: Is help asked in return for help (T3-151), or asked outright (T3-084)?


T3-014 | T3-015  (scheme_v2.jsonl; stale)

T3-014  moving planning into a chat
  must_show: A chat set up or named for the room's canvas work; invites posted or asked for; members sent there for plans, live direction or voice.
  discriminator against T3-015: Does the talk move out of Reddit into a chat (T3-014), or into one thread of the sub (T3-015)?

T3-015  routing canvas posts into megathreads
  must_show: Canvas talk gathered into one thread inside the sub: a moderator stickying a megathread, members asking for one, posts redirected or removed with a pointer to it, the plan kept in one visible place.
  must_not_show naming T3-014: Moving the planning out of the sub, to a chat or a new sub (T3-014, T3-090)
  discriminator against T3-014: Is the gathering place a thread inside the sub (T3-015), or a chat outside it (T3-014)?


T3-015 | T3-049  (scheme_v2.jsonl; stale)

T3-015  routing canvas posts into megathreads
  must_show: Canvas talk gathered into one thread inside the sub: a moderator stickying a megathread, members asking for one, posts redirected or removed with a pointer to it, the plan kept in one visible place.
  discriminator against T3-049: Is the scattering complained of with no gathering act (T3-049), or is the talk gathered into one thread (T3-015)?

T3-049  complaining the calls are scattered
  must_show: Complaints that the room lacks coordination: too many threads, coordinates or designs at once; no one keeping one plan up to date; members unsure where the work is.
  must_not_show naming T3-015: Gathering the talk into one thread (T3-015) or onto one template (T3-091) as an act
  decide_when_both naming T3-015: A complaint answered in the same theme by a megathread or a template: the act (T3-015, T3-091) is primary when it has more concepts, T3-049 otherwise.
  discriminator against T3-015: Is the scattering complained of with no gathering act (T3-049), or is the talk gathered into one thread (T3-015)?


T3-015 | T3-063  (scheme_v2.jsonl; stale)

T3-015  routing canvas posts into megathreads
  must_show: Canvas talk gathered into one thread inside the sub: a moderator stickying a megathread, members asking for one, posts redirected or removed with a pointer to it, the plan kept in one visible place.
  must_not_show naming T3-063: removals under the sub's rules with no pointer to a gathering thread (T3-063)
  decide_when_both naming T3-063: removals resting on other rules (karma, titles, relevance), or a bare removal that names no gathering thread, are T3-063.
  is_not naming T3-063: A moderator removing a canvas post because the canvas has ended (T3-063): nothing is gathered.
  discriminator against T3-063: Is the post sent to one gathering thread (T3-015), or removed or filtered under a standing rule with no such pointer (T3-063)?

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  must_not_show naming T3-015: Gathering canvas talk into one thread (T3-015)
  decide_when_both naming T3-015: Removing with a pointer to a gathering thread is T3-015
  is_not naming T3-015: A moderator stickying a megathread and asking for posts there (T3-015).
  discriminator against T3-015: Is the post removed under a standing rule (T3-063), or sent to one gathering thread (T3-015)?


T3-015 | T3-075  (scheme_v2.jsonl; stale)

T3-015  routing canvas posts into megathreads
  must_show: Canvas talk gathered into one thread inside the sub: a moderator stickying a megathread, members asking for one, posts redirected or removed with a pointer to it, the plan kept in one visible place.
  must_not_show naming T3-075: complaining about the flood without asking for a place to gather it (T3-075).
  discriminator against T3-075: Is one thread asked for so the work can go on in order (T3-015), or are members objecting that canvas posts crowd the sub (T3-075)?

T3-075  objecting to the canvas flood
  must_show: Members complaining that r/place posts flood the sub, are spam or off-topic, or crowd out its news and subject; asking that they stop, be condensed into one post or be removed.
  must_not_show naming T3-015: Moderators applying a rule (T3-063) or gathering posts (T3-015) with no members objecting
  discriminator against T3-015: Are members objecting to the flood (T3-075), or is the talk being gathered into one thread so the work can go on (T3-015)?


T3-015 | T3-090  (scheme_v2.jsonl; stale)

T3-015  routing canvas posts into megathreads
  must_show: Canvas talk gathered into one thread inside the sub: a moderator stickying a megathread, members asking for one, posts redirected or removed with a pointer to it, the plan kept in one visible place.
  must_not_show naming T3-090: Moving the planning out of the sub, to a chat or a new sub (T3-014, T3-090)
  discriminator against T3-090: One thread in the sub (T3-015), or a new sub made for the canvas work (T3-090)?

T3-090  opening a canvas sub
  must_show: A new subreddit made for the canvas work (a place sub for the room or nation), asked for, or used: canvas posts redirected to it, members told to go there.
  must_not_show naming T3-015: One thread inside the sub (T3-015)
  discriminator against T3-015: Is the canvas talk sent to a new sub (T3-090), or to one thread in the old one (T3-015)?


T3-015 | T3-107  (scheme_v2.jsonl; stale)

T3-015  routing canvas posts into megathreads
  must_show: Canvas talk gathered into one thread inside the sub: a moderator stickying a megathread, members asking for one, posts redirected or removed with a pointer to it, the plan kept in one visible place.
  discriminator against T3-107: NONE

T3-107  keeping planning in the thread
  must_show: A choice or agreement to coordinate in the thread rather than in a chat, or a chat tried and failed so that the thread carried the work.
  is_not naming T3-015: Gathering canvas talk into a megathread (T3-015).
  discriminator against T3-015: NONE


T3-015 | T3-140  (scheme_v2.jsonl; stale)

T3-015  routing canvas posts into megathreads
  must_show: Canvas talk gathered into one thread inside the sub: a moderator stickying a megathread, members asking for one, posts redirected or removed with a pointer to it, the plan kept in one visible place.
  discriminator against T3-140: Is the thread only gathering canvas talk (T3-015), or do the moderators also say the work is not the sub's (T3-140)?

T3-140  moderators disowning the canvas work
  must_show: Moderators stating that the sub as such takes no part in the canvas work: no official project, no brigading in the sub's name, members free to organise on their own.
  must_not_show naming T3-015: Moderators gathering or removing canvas posts without saying the work is not the sub's (T3-015, T3-063)
  decide_when_both naming T3-015: A sticky that gathers the canvas talk and disowns the work is T3-015 primary with T3-140 under rule 0.
  discriminator against T3-015: Is the thread only gathering canvas talk (T3-015), or do the moderators also say the work is not the sub's (T3-140)?


T3-015 | T3-197  (scheme_v2.jsonl; stale)

T3-015  routing canvas posts into megathreads
  must_show: Canvas talk gathered into one thread inside the sub: a moderator stickying a megathread, members asking for one, posts redirected or removed with a pointer to it, the plan kept in one visible place.
  discriminator against T3-197: Is the canvas talk moved or shaped because the creator of the room's subject asked (T3-197), or gathered into one thread with no creator's wish behind it (T3-015)?

T3-197  heeding the creator's wishes
  must_show: The wishes of the person the sub is about (an author, an artist) passed on and followed in the canvas work: not using their name, keeping canvas talk out of their sub, not pinging them.
  must_not_show naming T3-015: Moderators' rules for canvas posts with no creator's wish behind them (T3-063, T3-015).
  is_not naming T3-015: Moderators gathering canvas talk into a megathread for order (T3-015).
  discriminator against T3-015: Is the canvas talk moved or shaped because the creator of the room's subject asked (T3-197), or gathered into one thread with no creator's wish behind it (T3-015)?


T3-023 | T3-063  (scheme_v2.jsonl; stale)

T3-023  running an April Fools takeover
  must_show: A change made to a whole sub for April Fools, announced or staged by its moderators or by a sub acting together: a new name, look, subject, rules or flairs, a fake sale or takeover by a character, company or rival sub, or one sub taking over another for the day; and members playing along inside it.
  is_not naming T3-063: A moderator removing canvas posts under the sub's ordinary rules on 1 April (T3-063): nothing about the sub was changed for the joke.
  discriminator against T3-063: NONE

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  discriminator against T3-023: NONE


T3-032 | T3-063  (scheme_v2.jsonl; stale)

T3-032  objecting to April Fools posts
  must_show: Objection to the sub's April Fools content carried by three or more concepts: calling the jokes unfunny, stale, hurtful or disruptive; asking members or moderators to stop them or take them down; warning others not to post them.
  discriminator against T3-063: Are members objecting (T3-032), or moderators removing posts under the sub's rules (T3-063)?

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  discriminator against T3-032: Are members objecting (T3-032), or moderators removing posts under the sub's rules (T3-063)?


T3-063 | T3-075  (scheme_v2.jsonl; stale)

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  must_not_show naming T3-075: members objecting to the flood with no moderator act (T3-075).
  discriminator against T3-075: A removal or filter applied (T3-063), or members complaining about canvas posts (T3-075)?

T3-075  objecting to the canvas flood
  must_show: Members complaining that r/place posts flood the sub, are spam or off-topic, or crowd out its news and subject; asking that they stop, be condensed into one post or be removed.
  must_not_show naming T3-063: Moderators applying a rule (T3-063) or gathering posts (T3-015) with no members objecting
  discriminator against T3-063: A removal or filter applied (T3-063), or members complaining about canvas posts (T3-075)?


T3-063 | T3-118  (scheme_v2.jsonl; stale)

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  discriminator against T3-118: Is a removal contested (T3-063), or a loss laid at the moderators' door (T3-118)?

T3-118  blaming moderators for a loss
  must_show: Blame for the room's loss or failure laid on moderators or admins: their April Fools change, their removals, denied requests for help, the canvas said to be rigged.
  must_not_show naming T3-063: objections to a removal with no loss in view (T3-063, T3-185).
  is_not naming T3-063: Contesting a single removal under the sub's rules (T3-063).
  discriminator against T3-063: Is a removal contested (T3-063), or a loss laid at the moderators' door (T3-118)?


T3-063 | T3-121  (scheme_v2.jsonl; stale)

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  discriminator against T3-121: Is a post removed under the sub's rules (T3-063), or a member excluded as a sanction (T3-121)?

T3-121  excluding the room's own vandals
  must_show: Exclusion used as a sanction against the room's own members: bans from the Discord or the sub, kicking, shunning a 'traitor', members reported so moderators throw them out, such a ban challenged or reversed.
  must_not_show naming T3-063: posts removed under the sub's rules (T3-063)
  is_not naming T3-063: A moderator removing a post that breaks the sub's rules (T3-063).
  discriminator against T3-063: Is a post removed under the sub's rules (T3-063), or a member excluded as a sanction (T3-121)?


T3-063 | T3-140  (scheme_v2.jsonl; stale)

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  discriminator against T3-140: Do moderators say the canvas work is not the sub's (T3-140), or remove or filter canvas posts under the sub's rules without saying so (T3-063)?

T3-140  moderators disowning the canvas work
  must_show: Moderators stating that the sub as such takes no part in the canvas work: no official project, no brigading in the sub's name, members free to organise on their own.
  must_not_show naming T3-063: Moderators gathering or removing canvas posts without saying the work is not the sub's (T3-015, T3-063)
  discriminator against T3-063: Do moderators say the canvas work is not the sub's (T3-140), or remove or filter canvas posts under the sub's rules without saying so (T3-063)?


T3-063 | T3-182  (scheme_v2.jsonl; stale)

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  discriminator against T3-182: Posts removed for breaking the sub's rules (T3-063), or members shutting down bigotry in a chat (T3-182)?

T3-182  shutting down bigotry in chat
  must_show: Bigotry in the room's talk answered: anti-trans speech shut down in the Discord, a post removed for a slur, racist claims rebutted.
  discriminator against T3-063: Posts removed for breaking the sub's rules (T3-063), or members shutting down bigotry in a chat (T3-182)?


T3-063 | T3-184  (scheme_v2.jsonl; stale)

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  discriminator against T3-184: NONE

T3-184  pausing the sub's usual events
  must_show: A recurring event of the sub (a game among members, a contest, a daily thread) held off because of the canvas, or resumed once the canvas posts end.
  is_not naming T3-063: Removing canvas posts so that usual threads stay visible (T3-063).
  discriminator against T3-063: NONE


T3-063 | T3-185  (scheme_v2.jsonl; stale)

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  must_not_show naming T3-185: changing the rules themselves (T3-185)
  discriminator against T3-185: Are the rules applied as they stand (T3-063), or made, dropped or argued as a change (T3-185)?

T3-185  changing the sub's posting rules
  must_show: A change to the sub's rules or their enforcement meant to hold: allowing or banning a kind of post for a time, new flairs or filters, a rule dropped or added, members debating what the rules should be.
  must_not_show naming T3-063: Applying the rules as they stand (T3-063)
  is_not naming T3-063: An automatic removal under an existing rule (T3-063).
  discriminator against T3-063: Is a standing rule applied (T3-063), or is a rule made, dropped or argued (T3-185)?


T3-063 | T3-197  (scheme_v2.jsonl; stale)

T3-063  removing canvas posts by rule
  must_show: Canvas posts handled under the sub's standing rules: removals for titles, links, karma, relevance, duplicates or politics; automatic filters; required flairs; members asking what the rules allow or contesting a removal.
  discriminator against T3-197: Are canvas posts handled under the sub's rules (T3-063), or shaped by the creator's wish (T3-197)?

T3-197  heeding the creator's wishes
  must_show: The wishes of the person the sub is about (an author, an artist) passed on and followed in the canvas work: not using their name, keeping canvas talk out of their sub, not pinging them.
  must_not_show naming T3-063: Moderators' rules for canvas posts with no creator's wish behind them (T3-063, T3-015).
  discriminator against T3-063: Are canvas posts handled under the sub's rules (T3-063), or shaped by the creator's wish (T3-197)?


T3-032 | T3-075  (scheme_v2.jsonl; stale)

T3-032  objecting to April Fools posts
  must_show: Objection to the sub's April Fools content carried by three or more concepts: calling the jokes unfunny, stale, hurtful or disruptive; asking members or moderators to stop them or take them down; warning others not to post them.
  must_not_show naming T3-075: objections to canvas posts (T3-075).
  discriminator against T3-075: Are the posts objected to April Fools jokes (T3-032) or canvas posts flooding the sub (T3-075)?

T3-075  objecting to the canvas flood
  must_show: Members complaining that r/place posts flood the sub, are spam or off-topic, or crowd out its news and subject; asking that they stop, be condensed into one post or be removed.
  must_not_show naming T3-032: objecting to April Fools posts (T3-032).
  discriminator against T3-032: Are the unwanted posts canvas posts (T3-075) or April Fools jokes (T3-032)?


T3-037 | T3-075  (scheme_v2.jsonl; stale)

T3-037  arguing the canvas's worth
  must_show: The canvas weighed as a whole: a waste of time, stupid, pointless; or fun, art, a social experiment worth doing; a bare dismissal of a call to place.
  must_not_show naming T3-075: Complaints that canvas posts crowd the sub (T3-075)
  decide_when_both naming T3-075: A dismissal of the canvas inside a complaint about posts: T3-075 when the posts are the target, T3-037 when the canvas itself is.
  is_not naming T3-075: A member asking that canvas posts go into one megathread (T3-075).
  discriminator against T3-075: Is the canvas itself judged worthless or worthwhile (T3-037), or are its posts objected to in the sub (T3-075)?

T3-075  objecting to the canvas flood
  must_show: Members complaining that r/place posts flood the sub, are spam or off-topic, or crowd out its news and subject; asking that they stop, be condensed into one post or be removed.
  must_not_show naming T3-037: judging the canvas itself worthless (T3-037)
  decide_when_both naming T3-037: A complaint that the canvas is pointless, not that it floods the sub, is T3-037.
  is_not naming T3-037: A member calling the canvas a waste of time with no word on the sub's space (T3-037).
  discriminator against T3-037: Is the complaint that canvas posts crowd the sub (T3-075), or that the canvas is not worth doing (T3-037)?


T3-075 | T3-189  (scheme_v2.jsonl; stale)

T3-075  objecting to the canvas flood
  must_show: Members complaining that r/place posts flood the sub, are spam or off-topic, or crowd out its news and subject; asking that they stop, be condensed into one post or be removed.
  discriminator against T3-189: Is the complaint about canvas posts crowding the sub (T3-075), or about the people the mark brings in (T3-189)?

T3-189  fearing newcomers the mark draws
  must_show: Worry about the newcomers the mark draws: an influx that will swamp the sub or its site, newcomers who ignore the rules, the sub said to have gone downhill since.
  must_not_show naming T3-075: objecting that canvas posts flood the sub (T3-075).
  discriminator against T3-075: Is the complaint about canvas posts crowding the sub (T3-075), or about the people the mark brings in (T3-189)?


T3-004 | T3-020  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  must_not_show naming T3-020: choosing where it goes (T3-020)
  decide_when_both naming T3-020: Design argued and spot chosen in one theme, each in concepts of its own: both are placed, the larger primary and the other beside it (the spot is T3-020).
  discriminator against T3-020: Is the question what it looks like (T3-004), or where it goes (T3-020)?

T3-020  choosing a canvas spot
  must_show: Where the mark should go: free space found, corners and neighbours weighed, a location announced or changed before or while building.
  discriminator against T3-004: Is the question where it goes (T3-020), or what it looks like (T3-004)?


T3-004 | T3-033  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  must_not_show naming T3-033: Proposing that the room make a mark at all (T3-033)
  discriminator against T3-033: Is a mark proposed to the room (T3-033), or is its look worked out (T3-004)?

T3-033  proposing the room's mark
  must_show: An idea of what the room should put on the canvas, offered to the room: 'we should put X on r/place', 'let's make a ...', a proposal with or without a picture; slogans and symbols proposed as the room's mark included.
  must_not_show naming T3-004: the design of a chosen mark worked out (T3-004).
  discriminator against T3-004: Is a mark proposed (T3-033), or a chosen mark's look worked out (T3-004)?


T3-004 | T3-038  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  discriminator against T3-038: Is the mark being placed and its progress reported (T3-038), or its look argued and corrected against the plan (T3-004)?

T3-038  building and reporting the mark
  must_show: Placing the mark and reports of its state: started, coordinates of the work in progress, half done, almost finished, the parts done and left.
  must_not_show naming T3-004: the design argued (T3-004)
  discriminator against T3-004: Is the mark being placed and its progress reported (T3-038), or its look argued and corrected against the plan (T3-004)?


T3-004 | T3-041  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  must_not_show naming T3-041: a bigger or second piece (T3-041).
  discriminator against T3-041: Is the mark's own design settled (T3-004), or a bigger or second piece added (T3-041)?

T3-041  extending the room's work
  must_show: Proposals or work to add to the room's existing mark or to make another: a next piece, a bigger version, additions around the first.
  decide_when_both naming T3-004: Additions argued as design: T3-004 when the existing mark's look is settled, T3-041 when a new piece or an enlargement is added.
  discriminator against T3-004: Is the existing mark's look settled (T3-004), or a new piece or enlargement added (T3-041)?


T3-004 | T3-055  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  must_not_show naming T3-055: reshaping the mark against tampering (T3-055)
  discriminator against T3-055: Is the look changed for its own sake (T3-004), or to make the mark harder to tamper with (T3-055)?

T3-055  reshaping the mark against tampering
  must_show: A design change made for protection: a border or box around the mark, an outline, the mark enlarged or compacted, a vulnerable part (a name, letters) dropped or replaced.
  must_not_show naming T3-004: design changes for their own sake (T3-004)
  discriminator against T3-004: Is the change made for the look (T3-004), or for protection (T3-055)?


T3-004 | T3-066  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  decide_when_both naming T3-066: A design argument settled by a vote adds T3-066 when the vote has concepts of its own.
  discriminator against T3-066: Is the design argued out (T3-004), or put to a vote or poll (T3-066)?

T3-066  putting decisions to a vote
  must_show: Members asked to decide together: votes, strawpolls and polls in the thread, 'we need to decide as a group', a leader letting the room choose; members casting votes.
  must_not_show naming T3-004: The design settled by argument with no vote (T3-004)
  decide_when_both naming T3-004: A design argument that ends in a vote: T3-004 primary when the arguing leads, T3-066 added when the vote has concepts of its own.
  discriminator against T3-004: Is the design argued out (T3-004), or put to a vote or poll (T3-066)?


T3-004 | T3-070  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  discriminator against T3-070: Is the design still argued (T3-004), or its directions handed out (T3-070)?

T3-070  sharing coordinates, templates and how-to
  must_show: Coordinates, templates, grid images, overlays, guides, colour plans, border plans, timings or how-to posted or updated for placers to follow by hand.
  is_not naming T3-004: Arguing over which design to build (T3-004).
  discriminator against T3-004: Is the design still argued (T3-004), or its directions handed out (T3-070)?


T3-004 | T3-077  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  discriminator against T3-077: Is a still design settled (T3-004), or a change over time planned (T3-077)?

T3-077  animating the mark in timelapse
  must_show: A plan to change the mark over time so that it animates in the timelapse: flashing colours, a walking figure, a scripted animation.
  discriminator against T3-004: Is a still design settled (T3-004), or a change over time planned (T3-077)?


T3-004 | T3-091  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  must_not_show naming T3-091: holding everyone to a chosen template (T3-091)
  is_not naming T3-091: Holding placers to the agreed design against those who stray (T3-091).
  discriminator against T3-091: Is the design being settled (T3-004), or the settled design enforced against strays (T3-091)?

T3-091  keeping everyone on one template
  must_show: One plan declared official or current and members told to follow it: 'stick to the original', 'too many people do not follow the plan', an official design thread.
  must_not_show naming T3-004: choosing which design (T3-004).
  decide_when_both naming T3-004: Choosing the design is T3-004
  discriminator against T3-004: Is the design being chosen (T3-004), or the chosen design enforced (T3-091)?


T3-004 | T3-169  (scheme_v2.jsonl; stale)

T3-004  settling the mark's design
  must_show: Argument or work on the mark's look: which picture or version, colours, letters, fonts, size, outlines, details; corrections to make the placed work match the design.
  discriminator against T3-169: Is the mark's design settled (T3-004), or its signature added (T3-169)?

T3-169  signing the sub's name
  must_show: The sub's name, or a short form of it, written on the canvas; the choice whether to write it; keeping it there.
  discriminator against T3-004: Is the mark's design settled (T3-004), or its signature added (T3-169)?


T3-006 | T3-076  (scheme_v2.jsonl; stale)

T3-006  calling to deface rivals' work
  must_show: Calls, plans or reports of attacks on another room's work meant to destroy or erase it: 'attack the Danish flag', 'wipe out Arizona', 'we must destroy the blue corner', strikes timed against a rival.
  discriminator against T3-076: Is an attack called for (T3-006), or reined in (T3-076)?

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  decide_when_both naming T3-006: An attack called for and then reined in, each in concepts of its own: both are placed, T3-006 primary when the attacking leads, T3-076 when the reining in does.
  discriminator against T3-006: Is an attack called for (T3-006), or reined in (T3-076)?


T3-007 | T3-076  (scheme_v2.jsonl; stale)

T3-007  urging repair over retaliation
  must_show: A call to answer damage by repairing instead of retaliating against the attacker.
  must_not_show naming T3-076: stopping an attack the room itself started (T3-076).
  is_not naming T3-076: Telling members to stop an attack the room began unprovoked (T3-076).
  discriminator against T3-076: Is an attack the room started stopped (T3-076), or retaliation for damage it suffered declined (T3-007)?

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  discriminator against T3-007: Is an attack the room started stopped (T3-076), or retaliation for damage it suffered declined (T3-007)?


T3-024 | T3-076  (scheme_v2.jsonl; stale)

T3-024  refusing to cover others' work
  must_show: Restraint toward others' work kept by the room's own choice: going around a neighbour's design, refusing to overwrite it, sizing or placing the work to spare it, respect for others' effort stated.
  must_not_show naming T3-076: reining in the room's members who are already attacking (T3-076)
  discriminator against T3-076: Is an attack under way stopped (T3-076), or others' work spared before any attack (T3-024)?

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  must_not_show naming T3-024: Restraint before any attack (T3-024)
  discriminator against T3-024: Is an attack under way stopped (T3-076), or others' work spared before any attack (T3-024)?


T3-040 | T3-076  (scheme_v2.jsonl; stale)

T3-040  apologizing to neighbours for damage
  must_show: An apology to another room for damage to its work by the room or people from it: 'sorry about that', apologies made in the other room's thread, offers to help redraw or rebuild.
  discriminator against T3-076: Is the damage apologised for (T3-040), or the attackers stopped (T3-076)?

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  discriminator against T3-040: Is the damage apologised for (T3-040), or the attackers stopped (T3-076)?


T3-042 | T3-076  (scheme_v2.jsonl; stale)

T3-042  choosing upkeep over expansion
  must_show: Upkeep chosen over growth: calls to maintain, clean or defend before expanding; refusals of new projects or attacks because the room cannot hold more; designs scaled to what can be defended.
  must_not_show naming T3-076: reining in the room's own attacks (T3-076).
  discriminator against T3-076: Is the room's own attack on others stopped (T3-076), or upkeep put before expansion (T3-042)?

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  discriminator against T3-042: Is the room's own attack on others stopped (T3-076), or upkeep put before expansion (T3-042)?


T3-046 | T3-076  (scheme_v2.jsonl; stale)

T3-046  arguing whether covering is fair
  must_show: Argument over covering others' work as such: 'it's an open canvas', 'that's the whole point', 'they put in passion, respect it', whether a neighbour may use the room's background.
  decide_when_both naming T3-076: Stopping the room's own attack is T3-076
  discriminator against T3-076: Is the room's attack stopped (T3-076), or the fairness of covering argued (T3-046)?

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  discriminator against T3-046: Is the attack stopped (T3-076), or the fairness of covering argued (T3-046)?


T3-076 | T3-102  (scheme_v2.jsonl; stale)

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  must_not_show naming T3-102: members acting against such a call (T3-102).
  discriminator against T3-102: Is the room's call to hold back made (T3-076), or defied (T3-102)?

T3-102  defying the call for restraint
  must_show: A member refusing the room's restraint: attacking after being told no, calling to break the room's treaty, refusing to stop drawing over a neighbour.
  must_not_show naming T3-076: The room's call to hold back itself (T3-076)
  discriminator against T3-076: Is the call to hold back made (T3-076), or defied (T3-102)?


T3-076 | T3-121  (scheme_v2.jsonl; stale)

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  must_not_show naming T3-121: excluding members as a sanction (T3-121)
  discriminator against T3-121: Is the room's attack reined in by words (T3-076), or a member excluded (T3-121)?

T3-121  excluding the room's own vandals
  must_show: Exclusion used as a sanction against the room's own members: bans from the Discord or the sub, kicking, shunning a 'traitor', members reported so moderators throw them out, such a ban challenged or reversed.
  discriminator against T3-076: Is the room's attack reined in by words (T3-076), or a member excluded (T3-121)?


T3-076 | T3-139  (scheme_v2.jsonl; stale)

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  must_not_show naming T3-139: pleading with another room's attackers (T3-139)
  is_not naming T3-139: A member asking another room's raiders to stop (T3-139).
  discriminator against T3-139: Are the room's own attackers stopped (T3-076), or another room's attackers asked to stop (T3-139)?

T3-139  pleading with attackers to stop
  must_show: Requests addressed to an attacking room or group to stop, spare the work, or let it live.
  discriminator against T3-076: Are the room's own attackers stopped (T3-076), or another room's attackers asked to stop (T3-139)?


T3-076 | T3-188  (scheme_v2.jsonl; stale)

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  discriminator against T3-188: Does the room rein in its own attackers (T3-076), or say the attackers are not its own (T3-188)?

T3-188  disowning placers outside the plan
  must_show: A room, or its organisers, setting its plan apart from placers it does not control: 'we are not for that person', 'there are rogues outside our Discord', 'the hivemind works in mysterious ways', offers to repair what the rogues did.
  discriminator against T3-076: Does the room rein in its own attackers (T3-076), or say the placers are not its own (T3-188)?


T3-076 | T3-195  (scheme_v2.jsonl; stale)

T3-076  reining in the room's attackers
  must_show: The room's own members told to stop attacking or vandalising others' work, or an attack called off after an objection; rules against new wars.
  discriminator against T3-195: Does the room stop its own attackers (T3-076), or hold another room to an agreement (T3-195)?

T3-195  holding rooms to their agreements
  must_show: An existing agreement invoked: 'we made an agreement with hearts', 'it was the original deal', 'we agreed you can have the flower, but ...', a broken deal named.
  discriminator against T3-076: Is another room held to an agreement (T3-195), or does the room stop its own attackers (T3-076)?



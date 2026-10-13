T3-005 | T3-011  (scheme_v2.jsonl; stale)

T3-005  defending the work against attackers
  must_show: An attack on the room's work and the room's answer: alarms, calls to defend or fight back, holding the line, reports of an attack repelled.
  discriminator against T3-011: Is the room's own work defended (T3-005), or another room's work helped or defended by the room's members, a pledge to protect it included (T3-011)?

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  discriminator against T3-005: Is the room's own work defended (T3-005), or another room's work helped or defended by the room's members, a pledge to protect it included (T3-011)?


T3-011 | T3-056  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  discriminator against T3-056: Is help sent to another's own work (T3-011), or one mark made together (T3-056)?

T3-056  making joint marks with others
  must_show: A mark designed or built jointly by two or more rooms: shared borders made into a design, flags combined, each finishing part of the other's work, a joint emblem.
  must_not_show naming T3-011: Help sent to another room's own work (T3-011)
  is_not naming T3-011: Sending pixels to a neighbour's defence (T3-011).
  discriminator against T3-011: Is help sent to another's own work (T3-011), or one mark made together (T3-056)?


T3-011 | T3-062  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  discriminator against T3-062: Is help asked for (T3-062), or sent to another room's work (T3-011)?

T3-062  recruiting kindred subs to help
  must_show: The room's own call for hands, made by its members and carried into other subs or communities, or proposed: 'ask r/X for help', threads opened in other subs, recruiting from related communities.
  is_not naming T3-011: Sending the room's members to help another room's work (T3-011).
  discriminator against T3-011: Is help asked for (T3-062), or sent to another room's work (T3-011)?


T3-011 | T3-078  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  discriminator against T3-078: Is help sent to any room's work (T3-011), or to a kin nation's flag as kin (T3-078)?

T3-078  helping kin nations' flags
  must_show: Help for another nation's or region's flag felt as kin: helping Baltic brothers restore their flags, asking a kin nation's sub for help, defending a brother nation's flag.
  must_not_show naming T3-011: Help to any other room's work (T3-011)
  is_not naming T3-011: A sports sub helping a neighbouring logo (T3-011).
  discriminator against T3-011: Is help sent to any room's work (T3-011), or to a kin nation's flag as kin (T3-078)?


T3-011 | T3-084  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  must_not_show naming T3-084: asking for help (T3-084)
  discriminator against T3-084: Is help asked for (T3-084), or sent (T3-011)?

T3-084  asking other rooms for help
  must_show: A request for help with the work between canvas rooms, in the record of either room: the room asking another room, or another room's request or call for hands as it arrives in the room's threads, addressed to the room as a group or to its members: 'we could use your help', 'help us please', calls for reinforcements addressed to another room.
  discriminator against T3-011: Is help asked for (T3-084), or sent (T3-011)?


T3-011 | T3-099  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  discriminator against T3-099: Is the bigger room sending help (T3-011), or the small room relying on it (T3-099)?

T3-099  relying on a bigger neighbour
  must_show: The room counting on, seeking or being promised a larger room's protection: listed among a big flag's protected works, allied with a bigger room for a secure spot.
  decide_when_both naming T3-011: Protection given by the bigger room, told from its side, is not here: it sits with the help it is (T3-011) or the alliance (T3-150).
  discriminator against T3-011: Is the bigger room sending help (T3-011), or the small room relying on it (T3-099)?


T3-011 | T3-115  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  discriminator against T3-115: Is another room's request refused (T3-115), or its work helped (T3-011)?

T3-115  turning away another room's request
  must_show: A request from another room or its members refused or sent back: 'no', 'we can not offer our assistance', 'post it on your own sub', a refusal on grounds of rivalry.
  must_not_show naming T3-011: Requests granted (T3-012, T3-011)
  discriminator against T3-011: Is another room's request refused (T3-115), or its work helped (T3-011)?


T3-011 | T3-119  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  discriminator against T3-119: Is help sent with no prior attack (T3-011), or by those who attacked (T3-119)?

T3-119  turning attackers into helpers
  must_show: Former attackers helping the work they damaged: admitting the damage and helping rebuild, repairing a work they overwrote, a takeover followed by help to rebuild elsewhere.
  must_not_show naming T3-011: help with no prior attack (T3-011).
  discriminator against T3-011: Is help sent with no prior attack (T3-011), or by those who attacked (T3-119)?


T3-011 | T3-137  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  must_not_show naming T3-137: joining another group's build as one's own (T3-137).
  discriminator against T3-137: Does the member help another's work while keeping the room's own (T3-011), or join another group's build as theirs (T3-137)?

T3-137  joining an outside group's build
  must_show: A member, or the room, joining another group's work as a participant: 'I joined the void', 'all my pixels go to r/X's territory', following an outside sub's plan.
  must_not_show naming T3-011: Help sent while the room keeps its own work (T3-011)
  decide_when_both naming T3-011: Joining and helping in one theme: T3-137 when the member's effort moves to the other build, T3-011 when it stays the room's.
  is_not naming T3-011: Sending a few pixels to help a neighbour while building one's own (T3-011).
  discriminator against T3-011: Does the member help another's work while keeping the room's own (T3-011), or join the other build as theirs (T3-137)?


T3-011 | T3-150  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  must_not_show naming T3-150: an alliance for joint defence (T3-150)
  discriminator against T3-150: Are the rooms allied for joint defence (T3-150), or is help sent to another's work (T3-011)?

T3-150  forming alliances between rooms
  must_show: An alliance between rooms for defence or a fight: proposals and invitations, named alliances, rooms joining a front, promises to defend each other.
  must_not_show naming T3-011: help sent with nothing asked (T3-011)
  discriminator against T3-011: Are the rooms allied for joint defence (T3-150), or is help sent to another's work (T3-011)?


T3-011 | T3-151  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  must_not_show naming T3-151: Help traded for help (T3-151)
  decide_when_both naming T3-151: Help given in return is T3-151
  is_not naming T3-151: Help given in return for help received (T3-151).
  discriminator against T3-151: Is help given in return for help (T3-151), or with nothing asked (T3-011)?

T3-151  bartering help with neighbours
  must_show: Help offered or asked in return for help: 'we'll help you move if you maintain ours', 'repay the favour', maintenance traded for room.
  must_not_show naming T3-011: Help sent with nothing asked (T3-011)
  decide_when_both naming T3-011: Help given in return is T3-151, help with nothing asked T3-011.
  is_not naming T3-011: Sending pixels to a neighbour's defence unasked (T3-011).
  discriminator against T3-011: Is help given in return (T3-151), or with nothing asked (T3-011)?


T3-011 | T3-195  (scheme_v2.jsonl; stale)

T3-011  helping another room's work
  must_show: Help sent from one room to another room's work, in the record of either room: the room's members helping another room's work, or called to it by the room's own members; or another room's members arriving in the room's threads to help its work: 'come help the farm at r/X', 'I'm helping r/Y', 'from r/Z, glad to help', pixels sent to a neighbour's defence.
  discriminator against T3-195: Is an agreement already made invoked, spread or said to be broken (T3-195), or another room's work helped or defended, the pledge named only as the reason for the help (T3-011)?

T3-195  holding rooms to their agreements
  must_show: An existing agreement invoked: 'we made an agreement with hearts', 'it was the original deal', 'we agreed you can have the flower, but ...', a broken deal named.
  discriminator against T3-011: Is an agreement already made invoked, spread or said to be broken (T3-195), or another room's work helped or defended, the pledge named only as the reason for the help (T3-011)?



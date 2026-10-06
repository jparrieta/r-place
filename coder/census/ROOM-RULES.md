# What counts as a room

*Kind of page: reference. Target length: under 1,100 words before the lists. Made on 4 October 2026 from this folder's files and [the census page](../../Manual/census.md). The rules the atlas yard applied, so that venues_yard (the venues no atlas artwork credits) can apply the same ones, and every subreddit they kept or discarded; the lists are also in `ROOM-LIST.tsv`.*

## Terms and windows

A **venue** is any subreddit. A **room** is a venue read as one case. The **population** is every venue that passes the rules below (`handable = 1`). The yard codes it; the aggregator's frame is the part coded at a copy date.

| window | UTC | epoch seconds |
|---|---|---|
| the week before | 2017-03-24 16:00 to 2017-03-31 16:00 | 1490371200 to 1490976000 |
| the canvas open, 73 hours | 2017-03-31 16:00 to 2017-04-03 17:00 | 1490976000 to 1491238800 |
| the coders' window, 97 hours | 2017-03-31 16:00 to 2017-04-04 17:00 | 1490976000 to 1491325200 |
| the record (raw24), 24 days | 2017-03-24 16:00 to 2017-04-17 17:00 | 1490371200 to 1492448400 |

The record is every post and comment in the venue in the arctic-shift archive (`data/raw24/README.md`). Counting people drops the authors `[deleted]`, `[removed]` and `AutoModerator`.

## The rules, in order

A venue that fails a rule leaves under the label in bold; its row stays, with the reason in `validation_note`.

1. **Where candidates come from.** In the atlas yard: the subreddits the 2017 atlas links (case-folded, `r/` removed, each link resolved by hand, below), the communities whose names are written on the final canvas, and those an atlas description names as makers. A canvas name or a description credit joins only if the community took part in its own threads, with the evidence in `validations.jsonl`. **In venues_yard this rule is replaced by its own list**, for example every subreddit where a placer wrote while the canvas was open; rules 2 to 8 apply unchanged.
2. **It is a community with a public record.** Not a row: a user page, a feed (r/all), a Discord or other off-Reddit group, a private subreddit (the archive holds none), a name with no record at all, a subreddit created after the event. A redirect, a single post pointing to another subreddit, is read `none` and screened out (r/TFLS).
3. **It posted inside the 97 hours.** A venue with no item in the coders' window leaves as **silent_in_window**.
4. **It posted while the canvas was open.** A venue whose items fall only in the 24 hours after the freeze leaves as **post_freeze_only**, whatever they say: talk about a frozen canvas is not organising on a live one (four of the seven held canvas talk).
5. **It wrote about the event while the canvas was open** (J, 4 October 2026: "we need only communities in which there was some writing"). A venue that posted in the 73 hours but began to write about the event only after the freeze leaves as **event_talk_after_freeze**. r/lehigh posted twelve items while the canvas was open, none about it; its first coded turn is at hour 78.98. Once a room is coded, the test is its first coded turn at or before hour 73.
6. **Its text takes part in the event.** A lexical screen counts marker words over the 97 hours (`hit_strong`, `hit_canvas`, `hit_pixel`, `hit_coords`, `hit_craft`) and only flags. Its markers are English, and a room can name its artwork and never the event. A reading decides, and outranks the screen:
   - a coder's verdict of `none` screens the room out (**screened_out**);
   - a recorded reading of an uncoded venue, with its evidence in `validations.jsonl`, screens it out or keeps it;
   - a coder's `full` or `trace` keeps the room, unless a later reading finds no writing about the event (r/upvote: a link post whose replies only ask for upvotes, read so by two aggregator runs; **screened_out**, J 4 October 2026).
   A room that names its artwork and not the event stays: r/PokemonSage names the Foliat sprite, and r/OrderOfTheKoi organised the koi without once naming r/place.
7. **It is not the field.** r/place, where the rooms met, is not a case. It is coded and modelled apart and enters the aggregator at stage C4 (**screened_out**, class `the_field`).
8. **What is left is the population.** The yard builds and codes every venue in it. A room its coder closes `none` leaves under rule 6. The frame is every coded room of the population at the copy date (`package/FRAME.md`).

## The labels in the atlas census, 4 October 2026

| disposition | in the population | rows | rule |
|---|---|---:|---|
| `case` | yes | 298 | coded, and the event is in its text |
| `candidate` | yes | 408 | passed before it was coded; all coded since but r/The_Donald |
| `screened_out` | no | 34 | 6 or 7: 29 coded `none` (r/TFLS among them), 3 read by a check, r/upvote, r/place |
| `silent_in_window` | no | 29 | 3 |
| `post_freeze_only` | no | 7 | 4 |
| `event_talk_after_freeze` | no | 1 | 5 |

777 rows, 706 in the population, 705 coded. The yard holds 741 rooms: the 706 and 35 outside: r/place, coded apart; 32 built before the screen closed them; r/Lehigh and r/upvote, which left after coding.

## For venues_yard

- Apply rules 2 to 8 as written: the same windows, archive, author exclusions, labels and records. Rule 1 is yours to state.
- Without an artwork to anchor it, rule 6 carries the whole weight: a large general venue where placers also wrote passes rules 3 to 5 at once, and is a room only if its own threads take part in the event.
- Leave out every venue in the lists below; each has been judged once, and a second yard does not judge it again. Match on `subreddit_id`, or on the name without regard to case: 276 of the census's 777 spellings differ in case from Reddit's own name (`the_donald` for r/The_Donald, `Katamari` for r/katamari).
- The atlas-only parts do not carry over: the link resolutions, the canvas names, the description credits and the `atlas_*` columns.

## Where the names come from

Each name is the `subreddit` field of the venue's own record, as Reddit spells it: 705 from `aggregator/input/raw`, 36 from the yard's archives, one from `Layer A/raw24_additions`. The 35 with no local record were looked up in the arctic-shift archive on 4 October 2026 (29 by subreddit, 6 by their posts). The id is Reddit's (`t5_...`).

## Atlas links resolved to a room

| atlas link | the room it means | why |
|---|---|---|
| `hyperlightdrifer` | r/hyperlightdrifter | a typo |
| `r2007Scape` | r/2007scape | an r/ folded into the name |
| `avocodoarmy` | r/AvoArmy | a misspelling |
| `ccKufiPrFaShleWoli0` | r/ccKufiPrFaShleWoliGtM | a truncated name |
| `newzealand+australia` | r/newzealand and r/australia | a multireddit |

## The rooms: the population of 706

| Reddit name | subreddit id | census spelling, where it differs | coded |
|---|---|---|---|
| r/2007scape | t5_2wbww |  | yes |
| r/49ers | t5_2rebv |  | yes |
| r/4chan | t5_2qh4w |  | yes |
| r/AceAttorney | t5_2so0n | aceattorney | yes |
| r/acecombat | t5_2svt4 |  | yes |
| r/AceOfAngels8 | t5_2w3dk |  | yes |
| r/AcePlace | t5_3jsim |  | yes |
| r/Achievement_Hunter | t5_2v6vs | achievement_hunter | yes |
| r/adventuretime | t5_2s54g |  | yes |
| r/Aeon | t5_2vk9y | aeon | yes |
| r/AEskwadraat | t5_3heqc | aeskwadraat | yes |
| r/AFIP | t5_3jtag | afip | yes |
| r/aggies | t5_2qyds |  | yes |
| r/ainbowroad | t5_3jsb1 |  | yes |
| r/albania | t5_2sc6w |  | yes |
| r/alberta | t5_2qxon |  | yes |
| r/Amd | t5_2rw0n | AMD | yes |
| r/AmericanFlaginPlace | t5_3jt7h |  | yes |
| r/AnaheimDucks | t5_2rqhz | anaheimducks | yes |
| r/Anarchism | t5_2qh5j | anarchism | yes |
| r/Anarcho_Capitalism | t5_2qorf | anarcho_capitalism | yes |
| r/anarchocapitalism | t5_2r3rn |  | yes |
| r/AndroidGaming | t5_2s2ul | androidgaming | yes |
| r/AnimalCrossing | t5_2ro2c | animalcrossing | yes |
| r/anime | t5_2qh22 |  | yes |
| r/anime_irl | t5_386zh |  | yes |
| r/aoe2 | t5_2sg7u |  | yes |
| r/ApocalypseRising | t5_2umo5 | apocalypserising | yes |
| r/AprilKnights | t5_3deum |  | yes |
| r/araragi | t5_2tdi5 |  | yes |
| r/archlinux | t5_2qrzu |  | yes |
| r/argentina | t5_2qlht |  | yes |
| r/armenia | t5_2qo29 |  | yes |
| r/armok | t5_3jt6k |  | yes |
| r/aromantic | t5_2ug7r |  | yes |
| r/Asexual | t5_2rhee | asexual | yes |
| r/asexuality | t5_2qv0q |  | yes |
| r/asktransgender | t5_2r4b9 |  | yes |
| r/auburn | t5_2s54n |  | yes |
| r/australia | t5_2qh8e |  | yes |
| r/Austria | t5_2qo9i | austria | yes |
| r/austriahungary | t5_31zn5 |  | yes |
| r/AvoArmy | t5_3jsiv |  | yes |
| r/AyyMD | t5_38z4q |  | yes |
| r/azerbaijan | t5_2s8kv |  | yes |
| r/azores | t5_2solj |  | yes |
| r/BABYMETAL | t5_2xpsy | babymetal | yes |
| r/Bahrain | t5_2rv05 | bahrain | yes |
| r/bakchodi | t5_2tif7 |  | yes |
| r/bangladesh | t5_2qixf |  | yes |
| r/bangtan | t5_2zqih |  | yes |
| r/bannedfromanime_irl | t5_3clza |  | yes |
| r/bardmains | t5_37dgr |  | yes |
| r/batman | t5_2qqt8 |  | yes |
| r/battlecats | t5_2tsiy |  | yes |
| r/baylor | t5_2sg0d |  | yes |
| r/bdsm | t5_2qjdo |  | yes |
| r/bees | t5_2qpf4 |  | yes |
| r/belgium | t5_2qhe6 |  | yes |
| r/berkeley | t5_2qh9w |  | yes |
| r/Berserk | t5_2rru6 | berserk | yes |
| r/bigbang | t5_2r0zo |  | yes |
| r/bih | t5_2s7a1 |  | yes |
| r/bindingofisaac | t5_2sxpk |  | yes |
| r/bisexual | t5_2qwnx |  | yes |
| r/Bitcoin | t5_2s3qj | bitcoin | yes |
| r/blackmirror | t5_2v08h |  | yes |
| r/bobross | t5_2sao8 |  | yes |
| r/Borderlands | t5_2r8cd | borderlands | yes |
| r/borussiadortmund | t5_2svdo |  | yes |
| r/BostonBruins | t5_2rmt9 | bostonbruins | yes |
| r/bostonceltics | t5_2qmkf |  | yes |
| r/brasil | t5_2qh9i |  | yes |
| r/Bravenewbies | t5_2w7lx |  | yes |
| r/Braveryjerk | t5_2tl1h |  | yes |
| r/Bretagne | t5_2s9q8 | bretagne | yes |
| r/btc | t5_2si5v |  | yes |
| r/Buffalo | t5_2qi6i | buffalo | yes |
| r/buffalobills | t5_2ra29 |  | yes |
| r/BuffaloWizards | t5_31e75 | buffalowizards | yes |
| r/bulgaria | t5_2qhx7 |  | yes |
| r/CalgaryFlames | t5_2roln | calgaryflames | yes |
| r/calvinandhobbes | t5_2qtxs |  | yes |
| r/canada | t5_2qh68 |  | yes |
| r/canucks | t5_2qrs7 |  | yes |
| r/Cardinals | t5_2r7tu | cardinals | yes |
| r/CarletonU | t5_2s47v | carletonu | yes |
| r/catalonia | t5_2sau7 |  | yes |
| r/catalunya | t5_2s049 |  | yes |
| r/Catholicism | t5_2qi4f | catholicism | yes |
| r/cavestory | t5_2smq4 |  | yes |
| r/CelticFC | t5_2snki | CelticFc | yes |
| r/CFB | t5_2qm9d | cfb | yes |
| r/CGPGrey | t5_2u93l | cgpgrey | yes |
| r/chelseafc | t5_2rsl6 |  | yes |
| r/chess | t5_2qhr7 |  | yes |
| r/CHIBears | t5_2s0u3 | chibears | yes |
| r/chicago | t5_2qh2t |  | yes |
| r/CHICubs | t5_37k90 | chicubs | yes |
| r/chile | t5_2rer8 |  | yes |
| r/chronotrigger | t5_2sevh | ChronoTrigger | yes |
| r/churchofhelix | t5_30fqb |  | yes |
| r/cirkeltrek | t5_318w4 |  | yes |
| r/CKCrusaders | t5_3jsnb |  | yes |
| r/Clannad | t5_2soqc |  | yes |
| r/ClashRoyale | t5_3bog8 | clashroyale | yes |
| r/CLG | t5_2v76v | clg | yes |
| r/Cloud9 | t5_2udw5 | cloud9 | yes |
| r/ClubPenguin | t5_2serh | clubpenguin | yes |
| r/cmu | t5_2r87b |  | yes |
| r/Coldplay | t5_2qmkl | coldplay | yes |
| r/Colombia | t5_2qrpc | colombia | yes |
| r/Colorado | t5_2qhkb | colorado | yes |
| r/columbia | t5_2qq0v |  | yes |
| r/COMPLETEANARCHY | t5_397x6 | completeanarchy | yes |
| r/compsoc | t5_2qwv9 |  | yes |
| r/Cornwall | t5_2r2lk |  | yes |
| r/Corridor | t5_3f9jo | corridor | yes |
| r/COSI | t5_2qsms |  | yes |
| r/costa_rica | t5_2s4n6 |  | yes |
| r/counting | t5_2u9jq |  | yes |
| r/CowChop | t5_3d9a4 | cowchop | yes |
| r/criticalrole | t5_385bw |  | yes |
| r/croatia | t5_2qyps |  | yes |
| r/CrusaderKings | t5_2tgic | crusaderkings | yes |
| r/CryptoFR | t5_3jta0 |  | yes |
| r/crystalclear | t5_37ce5 |  | yes |
| r/CSUFoCo | t5_2spbq |  | yes |
| r/Cubers | t5_2r6a3 | cubers | yes |
| r/cuboulder | t5_2r8y0 |  | yes |
| r/czech | t5_2qiht |  | yes |
| r/DaftPunk | t5_2qtn5 | daftpunk | yes |
| r/DallasStars | t5_2ro4p | dallasstars | yes |
| r/danganronpa | t5_2wcd0 |  | yes |
| r/dankmemes | t5_2zmfe |  | yes |
| r/darksouls | t5_2sazo |  | yes |
| r/DatBoi | t5_3edq6 |  | yes |
| r/DavidBowie | t5_2smf8 | davidbowie | yes |
| r/day9 | t5_2rvng |  | yes |
| r/dbz | t5_2sdu8 |  | yes |
| r/DCFU | t5_3ct9r |  | yes |
| r/de | t5_22i0 |  | yes |
| r/Denmark | t5_2qjto | denmark | yes |
| r/DenverBroncos | t5_2s51j | denverbroncos | yes |
| r/Destiny | t5_2qnvz | destiny | yes |
| r/DestinyTheGame | t5_2vq0w |  | yes |
| r/detroitlions | t5_2rynx |  | yes |
| r/DetroitRedWings | t5_2resw | detroitredwings | yes |
| r/DevonUK | t5_2srfs |  | yes |
| r/Diablo | t5_2qore | diablo | yes |
| r/DiamondClub | t5_2sk9w |  | yes |
| r/DMT | t5_2qhvk | dmt | yes |
| r/Dofus | t5_2sl1e | dofus | yes |
| r/Dominican | t5_2qjy9 |  | yes |
| r/donaldglover | t5_2scgk |  | yes |
| r/Dorset | t5_2sw81 |  | yes |
| r/DotA2 | t5_2s580 | dota2 | yes |
| r/dragonquest | t5_2sbty |  | yes |
| r/drawhelix | t5_3jsh2 |  | yes |
| r/Drugs | t5_2qh7l | drugs | yes |
| r/drumcorps | t5_2rwjm |  | yes |
| r/duckgame | t5_380w4 |  | yes |
| r/ducks | t5_2qlr0 |  | yes |
| r/dustforce | t5_2tcmb | Dustforce | yes |
| r/dwarffortress | t5_2qyn1 |  | yes |
| r/eagles | t5_2qi5w |  | yes |
| r/earthbound | t5_2rkbz |  | yes |
| r/edBoxes | t5_3jt70 | edboxes | yes |
| r/Eder | t5_33ew8 | eder | yes |
| r/EdmontonOilers | t5_2rptq | edmontonoilers | yes |
| r/Eesti | t5_2rffn | eesti | yes |
| r/Egypt | t5_2ql2m | egypt | yes |
| r/ElderScrolls | t5_2s2ja |  | yes |
| r/EliteDangerous | t5_2vi60 | elitedangerous | yes |
| r/ElSalvador | t5_2qs3c |  | yes |
| r/EmpireDidNothingWrong | t5_397yx | empiredidnothingwrong | yes |
| r/england | t5_2qh8h |  | yes |
| r/EnterTheGungeon | t5_37d0t | enterthegungeon | yes |
| r/epublica | t5_3jteb |  | yes |
| r/EraseThePlace | t5_3jsao |  | yes |
| r/Esperanto | t5_2qo5v | esperanto | yes |
| r/ethereum | t5_2zf9m |  | yes |
| r/ethoslab | t5_2t5qc |  | yes |
| r/europe | t5_2qh4j |  | yes |
| r/Eve | t5_2qil9 | eve | yes |
| r/evedreddit | t5_2rhwu |  | yes |
| r/EVEX | t5_35smv | evex | yes |
| r/factorio | t5_2wabp |  | yes |
| r/faeria | t5_2v2l8 |  | yes |
| r/falcons | t5_2ql17 |  | yes |
| r/farmcarrots | t5_3jspd |  | yes |
| r/FaroeIslands | t5_2sx9p |  | yes |
| r/FederationPlace | t5_3jt7c |  | yes |
| r/feedthebeast | t5_2v620 |  | yes |
| r/Fez | t5_2socv |  | yes |
| r/FinalFantasy | t5_2qhdi |  | yes |
| r/Finland | t5_2qztz | finland | yes |
| r/fireemblem | t5_2t0cn |  | yes |
| r/fivenightsatfreddys | t5_331ct |  | yes |
| r/Flaggyflag | t5_3bdbq | FlaggyFlag | yes |
| r/FlashTV | t5_2y6bs | flashtv | yes |
| r/FlipnoteStudio3D | t5_2wmk4 |  | yes |
| r/FloridaGators | t5_2qv2r | floridagators | yes |
| r/FloydVsVoid | t5_3jt4l |  | yes |
| r/Flyers | t5_2ribt | flyers | yes |
| r/formula1 | t5_2qimj |  | yes |
| r/forsen | t5_33td5 |  | yes |
| r/foxes | t5_2qont |  | yes |
| r/FoxStevenson | t5_2xq73 | foxstevenson | yes |
| r/france | t5_2qhjz |  | yes |
| r/FrankOcean | t5_2tyek | frankocean | yes |
| r/FRC | t5_2rdka | frc | yes |
| r/freedomplanet | t5_2wc9f |  | yes |
| r/ftlgame | t5_2tnu1 |  | yes |
| r/FULLCOMMUNISM | t5_2w5yw | fullcommunism | yes |
| r/funhaus | t5_35b7i |  | yes |
| r/furry | t5_2qi2h |  | yes |
| r/furry_irl | t5_3b66u |  | yes |
| r/futanari | t5_2rai5 |  | yes |
| r/futurama | t5_2qhqw |  | yes |
| r/fxKorea | t5_2to6g |  | yes |
| r/GabrielDropout | t5_3if67 |  | yes |
| r/GameAttack | t5_3gbo3 | gameattack | yes |
| r/Gameboy | t5_2s0qt | gameboy | yes |
| r/gameofthrones | t5_2rjz2 |  | yes |
| r/gamindustri | t5_2w8vg |  | yes |
| r/gatech | t5_2r8t2 |  | yes |
| r/genderfluid | t5_2u0nr |  | yes |
| r/geometrydash | t5_304br |  | yes |
| r/germany | t5_2qi4z |  | yes |
| r/ghibli | t5_2riwr |  | yes |
| r/giantbomb | t5_2rlj3 |  | yes |
| r/GiIvaSunner | t5_3d0pd | giivasunner | yes |
| r/glasgow | t5_2rgo2 |  | yes |
| r/GlobalOffensive | t5_2sqho | globaloffensive | yes |
| r/goodboye | t5_3jtle | Goodboye | yes |
| r/gorillaz | t5_2rnhi |  | yes |
| r/GranColombia | t5_3jtk4 |  | yes |
| r/gratefuldead | t5_2qpnj |  | yes |
| r/gravityfalls | t5_2udb8 |  | yes |
| r/greece | t5_2qh8i |  | yes |
| r/GreenBayPackers | t5_2qqd2 | greenbaypackers | yes |
| r/GreenCorner | t5_3jsc0 |  | yes |
| r/GreenEmpire | t5_3js9i |  | yes |
| r/greenland | t5_2sp28 |  | yes |
| r/GreenLattice | t5_3jsd8 | greenlattice | yes |
| r/GreyBlob | t5_3jssw | greyblob | yes |
| r/GrowTheTree | t5_3jt9g |  | yes |
| r/GuardiansOfDatBoi | t5_3jsrs |  | yes |
| r/guatemala | t5_2samk |  | yes |
| r/Guildwars2 | t5_2r9po | GuildWars2 | yes |
| r/h3h3productions | t5_3345f |  | yes |
| r/Habs | t5_2r10m | habs | yes |
| r/halo | t5_2qixk |  | yes |
| r/harrypotter | t5_2qiqi |  | yes |
| r/haskell | t5_2qh36 |  | yes |
| r/hatsune | t5_2yud6 |  | yes |
| r/hawks | t5_2rhes |  | yes |
| r/hearthstone | t5_2w31t |  | yes |
| r/HelloInternet | t5_2z1tz | hellointernet | yes |
| r/hentai | t5_2qj7g |  | yes |
| r/heroesofthestorm | t5_2ym13 |  | yes |
| r/heyyea | t5_3juab |  | yes |
| r/homelab | t5_2ubz7 |  | yes |
| r/HomestarRunner | t5_2rj30 |  | yes |
| r/homestuck | t5_2rzgi |  | yes |
| r/homura | t5_2vp36 | Homura | yes |
| r/Honduras | t5_2r9ey |  | yes |
| r/HongKong | t5_2rbn0 | hongkong | yes |
| r/hoodr | t5_3jt1o |  | yes |
| r/hsv | t5_2qt6s |  | yes |
| r/httyd | t5_2teon |  | yes |
| r/hungary | t5_2qzzt |  | yes |
| r/HunterXHunter | t5_2spu5 | hunterxhunter | yes |
| r/hyperlightdrifter | t5_2yhza |  | yes |
| r/iastate | t5_2qtol |  | yes |
| r/IBO | t5_2s05l | ibo | yes |
| r/Ice_Poseidon | t5_3aelr | ice_poseidon | yes |
| r/Iceland | t5_2qigc | iceland | yes |
| r/ik_ihe | t5_39bxv |  | yes |
| r/india | t5_2qh1q |  | yes |
| r/indieheads | t5_2zj24 |  | yes |
| r/indonesia | t5_2qkte |  | yes |
| r/ireland | t5_2qhb9 |  | yes |
| r/Israel | t5_2qhvo | israel | yes |
| r/italy | t5_2qkhk |  | yes |
| r/Jamaica | t5_2rn39 |  | yes |
| r/japan | t5_2qh2u |  | yes |
| r/jerma985 | t5_2yt2x |  | yes |
| r/k_on | t5_2tpfm |  | yes |
| r/KamenRider | t5_2s8q8 | kamenrider | yes |
| r/Kanye | t5_2r78l | kanye | yes |
| r/katawashoujo | t5_2tb50 |  | yes |
| r/KCRoyals | t5_2s8ut | kcroyals | yes |
| r/KerbalSpaceProgram | t5_2smr1 | kerbalspaceprogram | yes |
| r/kilian | t5_3c44g |  | yes |
| r/kindafunny | t5_2vhlq |  | yes |
| r/KingdomHearts | t5_2s3jo | kingdomhearts | yes |
| r/Kirby | t5_2r411 | kirby | yes |
| r/Konosuba | t5_3c02n | konosuba | yes |
| r/korea | t5_2qiog |  | yes |
| r/kpop | t5_2r1ox |  | yes |
| r/KState | t5_2s66f |  | yes |
| r/kurdistan | t5_2rt31 |  | yes |
| r/Kuwait | t5_2qzc1 | kuwait | yes |
| r/lakers | t5_2qhv6 |  | yes |
| r/Landry | t5_3hug8 | landry | yes |
| r/latin | t5_2qloa |  | yes |
| r/latvia | t5_2rwqy |  | yes |
| r/leafs | t5_2r8hf |  | yes |
| r/leagueoflegends | t5_2rfxx |  | yes |
| r/lebanon | t5_2qzpg |  | yes |
| r/lego | t5_2qhm7 |  | yes |
| r/lexington | t5_2rjxn |  | yes |
| r/lifeisstrange | t5_32tf7 |  | yes |
| r/linux | t5_2qh1a |  | yes |
| r/Liquicity | t5_2uwa0 | liquicity | yes |
| r/lithuania | t5_2qj20 |  | yes |
| r/littlebusters | t5_2v13a |  | yes |
| r/LittleWitchAcademia | t5_2x9si | littlewitchacademia | yes |
| r/livecounting | t5_3304m |  | yes |
| r/LiverpoolFC | t5_2qn0o | liverpoolfc | yes |
| r/LofiHipHop | t5_31kv6 | lofihiphop | yes |
| r/loliconsunite | t5_3jsko |  | yes |
| r/loltyler1 | t5_3eanq |  | yes |
| r/lost | t5_2qhag |  | yes |
| r/LoveLive | t5_31qlw | lovelive | yes |
| r/LSU | t5_2rlgj | lsu | yes |
| r/luciomains | t5_3ejub |  | yes |
| r/Lugarix | t5_3d9dm |  | yes |
| r/Luxembourg | t5_2ryqf | luxembourg | yes |
| r/madeon | t5_2smxo | Madeon | yes |
| r/MadokaMagica | t5_2w9u6 | madokamagica | yes |
| r/magicTCG | t5_2qn5f | magictcg | yes |
| r/malaysia | t5_2qh8b |  | yes |
| r/malta | t5_2qrbz |  | yes |
| r/mamamoo | t5_30c4e |  | yes |
| r/ManningPlace | t5_3juay |  | yes |
| r/Mario | t5_2qlqx |  | yes |
| r/mariokart | t5_2s9ql |  | yes |
| r/Marvel | t5_2r40o | marvel | yes |
| r/maryland | t5_2qnnv |  | yes |
| r/masseffect | t5_2rc19 |  | yes |
| r/math | t5_2qh0n |  | yes |
| r/mcgill | t5_2rhkw |  | yes |
| r/McGillRobotics | t5_3ju3r | mcgillrobotics | yes |
| r/MechanicalKeyboards | t5_2ugo7 | mechanicalkeyboards | yes |
| r/Megaman | t5_2rq0l | megaman | yes |
| r/Metalcore | t5_2rfut | metalcore | yes |
| r/metalgearsolid | t5_2s4hr |  | yes |
| r/Metroid | t5_2rrd6 | metroid | yes |
| r/mexico | t5_2qhv7 |  | yes |
| r/miamidolphins | t5_2s20n |  | yes |
| r/MiamiHurricanes | t5_2sxfh |  | yes |
| r/mindcrack | t5_2to85 |  | yes |
| r/Minecraft | t5_2r05i | minecraft | yes |
| r/minnesotavikings | t5_2qocl |  | yes |
| r/miraculousladybug | t5_39tdz |  | yes |
| r/mit | t5_2qh3w |  | yes |
| r/mizzou | t5_2s1hj |  | yes |
| r/MLS | t5_2rbnb | mls | yes |
| r/MMA | t5_2qhj4 |  | yes |
| r/MonaLisaClan | t5_3jt1k | monalisaclan | yes |
| r/Monero | t5_31hbr | monero | yes |
| r/MonkeyIsland | t5_2rrrj |  | yes |
| r/Monstercat | t5_2se72 | monstercat | yes |
| r/MonsterHunter | t5_2rron | monsterhunter | yes |
| r/montenegro | t5_2sfri |  | yes |
| r/Moondye7 | t5_2yyqc |  | yes |
| r/Mordhau | t5_387za | mordhau | yes |
| r/Morrowind | t5_2r9nv | morrowind | yes |
| r/msu | t5_2qldh |  | yes |
| r/Muse | t5_2qz0k | muse | yes |
| r/mylittlepony | t5_2s8bl |  | yes |
| r/MysteryDungeon | t5_2srkz | mysterydungeon | yes |
| r/n64 | t5_2s34r |  | yes |
| r/Naruto | t5_2quts | naruto | yes |
| r/NASCAR | t5_2qs08 | nascar | yes |
| r/Natsume | t5_33udp | natsume | yes |
| r/NBASpurs | t5_2s53b | nbaspurs | yes |
| r/necrodancer | t5_2yq2c |  | yes |
| r/neopets | t5_2r64t |  | yes |
| r/Nerf | t5_2qz7g | nerf | yes |
| r/NEU | t5_2r47x | neu | yes |
| r/neutralmilkhotel | t5_2ro9f |  | yes |
| r/NewMexico | t5_2raxc |  | yes |
| r/newzealand | t5_2qhma |  | yes |
| r/nier | t5_2w4iz | NieR | yes |
| r/NightInTheWoods | t5_2z77i | nightinthewoods | yes |
| r/nin | t5_2qhwq |  | yes |
| r/nintendo | t5_2qhnk |  | yes |
| r/NLSSCircleJerk | t5_2xshw | nlsscirclejerk | yes |
| r/NonBinary | t5_2vcez | nonbinary | yes |
| r/norge | t5_2qh94 |  | yes |
| r/Northwestern | t5_2qptt |  | yes |
| r/Norway | t5_2qwrb | norway | yes |
| r/notredame | t5_2qxir |  | yes |
| r/NovaScotia | t5_2qtnx |  | yes |
| r/NPR | t5_2qnbd | npr | yes |
| r/NuclearThrone | t5_2yrck | nuclearthrone | yes |
| r/nVade | t5_3jtrb |  | yes |
| r/nyjets | t5_2s2av |  | yes |
| r/nyu | t5_2rbpf |  | yes |
| r/ockytop | t5_2v13w |  | yes |
| r/Ohio | t5_2qn7b | ohio | yes |
| r/Okami | t5_2sl60 |  | yes |
| r/OKState | t5_2qnwi |  | yes |
| r/OLTP | t5_319oi | oltp | yes |
| r/Oman | t5_2sayx | oman | yes |
| r/OnePiece | t5_2rfz5 |  | yes |
| r/oneplus | t5_30qnb |  | yes |
| r/OnePunchMan | t5_2vm97 | onepunchman | yes |
| r/oneshot | t5_2yg6l |  | yes |
| r/OneTrueEmilia | t5_3ekl7 |  | yes |
| r/ontario | t5_2qsf3 |  | yes |
| r/OpTicGaming | t5_2xpuo | opticgaming | yes |
| r/orderofthebluecorner | t5_3jsal |  | yes |
| r/OrderOfTheKoi | t5_3ju13 |  | yes |
| r/OSU | t5_2qj3f | osu | yes |
| r/osugame | t5_2s3lm |  | yes |
| r/Overwatch | t5_2u5kl | overwatch | yes |
| r/pakistan | t5_2qh89 |  | yes |
| r/Paladins | t5_2v7zr | paladins | yes |
| r/Palestine | t5_2qhak | palestine | yes |
| r/pansexual | t5_2spwe |  | yes |
| r/Parabola | t5_2t2tj | parabola | yes |
| r/paragon | t5_2uu0j |  | yes |
| r/Parahumans | t5_2x7ww | parahumans | yes |
| r/paranatural | t5_2w7ds |  | yes |
| r/parrots | t5_2qhyf |  | yes |
| r/PartyParrot | t5_3eyx3 | partyparrot | yes |
| r/pathofexile | t5_2sf6m |  | yes |
| r/Patriots | t5_2rx57 | patriots | yes |
| r/paydaytheheist | t5_2t0hx |  | yes |
| r/pcmasterrace | t5_2sgp1 |  | yes |
| r/pebble | t5_2txls |  | yes |
| r/penguins | t5_2r549 |  | yes |
| r/pepe | t5_2qrfy |  | yes |
| r/PERU | t5_2qp9h | Peru | yes |
| r/peterdraws | t5_2zu38 |  | yes |
| r/PGang | t5_3junr | pgang | yes |
| r/Philippines | t5_2qjov | philippines | yes |
| r/phish | t5_2ql29 |  | yes |
| r/Physical_Removal | t5_3fjrr | physical_removal | yes |
| r/PictureGame | t5_30dxu | picturegame | yes |
| r/Pigifs | t5_3ipqs |  | yes |
| r/PinkUnion | t5_3jsed |  | yes |
| r/PinkVomitMonster | t5_3jsu4 |  | yes |
| r/Pitt | t5_2rhsl | pitt | yes |
| r/placecanada | t5_3jslz |  | yes |
| r/placeDE | t5_3jt5z |  | yes |
| r/placehearts | t5_3jsj1 |  | yes |
| r/placehfarts | t5_3jszb |  | yes |
| r/PlaceNL | t5_3jt7o |  | yes |
| r/placeportalpattern | t5_3jsnj |  | yes |
| r/placesnek | t5_3jt9k |  | yes |
| r/placestart | t5_3jtgu |  | yes |
| r/placeTARDIS | t5_3jtrh | placetardis | yes |
| r/Planetside | t5_2s48x | planetside | yes |
| r/pokemon | t5_2qmeb |  | yes |
| r/PokemonSage | t5_31ph5 |  | yes |
| r/poland | t5_2qkmn |  | yes |
| r/polandball | t5_2sih3 |  | yes |
| r/Polska | t5_2qiqo | polska | yes |
| r/polyamory | t5_2qu5n |  | yes |
| r/popheads | t5_39nwj |  | yes |
| r/Portal | t5_2qzze | portal | yes |
| r/porterrobinson | t5_2tsz6 |  | yes |
| r/portugal | t5_2qmie |  | yes |
| r/PORTUGALCARALHO | t5_366ul |  | yes |
| r/Predators | t5_2rozp | predators | yes |
| r/PrequelMemes | t5_3i60n | prequelmemes | yes |
| r/Produce101 | t5_38n2q |  | yes |
| r/ProfessorLayton | t5_2snf8 |  | yes |
| r/PUBATTLEGROUNDS | t5_3fmbm |  | yes |
| r/Purdue | t5_2qoyi | purdue | yes |
| r/purplecorner | t5_3jsgl |  | yes |
| r/PurplePixels | t5_3jsbd |  | yes |
| r/pusheen | t5_2tz04 |  | yes |
| r/PuzzleAndDragons | t5_2w23a | puzzleanddragons | yes |
| r/Python | t5_2qh0y | python | yes |
| r/qotsa | t5_2sbyp |  | yes |
| r/Quebec | t5_2qhh9 | quebec | yes |
| r/quq | t5_3ii9b |  | yes |
| r/radiohead | t5_2r3p6 |  | yes |
| r/Rainbow6 | t5_2t1bl |  | yes |
| r/rainbowgrid | t5_3jufd |  | yes |
| r/rangers | t5_2rnpb |  | yes |
| r/raocow | t5_2uh0w |  | yes |
| r/ravens | t5_2s1w8 |  | yes |
| r/Re_Zero | t5_3e076 | re_zero | yes |
| r/ReBoot | t5_2ro1h |  | yes |
| r/reddevils | t5_2rxse |  | yes |
| r/RedHotChiliPeppers | t5_2s504 | redhotchilipeppers | yes |
| r/Redox | t5_3at99 |  | yes |
| r/redpandas | t5_2rck1 |  | yes |
| r/RedvsBlue | t5_2rofm | redvsblue | yes |
| r/RelientK | t5_2st45 |  | yes |
| r/rhythmheaven | t5_2twoc |  | yes |
| r/rickandmorty | t5_2u4lp |  | yes |
| r/ripcity | t5_2rt2i |  | yes |
| r/riskofrain | t5_2wi6h |  | yes |
| r/rit | t5_2qh3x |  | yes |
| r/rocketbeans | t5_2zn9o |  | yes |
| r/RocketLeague | t5_30cz1 | rocketleague | yes |
| r/rojava | t5_358x7 |  | yes |
| r/Romania | t5_2qm35 | romania | yes |
| r/roosterteeth | t5_2s7g9 |  | yes |
| r/RotMG | t5_2s505 | rotmg | yes |
| r/RPI | t5_2rg3u | rpi | yes |
| r/runescape | t5_2qwxl |  | yes |
| r/rush | t5_2r4wq |  | yes |
| r/russia | t5_2qh75 |  | yes |
| r/Russiaclan | t5_3jtna |  | yes |
| r/rust | t5_2s7lj |  | yes |
| r/rutgers | t5_2risk |  | yes |
| r/RWBY | t5_2vhg0 | rwby | yes |
| r/sabres | t5_2raob |  | yes |
| r/sadboys | t5_2xpx7 |  | yes |
| r/Sakartvelo | t5_2s9o3 | sakartvelo | yes |
| r/SakuraGakuin | t5_31mhn | sakuragakuin | yes |
| r/samuraijack | t5_2tlpl |  | yes |
| r/satania | t5_3j1jh |  | yes |
| r/SBU | t5_2sa4t | sbu | yes |
| r/SchoolIdolFestival | t5_31rt4 | schoolidolfestival | yes |
| r/Scotland | t5_2qkli | scotland | yes |
| r/ScottPilgrim | t5_2seyg |  | yes |
| r/SCP | t5_2r4ni | scp | yes |
| r/Seahawks | t5_2ryle | seahawks | yes |
| r/seolhyun | t5_353dc |  | yes |
| r/serbia | t5_2ql0k |  | yes |
| r/seventeen | t5_2spu6 |  | yes |
| r/sheffield | t5_2rab3 |  | yes |
| r/shield | t5_2rz8z |  | yes |
| r/Shishamo | t5_377n4 | shishamo | yes |
| r/ShitRedditSays | t5_2s4m9 | shitredditsays | yes |
| r/shrooms | t5_2qszq |  | yes |
| r/signal | t5_2s9g5 |  | yes |
| r/simonfraser | t5_2rlf7 |  | yes |
| r/singapore | t5_2qh8c |  | yes |
| r/sips | t5_2uts5 |  | yes |
| r/sixers | t5_2scmr |  | yes |
| r/skyrim | t5_2s837 |  | yes |
| r/Slovakia | t5_2qyjb |  | yes |
| r/Slovenia | t5_2s18h | slovenia | yes |
| r/smashbros | t5_2qiep |  | yes |
| r/Smite | t5_2stl8 | smite | yes |
| r/SNSD | t5_2s1g4 | snsd | yes |
| r/SonicTheHedgehog | t5_2rh21 | sonicthehedgehog | yes |
| r/sooners | t5_2r5kj |  | yes |
| r/southafrica | t5_2qney |  | yes |
| r/southpark | t5_2qoqu |  | yes |
| r/soylent | t5_2wmas |  | yes |
| r/spacex | t5_2srow |  | yes |
| r/SpaceXMasterrace | t5_32frp | spacexmasterrace | yes |
| r/spain | t5_2qhd6 |  | yes |
| r/spelunky | t5_2sk9c |  | yes |
| r/splatoon | t5_324q4 |  | yes |
| r/spongebob | t5_2sc60 |  | yes |
| r/SquareSpiral | t5_3jsgm |  | yes |
| r/SS13 | t5_2s9yk | ss13 | yes |
| r/SSBPM | t5_2u3tn | ssbpm | yes |
| r/starbound | t5_2tkp6 |  | yes |
| r/starcitizen | t5_2v94d |  | yes |
| r/starcraft | t5_2qpp6 |  | yes |
| r/StardewValley | t5_2wb7y | stardewvalley | yes |
| r/StardustCrusaders | t5_2tny5 | stardustcrusaders | yes |
| r/Stargate | t5_2qhar | stargate | yes |
| r/StarlightStage | t5_39t20 | starlightstage | yes |
| r/starryknights | t5_3jtf1 |  | yes |
| r/startrek | t5_2qixm |  | yes |
| r/StarVStheForcesofEvil | t5_32uti | starvstheforcesofevil | yes |
| r/stevenuniverse | t5_2viyl |  | yes |
| r/StLouis | t5_2qpnm | stlouis | yes |
| r/stlouisblues | t5_2rlvj |  | yes |
| r/StrangerThings | t5_3adlm | strangerthings | yes |
| r/straya | t5_2tt2t |  | yes |
| r/StreetFighter | t5_2qnu5 | streetfighter | yes |
| r/Summit1G | t5_2xvre |  | yes |
| r/Suomi | t5_2qlq3 | suomi | yes |
| r/superman | t5_2qrwe |  | yes |
| r/survivor | t5_2qhu3 |  | yes |
| r/sweden | t5_2qofe |  | yes |
| r/SwissNeutralityZone | t5_3jsv0 |  | yes |
| r/Switzerland | t5_2qhp6 | switzerland | yes |
| r/swordartonline | t5_2uikt |  | yes |
| r/SydneyFC | t5_2wgd6 |  | yes |
| r/TagPro | t5_2w7hh | tagpro | yes |
| r/taiwan | t5_2qhrg |  | yes |
| r/TampaBayLightning | t5_2rqi8 | tampabaylightning | yes |
| r/teamcube | t5_3jt7u |  | yes |
| r/TeamDignitas | t5_2uqei |  | yes |
| r/TeamYellowPlace | t5_3jsbq |  | yes |
| r/Telegram | t5_2zmr2 | telegram | yes |
| r/Temple | t5_2ro0v |  | yes |
| r/Tenma | t5_3jpd6 | tenma | yes |
| r/Terraria | t5_2sg5b | terraria | yes |
| r/teslamotors | t5_2s3j5 |  | yes |
| r/Tetris | t5_2r133 | tetris | yes |
| r/Texans | t5_2s450 | texans | yes |
| r/texas | t5_2qho4 |  | yes |
| r/TexasTech | t5_2rft2 | texastech | yes |
| r/tf2 | t5_2qka0 |  | yes |
| r/Thailand | t5_2qjw5 | thailand | yes |
| r/The_Donald | t5_38unr | the_donald | no: the yard holds it at brief awaiting validation |
| r/THE_PACK | t5_3e6ue | the_pack | yes |
| r/THE_R | t5_3jti4 |  | yes |
| r/TheAdventuresofTintin | t5_2stct |  | yes |
| r/TheB1G | t5_2vmjf |  | yes |
| r/theblackvoid | t5_3jswk |  | yes |
| r/TheBlueCorner | t5_3jsax | thebluecorner | yes |
| r/TheExpanse | t5_2xi70 | theexpanse | yes |
| r/TheFarLeftSide | t5_3jsf1 |  | yes |
| r/Thegreatblackhole | t5_3jsg5 |  | yes |
| r/thegreatgreenbox | t5_3js8p | TheGreatGreenBox | yes |
| r/thehulk | t5_3jtcu | TheHulk | yes |
| r/TheID | t5_3euw6 |  | yes |
| r/theitalyplace | t5_3jtqc |  | yes |
| r/thenetherlands | t5_30hrx |  | yes |
| r/thepointing | t5_3jsu9 |  | yes |
| r/TheSilphRoad | t5_3c2d7 | thesilphroad | yes |
| r/TheSimpsons | t5_2rhs5 | thesimpsons | yes |
| r/thetreesnetwork | t5_375yn |  | yes |
| r/timbers | t5_2s2lj |  | yes |
| r/tinytardis | t5_3jthd |  | yes |
| r/titanfall | t5_2xh0g |  | yes |
| r/Tokyo | t5_2r812 | tokyo | yes |
| r/ToolBand | t5_2rfjf | toolband | yes |
| r/torontoraptors | t5_2s5sb |  | yes |
| r/totallynotrobots | t5_38rmh |  | yes |
| r/touhou | t5_2qvi5 |  | yes |
| r/traaaaaaannnnnnnnnns | t5_2uog0 |  | yes |
| r/TransFlagPlace | t5_3jsp6 |  | yes |
| r/transformers | t5_2qh5t |  | yes |
| r/transgender | t5_2qxpm |  | yes |
| r/TreePlace | t5_3jsja |  | yes |
| r/trees | t5_2r9vp |  | yes |
| r/TrueSTL | t5_2xiwq | truestl | yes |
| r/TsundereSharks | t5_2zhuq |  | yes |
| r/Turkey | t5_2qlnu | turkey | yes |
| r/twentyonepilots | t5_2u0fp |  | yes |
| r/twice | t5_3812p |  | yes |
| r/Twitch | t5_2s0fe | twitch | yes |
| r/twitchplayspokemon | t5_30dlp |  | yes |
| r/UBC | t5_2qy2j | ubc | yes |
| r/UBreddit | t5_2s46r | ubreddit | yes |
| r/ucf | t5_2qh7r |  | yes |
| r/udub | t5_2razk |  | yes |
| r/ufl | t5_2rjcb |  | yes |
| r/uiowa | t5_2rflf |  | yes |
| r/UIUC | t5_2qkxs | uiuc | yes |
| r/ukplace | t5_3ju18 |  | yes |
| r/ukraine | t5_2qqcn |  | yes |
| r/ultrahardcore | t5_2tswi |  | yes |
| r/UMiami | t5_2spdi |  | yes |
| r/Undertale | t5_2xdht | undertale | yes |
| r/unitedkingdom | t5_2qhqb |  | yes |
| r/UNLincoln | t5_2spam |  | yes |
| r/unturned | t5_2z01g |  | yes |
| r/uofm | t5_2rjkn |  | yes |
| r/uofmn | t5_2s492 |  | yes |
| r/UofT | t5_2rbaq | uoft | yes |
| r/UPenn | t5_2s4l8 |  | yes |
| r/uruguay | t5_2qmvj |  | yes |
| r/UtahJazz | t5_2s5f0 | utahjazz | yes |
| r/UTAustin | t5_2qy08 | utaustin | yes |
| r/UVA | t5_2rcav | uva | yes |
| r/uvic | t5_2ru8r |  | yes |
| r/uwaterloo | t5_2rb5s |  | yes |
| r/vegan | t5_2qhpm |  | yes |
| r/VelvetUnderground | t5_2umjq |  | yes |
| r/vermont | t5_2qqdd |  | yes |
| r/VietNam | t5_2qkcr | vietnam | yes |
| r/villanova | t5_2s4sp | Villanova | yes |
| r/vim | t5_2qhqx |  | yes |
| r/Vinesauce | t5_2uks1 | vinesauce | yes |
| r/VirginiaTech | t5_2r39x | virginiatech | yes |
| r/Vocaloid | t5_2rn75 | vocaloid | yes |
| r/Wales | t5_2qhrl | wales | yes |
| r/wallstreetbets | t5_2th52 |  | yes |
| r/Warframe | t5_2urg0 | warframe | yes |
| r/Wario | t5_2u1i4 | wario | yes |
| r/warriors | t5_2rtiv |  | yes |
| r/Warthunder | t5_2uc6j | warthunder | yes |
| r/Watchmen | t5_2qomm | watchmen | yes |
| r/weezer | t5_2s48r |  | yes |
| r/wholesomememes | t5_3gcwj |  | yes |
| r/wildhockey | t5_2rp0l |  | yes |
| r/wine | t5_2qhs8 |  | yes |
| r/winnipegjets | t5_2ru32 |  | yes |
| r/WisconsinBadgers | t5_2slo5 |  | yes |
| r/witcher | t5_2sebi |  | yes |
| r/WorldofTanks | t5_2s113 | worldoftanks | yes |
| r/worldpowers | t5_30yfr |  | yes |
| r/wow | t5_2qio8 |  | yes |
| r/WPI | t5_2qwa8 |  | yes |
| r/wsu | t5_2roja |  | yes |
| r/Xcom | t5_2si6x | xcom | yes |
| r/Xenoblade_Chronicles | t5_2vcc3 | xenoblade_chronicles | yes |
| r/yerbamate | t5_2ro1q |  | yes |
| r/Yogscast | t5_2sg86 | yogscast | yes |
| r/yugioh | t5_2rpe6 |  | yes |
| r/yumenikki | t5_2s6br |  | yes |
| r/YuYuYu | t5_35vf9 | yuyuyu | yes |
| r/zelda | t5_2r61g |  | yes |
| r/zootopia | t5_2y5oo |  | yes |

## Discarded: the 71 census rows outside the population

| Reddit name | subreddit id | census spelling, where it differs | disposition | in the yard | why |
|---|---|---|---|---|---|
| r/Lehigh | t5_2rpp0 | lehigh | event_talk_after_freeze | yes | J 2026-10-04: no writing about the event while the canvas was open; its first coded turn is at hour 78.98, after the freeze (the coder verdict stands as written) |
| r/Britaly | t5_3juok | britaly | post_freeze_only | no | negative: no items during the 73 hours the canvas was open; 8 items after the freeze, and a coder read canvas talk in them (verdict full) |
| r/ccKufiPrFaShleWoliGtM | t5_3e3tr |  | post_freeze_only | no | negative: no items during the 73 hours the canvas was open; 1 item after the freeze |
| r/edditworldcongress | t5_3juqg |  | post_freeze_only | no | negative: no items during the 73 hours the canvas was open; 71 items after the freeze, and a coder read canvas talk in them (verdict full) |
| r/katamari | t5_2rzxa | Katamari | post_freeze_only | no | negative: no items during the 73 hours the canvas was open; 7 items after the freeze, and a coder read canvas talk in them (verdict trace) |
| r/Snoo | t5_2rsvg |  | post_freeze_only | no | negative: no items during the 73 hours the canvas was open; 7 items after the freeze |
| r/Spc | t5_2st9g | spc | post_freeze_only | no | negative: no items during the 73 hours the canvas was open; 2 items after the freeze |
| r/Touaoii | t5_3juom | touaoii | post_freeze_only | no | negative: no items during the 73 hours the canvas was open; 24 items after the freeze, and a coder read canvas talk in them (verdict full) |
| r/Artsakh | t5_2w743 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/britishcolumbia | t5_2qnc6 |  | screened_out | yes | confirmed: no event talk in 300 window items |
| r/Bunningsnags | t5_3g6dm |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/cesky | t5_2r1ex |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/cologne | t5_2r3rr |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/Connery | t5_2w2p3 | connery | screened_out | yes | confirmed: no event talk in 276 window items |
| r/Cplusplus | t5_2qh6x | cplusplus | screened_out | yes | its coder read no part in the event (verdict none) |
| r/elonmusk | t5_2tr91 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/Femdom | t5_2qyib | femdom | screened_out | yes | its coder read no part in the event (verdict none) |
| r/frankfurt | t5_2s8n1 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/genderqueer | t5_2r1c3 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/GMail | t5_2ql26 | gmail | screened_out | yes | its coder read no part in the event (verdict none) |
| r/Greenlantern | t5_2rmm3 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/Manitoba | t5_2r8t6 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/moon | t5_2qlwf | Moon | screened_out | yes | its coder read no part in the event (verdict none) |
| r/mozilla | t5_2qh4q |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/PEI | t5_2sgat |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/place | t5_2sxhs |  | screened_out | yes | the field, not a case: coded and modelled apart (stage C4) |
| r/PlazaEuskadi | t5_35fng |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/RealGirls | t5_2r5a3 | realgirls | screened_out | yes | confirmed: no event talk in 2259 window items |
| r/redditores | t5_2rxnt |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/riodejaneiro | t5_2rrpr |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/RMTK | t5_37yqr | rmtk | screened_out | yes | its coder read no part in the event (verdict none) |
| r/rollingstones | t5_2sbbq |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/SakuraKyouko | t5_2vqam |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/srpska | t5_32vm0 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/TFLS | t5_3jssn |  | screened_out | yes | its coder read no part in the event (verdict none); a redirect to r/TheFarLeftSide |
| r/TheBeatles | t5_2s75d |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/upvote | t5_2qiu1 |  | screened_out | yes | J 2026-10-04: no writing about the event; its one coded thread asks for upvotes and names no canvas, drawing or placement (the aggregator A1 screen in claude-v41-1 and ... |
| r/valencia | t5_2qn44 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/vixx | t5_2y5rp | VIXX | screened_out | yes | its coder read no part in the event (verdict none) |
| r/Vulfpeck | t5_30wlu |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/Yukon | t5_2s8gf | yukon | screened_out | yes | its coder read no part in the event (verdict none) |
| r/yuri | t5_2qqk8 |  | screened_out | yes | its coder read no part in the event (verdict none) |
| r/AlandIslands | t5_30n1w |  | silent_in_window | no | 2 records in the span, none in the 97-hour window |
| r/alexjokes | t5_30ndh |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/alsace | t5_2uhvt | Alsace | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/bahamas | t5_2rld2 |  | silent_in_window | no | 37 records in the span, none in the 97-hour window |
| r/Burdcrew | t5_3e9sg | burdcrew | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/CactusMccoy | t5_2z8sc | cactusmccoy | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/canwc | t5_3f6ee |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/GioJ | t5_3755b | gioj | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/Honkers | t5_355gg |  | silent_in_window | no | 12 records in the span, none in the 97-hour window |
| r/infiniteapples | t5_2snnh | Infiniteapples | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/isreal | t5_2rmpx | Isreal | silent_in_window | no | 2 records in the span, none in the 97-hour window |
| r/jakkid166 | t5_3g0na |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/Madeira | t5_2uixz | madeira | silent_in_window | no | 2 records in the span, none in the 97-hour window |
| r/Madoka | t5_2tnwn | madoka | silent_in_window | no | 17 records in the span, none in the 97-hour window |
| r/MetisNation | t5_2v9em |  | silent_in_window | no | 1 records in the span, none in the 97-hour window |
| r/MysterySkulls | t5_2yi8j |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/nagisamomoe | t5_3d46w |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/nctsm | t5_3c4vm |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/NefariousSMP | t5_39bdv |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/numberphile | t5_2ximr |  | silent_in_window | no | 10 records in the span, none in the 97-hour window |
| r/onefjef | t5_30pg3 |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/PlazaCatalunya | t5_35fk1 |  | silent_in_window | no | 2 records in the span, none in the 97-hour window |
| r/PlazaGalicia | t5_35fkv | plazagalicia | silent_in_window | no | 8 records in the span, none in the 97-hour window |
| r/robigalia | t5_3jvpg |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/ruinscraft | t5_322wm |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/Sayaka | t5_316d0 | sayaka | silent_in_window | no | 30 records in the span, none in the 97-hour window |
| r/thebutton | t5_36buk |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |
| r/TowerClimb | t5_2tqm4 |  | silent_in_window | no | 1 records in the span, none in the 97-hour window |
| r/WIT | t5_arnp11 |  | silent_in_window | no | empty download: no records anywhere in the 24-day span |

## Considered and not rows: atlas links and makers that name no community

| name | subreddit id | why not a row | detail |
|---|---|---|---|
| u/steven_presents_six |  | not a subreddit | a user page; the user posted about the artwork (#1491 Fishy) only in r/place |
| u/Zequez |  | not a subreddit | a user page; the artwork (#1454) was drawn by his bot; he coordinated r/totallynotrobots, a room |
| u/GoldenBoy9999 |  | not a subreddit | a user page (the atlas link reads /useGoldenBoy9999); #112 Austyn names a friend of the user |
| r/all |  | not a community | a feed, not a subreddit (#1667) |
| r/centuryclub |  | no record | private; the archive holds nothing (#1095, #1703) |
| r/clanicahn |  | no record | no record under any case (#1674, #1834) |
| r/RatHub |  | no record | a group of friends on Discord, by the atlas (#1244) |
| r/transgenderplace | t5_65kcyf | created after the event | first post 2022; its artwork (#123) is credited to three rooms |
| r/ProtectTheT | t5_3ju97 | no writing in the event | first post 2019-06-10; the artwork (#1640) belongs to r/ockytop |
| r/Chelsea | t5_2qixd | wrong subreddit named | a real, dormant subreddit with no record in the 24 days; the artwork (#629) belongs to r/chelseafc |
| r/rockytop | t5_2s4pa | not the community meant | collected while settling the links; the artwork belongs to r/ockytop |
| r/Brazil | t5_2qmku | no record in the span | named as a maker in a description; no post or comment 24 March to 17 April 2017; Blanka (#708) is credited to r/brasil |
| r/pict | t5_2t9n4 | no record in the span | named as a maker in a description; no post or comment 24 March to 17 April 2017 |
| r/spacefarts |  | no record | named as a maker in a description; nothing in the archive |
| r/Czechoslovakia | t5_32pv5 | no record in the span | named in an unlinked description; nothing 24 March to 10 April 2017 |

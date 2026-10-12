# Adjudication packet 4, chunk 18

### 426. haskell/t04, class 3

**sharing and fixing PlaceBot scripts** | note: These passages ask for, generate, limit, run, and update configurations; automation varies from protecting only priority text to accidentally undoing a newer shift and arriving after the canvas closed.

- c0011 | asking for a script | Is there a script?
- c0012 | answering with a PlaceBot script and a config made using JuicyPixels | Open `/r/place` 2. Copy this script into developer console https://grind086.github.io/PlaceBot/dist/placebot.min.js 3. Insert this config into developer console http://lpaste.net/raw/8073720046037237760 The config was made from the image source using [JuicyPixels](https://hackage.haskell.org/package/JuicyPixels)!
- c0013 | revising the config to avoid overwriting others' art and to use the new font and colors | EDIT: a less intrusive version of the config that will not overwrite the art of others with unnecessary white pixels: http://lpaste.net/raw/4408905038831812608 EDIT: new font + colors: http://lpaste.net/raw/2715401684581875712 (as discussed in other comment threads).
- c0028 | sharing how GIMP and GHCi generated the bot configuration | First I scaled the source image in GIMP by the factor of 16 with interpolation set to "None" to get pixel-to-pixel correspondence and saved it as a `.bmp`-file with RGB encoding. Then I've just run a few GHCi commands but to answer your request I put them into a file you can run with `stack runghc MakeTiles.hs`: http://lpaste.net/1444710802329174016
- c0034 | running the script only for the higher-priority text | Running this, but I trimmed the tiles to just the text, since that seems higher priority.
- c0035 | defending while code compiles and finding old scripts undo a shifted logo | It's the same 4 or 5 accounts, which I suspect are all alts running a bot. I keep changing bits back while I wait for code to compile. I also moved the logo 4 pixels to the right to avoid the purple head thing, but it looks like people are running the old script for the logo and it is changing back
- c0036 | admitting an old screenshot and bot were shifting the logo back, then agreeing to update | I would be one of the people trying to shift it back to the left, possibly the only one. I'm actually working off of an old screenshot I managed to find. I have set up a bot now using that shot as a template, though, since I'm going to bed soon. I guess I'll update it to use the shifted-right version
- c0037 | noticing r/place ended just after making another bot template | Well, looks like place just ended. I JUST made a template for the rust bot, too :(

**Reading A:** T3-028 running scripts for the work; T3-089 switching off stale scripts (confidence clear; read whole; families opened G11)
- why T3-028: Scripts and configs are requested, shared, generated and run for the work.
- why T3-089: Old scripts and bots are found shifting the logo back and need updating or stopping.
- added T3-089, own concepts c0035 c0036; why_not_one: T3-028 covers sharing and running scripts but not the room's own old scripts fighting the current shifted plan.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: members ask for, generate, configure and run PlaceBot scripts for the logo, which is T3-028's running scripts for the work.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-089 switching off stale scripts; T3-168 editing scripts to spare neighbours

### 427. heyyea/t02, class 3

**automagically maintaining the heroes** | note: These codes enact a shared defence practice: rallying Eternians, naming hostile changes, distributing automation, installing it, and using it to preserve the heroes. They vary from story-like recruitment to technical setup and actual automated maintenance.

- c0008 | calling fellow Eternians to have He-Man and Skeletor join forces again | That was awesome!! Well fellow Eternians, the time has come yet again!
- c0009 | calling pixel changes an Evil Horde attack putting stuff in their mouths | This time, He-Man and Skeletor are being attacked by a rouge Evil Horde who are trying to defile our favorite super hero and super villain by putting stuff in their mouths!
- c0010 | sharing a site to help in the fight | Fortunately u/DatBlizzard has created the an awesome site to help us in our fight
- c0011 | instructing defenders to install the userscript | You will need to install Greasemonkey/Tampermonkey as well as the userscript from the site linked above.
- c0012 | automagically placing pixels to maintain the heroes | This should allow you to automagically place pixels and maintain our heroes. It's working for me so far.
- c0013 | adding a rainbow to preserve the area around He-Man | The rainbow has been added around He-Man to preserve that area too.
- c0022 | reassuring users and directing them to install the autoscript | You must log into reddit. It is safe, they do not have your password. You must have tamper monkey installed and you need to install this script

**Reading A:** T3-028 running scripts for the work; T3-005 defending the work against attackers (confidence arguable; read whole; families opened G09,G11)
- why T3-028: The userscript, install instructions, and automagical pixel placement make running scripts for the work primary.
- why T3-005: The Evil Horde attack, rally to Eternians, and shared fight site satisfy defending the work against attackers as a distinct act.
- added T3-005, own concepts c0009 c0008 c0010; why_not_one: T3-028 carries the shared userscript and automated placement but not the explicit Evil Horde attack alarm and rally to defend.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11,G09)
- why T3-028: The concepts distribute, install, and run a userscript to automagically maintain He-Man and Skeletor, which is T3-028 running scripts for the work, with defence language as motivation.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work

### 428. iastate/t02, class 3

**getting more people and scripts onto the logo** | note: Participants build a working crowd around the logo; they vary between direct coordinate calls, inviting many accounts, sending people to a bot, recounting the small start, and lowering the barrier with a browser script.

- c0004 | sending everyone to 360, 360 to help the Iowa State logo | Go to r/place and go to the coordinates 360, 360 and help us with the Iowa State Logo
- c0008 | automating the logo and inviting as many accounts as people like | I've automated our logo, https://github.com/matt-moser/reddit-placebot. You can run as many accounts as you'd like with this, and spread it around to as many people as you like.
- c0010 | directing people to the bot that draws the logo | I just posted another comment with a bot to automate drawing the logo. Check it out.
- c0011 | directing people to the bot that draws the logo | I just posted another comment with a bot to automate drawing the logo. Check it out.
- c0017 | calling people to start from the bottom up at 95,753 | The time is now, go to 95,753 and start from the bottom up
- c0027 | recounting three friends starting small before others joined | The first one was just two friends and me until you guys joined in so we wanted to keep it small. If we want to try a bigger logo, go ahead and put something together.
- c0028 | calling for more people as the old logo comes together | The old logo is actually starting to come together again, just need more people
- c0029 | automating the original logo and inviting as many accounts as people like | I've automated our original logo, https://github.com/matt-moser/reddit-placebot. You can run as many accounts as you'd like with this, and spread it around to as many people as you like.
- c0047 | making a browser script because the current one is not getting adoption | I'm also going to put a browser-only script together. It doesn't look like the current one is getting any adoption. Browser-based like DOTA's should be more approachable.
- c0049 | promising to use the browser script | Let us know when you get that one done. I'll definitely use it.

**Reading A:** T3-028 running scripts for the work; T3-002 calling members in to place; T3-088 placing beyond the pixel limit (confidence arguable; read whole; families opened G11,G04)
- why T3-028: Several concepts share, direct people to, and promise to use scripts or bots that automate the logo.
- why T3-002: Other concepts directly call members to coordinates and to help build the logo.
- why T3-088: Concepts invite running the automation with as many accounts as people like, multiplying placements beyond the limit.
- added T3-002, own concepts c0004 c0017 c0028; why_not_one: T3-028 covers scripts and bots but not direct calls for people to come and place by hand at coordinates.
- added T3-088, own concepts c0008 c0029; why_not_one: T3-028 covers running the script but not multiplying placements by inviting many accounts.

**Reading B:** T3-028 running scripts for the work (confidence arguable; read whole; families opened G11,G04)
- why T3-028: The concepts center on writing, sharing and running bots/scripts for the Iowa State logo, with direct calls and extra accounts as supporting means.

**B1 grouping (mine, at B1):** T3-002 calling members in to place; T3-028 running scripts for the work; T3-088 placing beyond the pixel limit

### 429. india/t06, class 4

**running shared scripts and coordination rooms** | note: Participants circulate, update, troubleshoot, and teach shared placement scripts while moving some planning and votes through Discord or linked tools; what varies is overnight defence, expansion, bitmap governance, access for non-technical users, and conflict between automation and manual changes.

- c0036 | inviting builders to the FlagAlliance and its Discord | Join the /r/FlagAlliance and the [discord](https://discord.gg/Vy9DhKe).
- c0041 | sharing a developer-console change for a bigger canvas view | paste this in your developer console(F12) to get a much bigger view of the canvas, I also recommend zooming to 60%
- c0047 | moving the flag bitmap outside the script to end repeated updates | Alright guys I think this will be the last script you will ever have to update. I have now moved the bitmap to an external file so we dont have up update the script again and again
- c0048 | asking how a non-tech person can run the script | Non-tech person here, how do I run the script?
- c0049 | walking a non-tech participant through running the script in Chrome | Use Chrome on desktop. Open r/place in full-screen Press ctrl-shift-I, it'll open developer panel Copy the script from url Paste in the console tab on the developer panel Hit enter And let it run in the background
- c0054 | reporting being kicked out of the Discord chat | I just got kicked out of the discord chat.
- c0104 | moving flag discussion and planning to Discord | Discussions and planning: https://discord.gg/REmwQ5b
- c0201 | telling people to run the updated script before sleep | #UPDATED TO THE LATEST SCRIPT. Run this before you go to sleep.
- c0202 | turning 300 active users into 3000 defensive pixels per hour | Don't think that we can't ever make it, we can! If you contribute, there are around 300 active users on r/india so if everyone just uses 10 pixel per hour then we will be having 3000 pixels per hour which is enough to defend our flag!
- c0211 | offering a script that expands in all directions at a 3:2 ratio | It is the current script but expands in all directions and maintains the 3:2 ratio.
- c0213 | settling on what might be the last maintenance script | This just might be the last script we need.
- c0216 | dividing the script by areas and colours | Can we divide the script to work in certain areas, or colours. the current script doesnt seem very efficient. we can divide the work between us.
- c0219 | using two alternate accounts against the attack | Using two alts to counter pakistani attack on our flag
- c0287 | asking for a fully working r/place script everyone can use tonight | [NP]We need a fully working script for r/place that we can all use tonight
- c0291 | asking what a negative drawing timer means without coding experience | i am getting drawing in -994 seconds. what does this mean? forgive me i am a doctor. no experience in coding
- c0296 | explaining that an increased timer requires waiting | timer increased for you. You need to wait that many seconds.
- c0297 | calling out alts that are not being discreet | They're not even being discreet at this point
- c0298 | telling a user to reload and run the script again | Just reload the page and run the script again.
- c0299 | correcting that new alts cannot take part | New alts can't even take part scrub
- c0369 | asking for copy-paste code to automate the drawing | Does anyone have a copy paste of the code?
- c0373 | asking for an automated way to draw it | Is there some automated way to do it?
- c0401 | directing flag defenders to run one script | Who ever wants to help defend the India flag simply run this script
- c0402 | warning that conflicting scripts overwrite each other | Dont run any other script no matter what. Conflicting scripts just overwrite each other.
- c0403 | putting script features to comment upvotes | If you want new features, just post it as a comment. If it gets a lot of upvotes it shall be considered and I shall update the script.
- c0404 | teaching people to open r/place and run the script | Open https://www.reddit.com/place?webview=true on Chrome
- c0407 | moving r/place discussion to the r/India Discord | We have a Discord discussion on our r/India discord server too just for discussing r/place.
- c0414 | defending a change as what Discord voted | He did what he did based on what the people on discord voted.
- c0418 | calling their Discord a mess | Our discord is a mess!
- c0419 | finding the defense script blocks a manual Taj Mahal change | starting to make the Taj Mahal at the bottom green part won't work because the current script keeps changing it to white
- c0427 | pointing to Discord for r/place | Discord r/place
- c0452 | explaining that DollarAkshay wrote the defense script and others ran it all day | he didn't write it dude. It was written by u/DollarAkshay, we all just ran it on our computers. It had automated system to check pixels in certain coordinate area and check if they are having the desired value or not, if not it will give those pixels that desired value. So instead of sitting whole day and defending your flag on r/place people just ran scripts running on their computer for whole day.
- c0460 | attributing the result to scripts | Because you used scripts.
- c0464 | defending scripts as allowed and working smart | Everyone did and it wasn't disallowed. Work smart not hard.
- c0487 | crediting a more efficient end-stage script update | The script was updated at the end and made much more efficient.
- c0495 | sharing the placement script on GitHub | Ive posted it on my github under Miscellaneous Scripts repo

**Reading A:** T3-028 running scripts for the work; T3-014 moving planning into a chat; T3-088 placing beyond the pixel limit (confidence arguable; read whole; families opened G11,G03)
- why T3-028: Scripts are written, shared, taught, updated and run for the flag; the item's centre is automated placement and maintenance.
- why T3-014: Planning and voting move through Discord and the FlagAlliance room, distinct from script running.
- why T3-088: Alt accounts are used and discussed for extra placements, distinct from scripts and chat.
- added T3-014, own concepts c0036 c0104 c0414; why_not_one: T3-028 alone would not carry the movement of planning and voting into Discord and the FlagAlliance room as the coordination venue.
- added T3-088, own concepts c0219 c0297 c0299; why_not_one: T3-028 alone would not carry the use of extra accounts to place beyond the one-pixel limit.

**Reading B:** T3-028 running scripts for the work; T3-014 moving planning into a chat; T3-088 placing beyond the pixel limit (confidence arguable; read whole; families opened G03,G11)
- why T3-028: Scripts are shared, updated, run and troubleshot for the room's flag work.
- why T3-014: Planning and discussion move into Discord and coordination rooms.
- why T3-088: Alts and extra accounts are used or discussed as extra placing capacity.
- added T3-014, own concepts c0036 c0104 c0407 c0427 c0054 c0418; why_not_one: T3-028 cannot carry moving planning and discussion into Discord or coordination rooms.
- added T3-088, own concepts c0219 c0297 c0299; why_not_one: T3-028 cannot carry the use of alts and extra accounts to place more.

**B1 grouping (mine, at B1):** T3-014 moving planning into a chat; T3-028 running scripts for the work; T3-070 sharing coordinates, templates and how-to

### 430. italy/t07, class 4

**automating and disputing pixel work** | note: Participants write, run, revise, recalibrate, question, and resist scripts and multiple-account routines that maintain or expand drawings.

- c0108 | considering a script but finding it against the game and risky | ho anche pensato di fare uno script visto che continuano a cazzeggiare sulla bandiera ma mi sembra contrario al gioco oltre che alla fine rischiare di essere controproducente in caso di errori/cambi di rotta (vedi il casino UK).
- c0109 | offering to write and test a few lines of code | butto giu due righe di codice, lo testo e poi vedra chi c'è se usarlo.
- c0119 | sharing a Python script to maintain the flag | Ho fatto uno script per mantenere la nostra bandiera, avviatelo con python2 place_italy_flag.py
- c0120 | leaving the flag script running overnight on multiple accounts | Io ora lo lascio andare per la notte sui miei account
- c0121 | adding a list of pixels the script must ignore | Aggiornato, ora si può impostare una lista di pixel da ignorare (linea 17)
- c0122 | asking whether scripting is cheating | ma non e' tipo.. barare? e poi perche' python2 ??
- c0123 | asking the script to stop expanding and leave the rest to humans | Se è lo script, per favore fermalo dov'è, che mantenga quello che c'è e lasci che gli umani facciano il resto.
- c0124 | answering that r/button also had scripts | Nah, anche in /r/button c'erano gli script (che tra l'altro hanno fallito)
- c0125 | offering a new program to protect the flag | Ciao a tutti, ho sviluppato un nuovo programma per proteggere la nostra bandiera https://www.reddit.com/r/theitalyplace/comments/630k5f/nuovo_programma_per_coordinare_i_nostri_sforzi/
- c0129 | warning that drawing the Vespa would conflict with active scripts | Bella, ma ora che c'è gente con lo script attivo andremmo in conflitto
- c0157 | favoring a Vespa but fearing active scripts will prevent it | Io sarei favorevole. Non ha più senso continuare espandersi. Però ho paura che finché ci sarà gente con lo script attivo, sarà un bordello sia contenere l'espansione che disegnare 'sta vespa.
- c0167 | proposing coordinated movement of ITALY and recalibration of bots | Se siete d'accordo e siamo abbastanza coordinati c'è lo spazio per farlo, ovviamente dovrete ricalibrare i bot e cercare di essere più lesti possibile.
- c0174 | calling for a script to remove blue pixels at specified coordinates | Scriviamo uno script per levare i punti blu con x tra 95 e 106 e y tra 316 e 323
- c0294 | saying scripts partly ruined Reddit's brilliant idea | Idea geniale di reddit, ma tutti gli script e compagnia bella l'hanno in parte rovinata. Peccato.
- c0309 | arguing nothing sensible would result without scripts | Senza script non sarebbe venuto nulla di sensato, chi sta attaccato al computer per ore a mettere un pixel ogni 5 min?
- c0314 | insisting eight accounts were switched and clicked by hand without a bot | Aveva 8 account in tutto e non usava il bot, ha switchato tutto il tempo fra un account e l'altro e continuato a cliccare a mano.
- c0339 | saying scripts and uncoordinated rebuilding made a big mess | c'era la prima bandiera accanto alla nostra, poi qualcuno ha postato uno script per fare la bandiera a destra e molti l'hanno messo su e hanno lasciato il computer a farla. nel contempo altri hanno cominciato a rifare la bandiera piu grossa sulla vecchia e non riuscendo a coordinare tutti si e' creato un gran casino.

**Reading A:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair; T3-089 switching off stale scripts (confidence arguable; read whole; families opened G11)
- why T3-028: Members write, share, run, and protect scripts for the flag.
- why T3-027: Members dispute whether scripting is cheating or necessary.
- why T3-089: Members call to stop or recalibrate scripts that conflict with the current plan or Vespa drawing.
- added T3-027, own concepts c0108 c0122 c0124 c0294 c0309; why_not_one: T3-028 alone would not carry the fairness dispute over scripts and multiple accounts.
- added T3-089, own concepts c0123 c0129 c0157 c0167 c0339; why_not_one: T3-028 alone would not carry the conflict of stale scripts fighting the room's own current plan.

**Reading B:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair; T3-089 switching off stale scripts (confidence arguable; read whole; families opened G11,G06)
- why T3-028: Concepts share/run scripts and bots to maintain/expand pixels, the gate for T3-028.
- why T3-027: Concepts argue whether scripting is cheating or okay, the gate for T3-027.
- why T3-089: Concepts call for stopping or recalibrating scripts that fight the current plan, the gate for T3-089.
- added T3-027, own concepts c0108 c0122 c0294; why_not_one: T3-028's gate covers running scripts but not the fairness argument about whether scripting is cheating.
- added T3-089, own concepts c0123 c0129 c0157; why_not_one: T3-028's gate covers running scripts but not stopping stale scripts that fight the room's plan.

**B1 grouping (mine, at B1):** T3-027 arguing whether scripts are fair; T3-028 running scripts for the work; T3-168 editing scripts to spare neighbours

### 431. livecounting/t07, class 3

**running borrowed code to protect the box** | note: These passages share instructing people to automate work on the livecounting box with borrowed code. What varies is sourcing the code, starting it, leaving it running, and multiplying it across browsers and accounts.

- c0054 | sharing code for automatically working on the livecounting box | Copy and paste [this code](https://pastebin.com/LbgvaACX) into the console.
- c0055 | saying the automation code came from r/wallstreetbets | I stole it from /r/wallstreetbets
- c0056 | telling defenders to leave the automated tab running | Keep the tab open and don't touch it.
- c0057 | running the defence code through multiple accounts | Open up an incognito/private browsing window and other browsers so multiple accounts can run it.

**Reading A:** T3-028 running scripts for the work; T3-088 placing beyond the pixel limit (confidence arguable; read whole; families opened G11)
- why T3-028: Borrowed console code is shared, sourced and left running to automate work on the box, so scripts are run for the room's work (T3-028).
- why T3-088: Defenders are told to open incognito windows and other browsers so multiple accounts can run it, using extra accounts to place more (T3-088).
- added T3-088, own concepts c0057; why_not_one: T3-028 carries the borrowed automation code but not the instruction to multiply it across incognito windows and other browsers so that several accounts run it, which is its own act.

**Reading B:** T3-028 running scripts for the work (confidence arguable; read whole; families opened G11)
- why T3-028: Members share a pastebin script for automatic work on the livecounting box, source it from another sub, and tell defenders to keep the tab running - a script made, shared and run for the room's work (T3-028); the single incognito/multi-account line is a mode of running that script and does not form a distinct act of its own.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-088 placing beyond the pixel limit

### 432. minnesotavikings/t09, class 3

**running, correcting, and arguing over placement scripts** | note: These codes describe using scripts to place or maintain pixels, publishing versions, finding errors, routing fixes, and disputing scripting; what varies is the target, the failure, and whether automation is welcomed.

- c0158 | publishing a final template with fixed horns and face | here is the final template! the horns have been fixed and the face is one pixel skinnier! lets get it looking crisp!
- c0159 | reporting a no-wait glitch used to add many squares | I was able to add about 30 purple and gold squares, and I didn't have to wait between clicks. It was a like a glitch in the system.
- c0175 | making script changes conditional on consensus | If there's any kind of consensus for this (I'm okay with it), he could add it to the script.
- c0177 | calling skoldiers for help while the post body is removed | skoldiers we need your help in r/place!
- c0178 | publishing an updated placement script | just updated script, this is new: https://pastebin.com/raw/gVfBDKqx
- c0179 | proposing building around r/drugs rather than destroying it | maybe we should just build around the r/drugs logo. Seems like a dick move to destroy it.
- c0180 | adding r/drugs to the script to stop fighting | ill add their stuff in an update in a bit so we arent fighting them
- c0183 | testing the script and reporting two failures | I don't see any changes to account for r/drugs. Also, this doesn't seem to place any black.
- c0184 | acknowledging and fixing a failed update | ahh, you were right, didnt update for some reason. fixed now.
- c0185 | debugging the purple colour line | you now need a "," after the 15 for purple.
- c0186 | checking that the tester uses the latest script | yeah i caught that, are you using this one? https://pastebin.com/raw/QQsmCrt9
- c0190 | apologizing for script leakage and promising to build around r/drugs | We had some bot scripting issues that may have leaked. They should be fixed now. We plan on building around you guys. =]
- c0192 | calling for proper hosting and versioning | Why don't we host this somewhere and/or use proper versioning instead of "no this one, now this one, no this one is better."
- c0193 | answering versioning criticism defensively | sorry its not perfect. your welcome to do it yourself.
- c0217 | announcing a possibly final bot update while the body is removed | /r/Placers, we have an update to the bot. (final?)
- c0219 | updating the script to include the shared heart | ive just made an update to include this
- c0221 | asking users to refresh after another template mistake | please refresh the bot if you got the link in the last 30 mins, i made a template mistake (again).
- c0222 | seeking agreement before updating the bot | im thinking i'll update the bot to this but i want to make sure everyone agrees first.
- c0223 | voting for the proposed bot update | Gets my vote
- c0228 | trying to put up a scripted purple #4 to mock the Packers | We've been trying to put a purple #4 to mock the packers there for awhile, and we have a much of scripts going. Probably best to pick a safer spot.
- c0231 | sending the proposal to the person setting their bot scripts | we were planning on centering the logo today. Your best bet is talking to /u/pvt13krebs he has been setting the bot scripts for us.
- c0235 | reporting that the r/place bot thread went missing | r/place thread bot thread seems to have gone missing
- c0256 | asking the moderator what happened to the bot post | and uh, what happened to my post?
- c0259 | making a Discord script to maintain the drawing automatically | We made a script in the discord to automate this so that it's maintained automatically:
- c0261 | spreading the plan while trying to replace an out-of-date image | We can't control everyone, and it looks like we're just getting the word out now. I'm trying to spread the link to the image, but I'm also hearing the one I'm linking is out of date. I'll go back and update my comments with the new one once I hear back.
- c0262 | thanking them and spreading the updated plan | Thanks mate, spreading the word now.
- c0263 | running the script all day and recruiting more helpers | Running the script all day at work! Let's get some more people helping it's super easy!
- c0271 | opposing scripting and saying their sub lacks clear messaging | Though personally I'm anti-scripting, I don't know if the script is updated yet. We don't really have clear messaging on our sub atm.
- c0273 | coordinating a shared final script with the Packers | We are coordinating with the packers to all run this same script and this will be the final result
- c0274 | correcting the planned update because Place is over | No you're not, Place is over :D
- c0275 | stopping updates after Place ended | no more updating
- c0285 | taking pride across the scripting dispute and promising to own the 4 next time | I am really proud of what our subreddit did. Regardless of how you feel about scripting or not scripting, we did something great. Next time we can accomplish more, next time we will own the 4.
- c0288 | expecting another r/place after its popularity and calls for a script-less event | I legitimately don't know for sure, but considering how widely popular this one was AND people clammoring for a script-less event, I'd be surprised if they don't.

**Reading A:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: Scripts are published, updated, run, and debugged for the room's pixels; the anti-scripting remarks are secondary to running and correcting the placement code.

**Reading B:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair (confidence clear; read whole; families opened G11)
- why T3-028: The theme is centrally about publishing, updating, testing, and running placement scripts and bots.
- why T3-027: It also carries an explicit dispute over whether scripting is acceptable and calls for a script-less event.
- added T3-027, own concepts c0271 c0285 c0288; why_not_one: T3-028 cannot carry the argument over whether scripting is fair or the call for a script-less event.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-066 putting decisions to a vote; T3-108 sharing one bot target

### 433. monero/t05, class 3

**running scripts and fighting their mistakes** | note: These codes share the practice of automating placement and managing what that automation does; they vary between disputing whether scripts are cheating, teaching and releasing versions, stopping rogue bots, seeking consensus, and handling incompatible copies.

- c0056 | asking to modify Bitcoin's maintenance script for Monero | Someone made a script to automate Bitcoin logo maintenance on r/place . Can we modify this for Monero?
- c0057 | objecting that automation would turn community effort into cheating | I was proud to see the community come together to make this thing happen. What's the fun in cheating?
- c0058 | defending automation as a way to even the odds | I don't think it's unreasonable to even the odds with a bit of automation :)
- c0059 | preferring to keep fighting instead of accepting the logo's end | No thanks, I prefer to keep fighting.
- c0070 | teaching people how to run the placement script | USAGE: go to webpage -> F12 -> console -> paste -> enter -> keep tab open
- c0073 | saying the unattended bots have gone rogue | Shit I'm at work an the script is running on my machine. The bots have gone rogue!
- c0076 | combating one's own bot | I'm doing my best to combat my own bot. o7
- c0077 | slaying a rogue bot with another member's tip | My rogue bot has been slain thanks to a tip from needmoney90. :)
- c0080 | joking that script changes need Proof of Place consensus | We need consensus. Perhaps we can switch to PoP(Proof of Place). ;)
- c0081 | warning that differing unattended scripts make helpers fight each other | releasing different scripts is hindering us because people are running old scripts whilst asleep and we are fighting each other
- c0083 | releasing v4 for the community's bots | Latest script just released. v4 is ready for your bots.
- c0090 | announcing the final V4 script and asking everyone to update | WELCOME THE LOGO: Final V4 /r/place script is here. Please update your browsers!
- c0121 | telling Monero not to use scripts on r/place | Guys u are not supposed to use scripts on the /r/place
- c0122 | arguing it would be unsportsmanlike not to use scripts when everyone does | wouldn't it actually be unsportsmanlike if we didn't use scripts in an environment where everyone else is using it? :D
- c0123 | calling script users sore losers and contrasting them with Discord organizing | U guys are sore losers , instead of acting like weebs and be on a discord like we do (100 people in a channel atm) , but yeah lets compare bots to doping .
- c0124 | defending bots as necessary to survive | Without our bots we would have been wiped out completely. Gotta do what you have to to survive.
- c0129 | saying we are destroying us with our own weapons | noooo we are destroying us with our own weapons xD
- c0130 | maintaining consensus while versions make people fight each others edits | I want to maintain consensus so I'll go along with new versions. But I must say I really preferred v1. Now that we're changing things so much a lot of people are unknowingly fighting each other's edits.

**Reading A:** T3-028 running scripts for the work (confidence arguable; read whole; families opened G11)
- why T3-028: The item centres on running, sharing and releasing scripts/bots for the Monero work, including managing rogue bots, which is the gate for running scripts rather than merely arguing their fairness.

**Reading B:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair; T3-089 switching off stale scripts (confidence arguable; read whole; families opened G11)
- why T3-028: Members teach, release and run placement scripts and bots.
- why T3-027: They argue whether scripts are cheating, fair, unsportsmanlike or necessary.
- why T3-089: They also deal with their own rogue or conflicting scripts and try to stop/update them.
- added T3-027, own concepts c0057 c0058 c0121 c0122 c0123 c0124; why_not_one: T3-028 carries writing, teaching and releasing scripts but not the dispute over whether automation is fair or cheating.
- added T3-089, own concepts c0073 c0076 c0077 c0081 c0130; why_not_one: T3-028 carries running scripts but not the room's own scripts going rogue or fighting each other.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work

### 434. monstercat/t11, class 3

**sharing and aligning scripts with the chosen design** | note: These passages use browser or AFK scripts to place pixels, then troubleshoot competing patterns by updating a script to the design people chose.

- c0214 | sharing Protostar's AFK script | [proto made a script if you want to help while being afk](https://twitter.com/Protostar_UK/status/848742254923718656)
- c0215 | sharing an AFK r/place script for Protostar | /r/place script for Protostar's logo while being afk
- c0225 | telling people how to paste the placement script | I've edited the script so we can get the title above the logo finished. It fits with [this](http://i.imgur.com/Q1Kus97.png) Paste the text from [here](https://pastebin.com/XEGY7kzQ) into your browsers console and hit enter.
- c0226 | warning that two patterns have teams working against each other | Another thread on here suggested [this](http://i.imgur.com/Q1Kus97.png) earlier, which is much easier to read an uses less space. There's basically 2 or more teams with different patterns working against each other right now.
- c0227 | updating the script to the shared design | Oh sorry, I'll update the script to that design!

**Reading A:** T3-028 running scripts for the work; T3-089 switching off stale scripts (confidence clear; read whole; families opened G11)
- why T3-028: The item shares and troubleshoots AFK placement scripts so members can place or maintain the Monstercat work.
- why T3-089: It also warns that competing patterns are fighting each other and updates the script to the shared chosen design, bringing the room's scripts into line.
- added T3-089, own concepts c0226 c0227; why_not_one: T3-028 alone would not carry the correction and updating of scripts that are fighting the chosen design.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: The item shares, installs and updates AFK or browser scripts that place pixels and repair the Monstercat or Protostar work.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-089 switching off stale scripts

### 435. pathofexile/t13, class 3

**using scripts and bots to keep the picture in shape** | note: These codes offer, run, justify, or thank automation used for placement and repair; attitudes range from feeling dirty to saying it was worth it.

- c0108 | suggesting a browser script to auto-paint the PoE logo | they are running a script in their members browsers to auto-paint the american flag
- c0109 | sharing a script modified for the logo | Here is a script modified for our logo:
- c0110 | telling painters how to run the logo script | paste the above script into the console and hit enter
- c0325 | thanking a builder for setting up bots against griefing | for helping us set up a couple bots to deal with griefing
- c0328 | feeling dirty about botting | I feel so dirty botting..
- c0329 | justifying bots because flames were hard to repair pixel by pixel | We had to fix the flames, sadly. They were hard for people to repair pixel by pixel.
- c0330 | saying the bot was worth it and they would bot again | Yeah, it was worth. Would bot again.

**Reading A:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: Members share a script modified for the logo (C0611815), tell painters how to run it (C1056677) and set up bots against griefing (C0416359): scripts run for the room's work, not their fairness argued (T3-027).

**Reading B:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair (confidence arguable; read whole; families opened G11)
- why T3-028: the codes share and run a script/bots for the logo (here is a script modified for our logo, paste it into the console, thanking a builder for setting up bots against griefing), T3-028's gate.
- why T3-027: a distinct set argues the fairness of botting (feeling dirty about botting, justifying the bots because the flames were hard to repair by hand, saying it was worth it and they would bot again).
- added T3-027, own concepts c0328 c0329 c0330; why_not_one: T3-028's gate is running and sharing the script and cannot carry the codes that judge whether botting is fair or embarrassing.

**B1 grouping (mine, at B1):** T3-027 arguing whether scripts are fair; T3-028 running scripts for the work

### 436. pepe/t04, class 3

**setting up bots, targets and Discord to keep Pepe up** | note: These passages organise a build through a bot file, placement choice, remote target, simultaneous running, friends, Discord and direct questions. The shared practice is setting up how people can act together; the tools and venues vary.

- c0024 | offering a bot file after starting work | I actually already started work on this, and have a file for [the bot](https://github.com/Zequez/reddit-placebot) if anyone would like to help me.
- c0025 | placing a nervous Pepe in the white triangle | That said, it's a nervous Pepe rather than a happy Pepe, and in the white triangle above the flag.
- c0026 | giving the remote target file | The remote link to use for the target is https://dl.dropboxusercontent.com/s/yfkpea8e5wxprea/target.bmp?dl=0
- c0027 | saying enough people running the bot can keep him up | If enough of us run the bot at the same time they won't be able to keep him down.
- c0028 | saying Pepe deserves representation on r/place | Pepe have have fallen on hard times with the slander against him, but he's still an important part of internet history that deserves representation on r/place
- c0035 | starting a Pepe with friends and looking for support | Two of my friends and I have started to make a pepe at https://www.reddit.com/r/place/#x=1&y=625, and we are looking for support.
- c0036 | making a Discord with the Pepe pixel reference | We have made a discord which has a reference to a pixel image of Pepe. You can find it here https://discord.gg/2KCnM.
- c0037 | inviting questions and saying Kek wills it | If you have any questions feel free to message me, and Shadilay my brothers. Kek wills it!

**Reading A:** T3-028 running scripts for the work; T3-014 moving planning into a chat (confidence arguable; read whole; families opened G11,G03)
- why T3-028: Bot file, remote target and simultaneous running make scripted maintenance the leading act.
- why T3-014: A Discord is set up with the Pepe pixel reference and invite, a chat venue distinct from the bot itself.
- added T3-014, own concepts c0036; why_not_one: T3-028 covers the bot and target but does not reach the separate act of making a Discord venue for the canvas work.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: The passages set up and share a bot file, remote target, and simultaneous running to keep Pepe up, which is the running of scripts/bots for the room's work.

**B1 grouping (mine, at B1):** T3-014 moving planning into a chat; T3-028 running scripts for the work; T3-037 arguing the canvas's worth

### 437. python/t05, class 4

**tracking pixel changes for later** | note: These turns share and defend a tracker that reconnects to the feed, writes pixel changes, and keeps positions, colours, and order for later use. What varies is whether the speaker describes the machinery, the retained data, or why the personal-purpose tool is worth making.

- c0074 | sharing a script that tracks new r/place pixels | I made a very brief script that tracks new pixels added to r/place!
- c0076 | restoring the pixel feed and writing new pixels to a file | Automatically setup and restore (when the connection breaks) a connection to the web server that pushes out the pixel updates. * Write new pixels continuously to a file. * Grab the most recently placed pixel.
- c0077 | keeping pixel positions, colors, and placement order for later use | I only care about the the pixel positions, colors, and relative order of placement time, so I didn't put anything in there to track who placed what pixel exactly when.
- c0078 | defending the tracker as scratching a personal itch | To scratch a personal itch.. He said so right in the post

**Reading A:** T3-028 running scripts for the work (confidence arguable; read whole; families opened G11,G21)
- why T3-028: The item is a script/tracker made and shared for r/place pixel changes, so it sits with running scripts for canvas work rather than saving finished screenshots or timelapses.

**Reading B:** T3-028 running scripts for the work (confidence arguable; read whole; families opened G11)
- why T3-028: The item's concepts are a script/tracker shared and run for r/place work, so it satisfies running scripts for the work rather than saving visual records or arguing fairness.

**B1 grouping (mine, at B1):** T3-105 saving screenshots and timelapses

### 438. quebec/t12, class 3

**scripting placements and synchronizing design changes** | note: These passages turn repeated pixel placement into a coordinated technical routine. They vary between recommending automation, giving commands, looping defence, and preventing scripts from fighting revisions.

- c0101 | endorsing automatic placement through the pinned thread | Ouais, c'est pas mal plus efficace d'avoir ton ordi qui place les trucs tout seul. Check le fil punaisé.
- c0102 | sharing the placer.py command and coordinates | python placer.py myimage.jpg 370 242 MyUsername MyPassword
- c0126 | giving the command for the pixel placing script | python placer.py myimage.png 370 242 MyUsername MyPassword
- c0127 | warning that scripts will fight a new design unless changed together | Le problème pour changer le design à ce point est que tout le monde qui ont des scripts vont devoir changer en même temps parce que sinon ils vont se battre contre le nouveau design.
- c0135 | putting the placer script in an infinite loop | J'ai mit ça dans une boucle infinie maintenant
- c0137 | synchronising on a time to change the design | Ensuite on se synchronise sur une heure de changement.
- c0155 | using a tutorial made by people from 4chan | Les gens de 4chan nous ont fait un joli tutoriel ici: https://www.reddit.com/r/4chan/comments/62wqjx/rplace_python_script_tutorial/

**Reading A:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: The concepts share and run placer.py, infinite loops, and a script tutorial; the nearest T3-027 would require arguing their fairness, which is absent.

**Reading B:** T3-028 running scripts for the work; T3-089 switching off stale scripts (confidence clear; read whole; families opened G11)
- why T3-028: Scripts and commands for automatic placement are endorsed, shared, and looped for defence.
- why T3-089: Warnings that scripts will fight a revised design unless changed together, and synchronising the change time, concern stale scripts against the plan.
- added T3-089, own concepts c0127 c0137; why_not_one: T3-028 does not carry the conflict when existing scripts fight a revised design.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-089 switching off stale scripts

### 439. rpi/t06, class 3

**running, fixing, and disputing the placement bot** | note: The common practice is making automated placement usable and consequential: borrowing and modifying scripts, restoring instructions, leaving tabs running, updating boundaries, diagnosing duplicate pixels, and challenging whether botting ruins the event. It varies between technical maintenance, coordination through Discord, and explicit moral criticism.

- c0037 | moving strategy talk into the RPI Discord | Come join us in the RPI discord to talk strats. https://discordapp.com/channels/163479540683767810/163479540683767810
- c0041 | claiming scripts and numbers could win | We could probably win since we have a few scripts floating around and numbers, though, was the point.
- c0045 | sharing a console script for the new plan | here](https://pastebin.com/np7Q8ZTR)'s a script. Open the dev console with f12, go to "console", and paste this in there.
- c0064 | recruiting help for a found spot without manual work | We've found a spot, help us out on r/place without doing any work!
- c0069 | posting a new script made by someone in Discord | new script](https://pastebin.com/raw/jDAmtzVf) courtesy of one of the others from the discord.
- c0070 | asking for deleted bot instructions | The thread with instructions on how to setup the bot was deleted. How do you set it up?
- c0071 | restoring the bot instructions | updated to have that info.
- c0072 | checking whether the bot should be left running | Awesome, thanks. So I just leave it running, right?
- c0073 | explaining how long to leave the bot running | The bot will run for as long as you leave the tab with the extra code in the console running.
- c0079 | asking where the bot came from | The bot is a nice touch. You came up with it or did you find it somewhere?
- c0080 | modding Purdue's bot in Discord for RPI's new spot | We had a guy on the rpi discord mod Purdue's bot, and we've coopted it for our new spot.
- c0081 | announcing a replacement bot | NEW BOT TO RUN AS OF 8:45 4/3
- c0094 | redirecting renewed attack talk to running the current bot | If you'd like to help out, running the currently linked bot is the most effective way to participate.
- c0097 | keeping the current script posted through the morning | Good morning! We're still at it! I'll be updating this comment with the most recent iteration of the script being used.
- c0098 | noticing the bot duplicates pixels | Anyone notice duplicate pixels being placed?
- c0099 | proposing ways to stop duplicate pixel placements | Perhaps we need the script to check a central list of transactions so they are not duplicated. Or randomise the targetPoint so it is not likely that two of us are placing a color on the same pixel?
- c0100 | inviting a bot improvement to be shared on Discord and Reddit | Feel free to implement that feature, and you or I can post it to the discord and here for use.
- c0101 | offering to inspect the bot improvement without committing | I will give it a look when I can, at work though so not sure I can commit for sure.
- c0102 | thanking the person offering to inspect the bot | thanks!
- c0103 | calling botting a dick move that ruins the fun | why are we botting? that's just ruining everyone's fun here. In bird culture that would be considered a dick move.
- c0104 | challenging the community for supporting botting | why are we supporting botting? its ruining the fun of r/place

**Reading A:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair (confidence clear; read whole; families opened G11)
- why T3-028: Scripts and bots are shared, run, updated, and diagnosed for RPI's placement.
- why T3-027: Members explicitly challenge botting as ruining fun and ask why it is supported.
- added T3-027, own concepts c0103 c0104; why_not_one: T3-028 covers running and fixing the bot but not the moral argument that botting ruins the event.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: The concepts are about making, sharing, running, restoring and fixing placement scripts/bots for RPI's work, which is T3-028; the fairness dispute is present but secondary.

**B1 grouping (mine, at B1):** T3-027 arguing whether scripts are fair; T3-028 running scripts for the work

### 440. runescape/t13, class 3

**Building drawings pixel by pixel and by script** | note: Participants turn designs into pixels, share or revise scripts, and report construction progress; the means vary between manual placement, multiple accounts, and browser automation.

- c0321 | offering a script to draw a RuneScape icon faster | I've written a script that will attempt to draw a Runescape icon on /r/place. The more people running it, the faster it will be drawn!
- c0322 | telling people to paste the script into the browser console | paste it into your browser's console
- c0325 | editing their script and hoping others get the message | I edited it on my end but hopefully everybody else gets the message.
- c0326 | asking helpers to switch to the newer script | I ask all that are helping out to switch to this script.
- c0329 | running a browser script that keeps adding pixels | To run the script, go to /r/place, open your browser console (usually with F12), paste it in and hit enter. After that, you can just leave the tab open and it'll continue to add new pixels whenever it can.
- c0331 | asking for a placer script for the connection lost drawing | could we get a placer script for the "connection lost" in the top left corner that we're trying to do?
- c0332 | working on the requested placer script right now | i'm working on that right as we speak
- c0333 | working together to draw and maintain the RS logo by script | We're all working together to draw and maintain the RS logo by running that script.
- c0334 | reporting the logo over halfway done | logo is over halfway done!
- c0352 | thanking Two101 for the script | Thanks /u/Two101 for the script!
- c0358 | stopping the new script without RS at the bottom | I have stopped the new script, and am running the original one without the added "RS" at the bottom.
- c0360 | keeping the script running while others are probably asleep | I still have the script running, but I doubt many other people do.
- c0367 | battling themselves over moving Lost one pixel | "Lost" all needs to move to the right 1 pixel. Right now we are battling ourselves trying to do it.
- c0368 | keeping it exactly as it is instead of perfecting it | everyone's just keeping it exactly as is
- c0419 | explaining how to keep the script drawing new pixels | To run the script, go to r/place, open your browser console (usually by pressing F12), paste the script into there and hit enter. The script will continue to run and draw new pixels as long as you keep the tab open. I've added a 2-second delay between requests because people were getting kicked off their connections by the Reddit servers for sending too many requests.
- c0421 | maintaining the logo manually and appreciating the script | Shame this is getting downvoted. I've been trying to help maintain the logo, but doing it manually. Appreciate the script!
- c0423 | reporting that the script waits but never shows the cooldown | I don't think it works for me. It tells me when it's attempting to place a pixel, and that it's waiting, but I never see the 5 minute cooldown on screen. Edit: Pretty sure it just desynchs me.
- c0424 | calling the script use botting | Ban this man for botting
- c0425 | explaining that the script places through the API | The actual application doesn't know about the pixel you placed because the script goes directly via the API.
- c0428 | claiming to have made the dead pixel | See that dead pixel right in the middle? I did that.
- c0429 | asking for the proper image | link to proper image?
- c0430 | offering the proper image by PM | I can PM it too you if you want, I can't target specific players on this sub
- c0431 | accepting the offer of an image by PM | yeah feel free
- c0448 | sharing an improved script that draws only the R | Link to the improved script by /u/Two101 (this only draws the "R" and nothing else): https://pastebin.com/raw/PDuQT9YS
- c0450 | complaining about the script's informative errors | I love the informative errors. Bollocks
- c0452 | saying they do not get it | I don't get it
- c0460 | running six accounts on the RS script and offering a link | I have 6 or so accounts running the rs one but other people are as well so I am just going to make my own place. I'll get you a link though
- c0462 | sharing the original script | Original script can be found here: https://pastebin.com/raw/WNHNm5Fe
- c0477 | pointing out scripts that auto-replace altered pixels | You realize people just set up scripts that auto replace altered pixels whenever they get a chance, right?
- c0479 | explaining that scripts can afk-replace pixels | A lot of the art pieces on r/place have scripts that people can use to afk replace pixels. It'll still show up as them "clicking the pixel" but it's automated, they're not actually manually there doing it.
- c0510 | claiming five-minute clicking made this nothing | We have mastered the art of clicking once every five minutes avoiding the auto log out while afk training. This? This is nothing.
- c0515 | joking that repetitive clicking prepared them for pixels | “Ah you think repetitive clicking is your ally? You merely adopted the clicking. I was born in it, molded by it. I didn't see the pixel until I was already a man, by then it was nothing to me but pixelated!”

**Reading A:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: Concepts centre on writing, sharing, and running scripts/bots to draw and maintain RuneScape art (offering script, paste into console, switch script, run by script), matching T3-028 rather than T3-038's manual build.

**Reading B:** T3-028 running scripts for the work; T3-088 placing beyond the pixel limit (confidence arguable; read whole; families opened G11)
- why T3-028: The item is built around scripts and bots shared, edited, run in the browser console, and left running to place or maintain pixels.
- why T3-088: C0734432 says six or so accounts are running the RS script, placing beyond the one-pixel limit by extra accounts.
- added T3-088, own concepts c0460; why_not_one: T3-028 covers scripts and bots but not the distinct extra-account means of placing beyond the one-pixel limit.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-038 building and reporting the mark

### 441. rutgers/t15, class 3

**automating defense while keeping art human** | note: A poster adapts, checks, explains, and shares a browser script, protects the neighboring border, and justifies automation for correction while reserving art-making for people; the bare reply shows reception without clarifying agreement.

- c0172 | adapting one of the floating r/place scripts | I got this script the /r/place scripts that are floating around.
- c0173 | sharing a browser script that automatically corrects the logo's colors | They came up with this javascript script that you can run in your browser that will automatically check our coordinates for the correct colors, and use the layout provided to correct it. Set it and forget it!
- c0175 | justifying bots for defense while reserving art-making for people | Shoutout to NE bc I basically copied their post to say how it worked. Also, I'm not a huge fan of bots, but with everyone else using bots, it becomes really difficult to keep art up. I think as long as we make the pixel art ourselves, but only use bots as defense, it's acceptable.
- c0176 | responding to the shared defensive script with its bare name | script
- c0191 | asking others to check the pasted script and combining a shared image with the existing canvas layout | Here is the link to the script: https://pastebin.com/yvmvdpK5 Somebody should take a look and correct any mistakes I made in the given image. I used this image + what we already had on /r/place to determine the final layout: http://imgur.com/a/Wuj58
- c0192 | giving browser setup instructions and defining the script's tile space | Simple Usage Firefox: go to webpage -> F12 -> console -> paste in script -> enter -> keep tab open Chrome: Go to webpage -> view menu -> developer -> console -> paste script -> enter -> keep tab open Advanced Usage For auto script runs after page refresh tampermonkey. For up to date data Easy auto refresh Script includes 30x16 tile space. Coordinates in script determine the top left most point.

**Reading A:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: The passages share, adapt and explain a browser script that automatically corrects the logo's colours and protects the border, so scripts are run for the work rather than only debated.

**Reading B:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair (confidence clear; read whole; families opened G11)
- why T3-028: Scripts are adapted, shared, explained and run to auto-correct the logo, satisfying running scripts for the work.
- why T3-027: C1187636 argues bots are difficult to avoid and acceptable only for defence while art stays human, an argument about script fairness.
- added T3-027, own concepts c0175; why_not_one: T3-028 alone would not carry the explicit ethical justification that bots are tolerable only as defence while the art itself remains human.

**B1 grouping (mine, at B1):** T3-027 arguing whether scripts are fair; T3-028 running scripts for the work

### 442. sbu/t02, class 3

**building and helping people run the logo script** | note: These passages make automated placing usable: creating and reposting the script, showing its target image, giving download instructions, troubleshooting operating systems and errors, checking whether it works, and arguing over whether scripts are acceptable. They vary between practical setup help and justification or criticism of scripted placing.

- c0004 | creating a script to place the SBU logo every five minutes | I created a python script that will create an SBU logo in /r/place if enough people run it. It'll automatically place a tile in the appropriate place on your behalf every five minutes.
- c0006 | showing what the logo will look like if enough people run the script | If enough people run it, this is what it will look like: http://i.imgur.com/RbCYPAQ.png
- c0007 | telling people how to download and run the script | To run the script, click [here](https://github.com/shaansheikh/redditPlaceSBU/blob/master/redditPlaceSBU.py) to download it, and then run it using
- c0010 | asking where to paste the script | Where do I paste that to get it to work?
- c0011 | asking which OS to troubleshoot the script | What kind of OS do you use? OSX or Windows or Linux?
- c0012 | answering that the script user has Windows 8 | Windows 8
- c0013 | getting the script working and asking how to check | I think I got it working, how do I check?
- c0017 | answering that most images are maintained by scripts | No, the majority of images there are maintained by scripts.
- c0018 | arguing Reddit encouraged scripts by making the API simple | Reddit intentionally made the api for place simple to make writing scripts easy. It's clear they expected and encourage writing scripts.
- c0023 | disputing the script defence from a large mods-only Discord | This is beyond false. I am a mod in a discord server with over 2000 users that handles almost exclusively mods of place groups. Mods only. And we get at least 75 joiners an hour. This is way bigger than you think.
- c0029 | reporting a requests import error while trying the script | This is lit!! I run into an import error unfortunately, it says: No module named 'requests'.
- c0037 | posting another script thread for the SBU logo | Script to create SBU logo on /r/place

**Reading A:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair (confidence clear; read whole; families opened G11)
- why T3-028: Most concepts create, share, install, troubleshoot, and run the SBU logo script, which is the running-scripts gate.
- why T3-027: Separate concepts argue whether scripts are acceptable, with claims about Reddit's API and a large mods-only Discord, so the fairness argument has its own support.
- added T3-027, own concepts c0017 c0018 c0023; why_not_one: T3-028 alone would not carry the explicit dispute over whether scripted placing is fair or cheating; that argument is not script-running itself.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: Scripts created, shared, run, and troubleshot for the room's logo work.

**B1 grouping (mine, at B1):** T3-027 arguing whether scripts are fair; T3-028 running scripts for the work

### 443. texans/t14, class 3

**automating protection while questioning and fixing scripts** | note: Participants share and recruit users to an auto-protection script, synchronize versions, modify its contents, defend using it, question its point, and admit version conflict; the practice includes both adoption and objection.

- c0105 | sharing a script to auto-protect the logo | This script will auto protect our logo for you
- c0106 | recruiting more people to run the protection script until the end | The more people running it the better. Hopefully this way we can last until the end.
- c0107 | coordinating script updates to avoid working against each other | keep your script up to date so we are not working against each other
- c0108 | offering to remap and republish the script with FTC | I'm happy to remap and republish the script to do that.
- c0109 | approving a little FTC box in the script | if you want to add a little box around FTC that'd be awesome
- c0110 | questioning whether group scripts defeat the point | If everyone runs scripts for their group, what is the point?
- c0112 | justifying resorting to the script because it was everywhere | I only resorted to this because it was being used everywhere
- c0121 | acknowledging and defending the late resort to scripts | Sucks that we had to resort to scripts by the end of it, but I don't feel bad
- c0126 | admitting an outdated script may have fought their own cause | i may have been fighting against the cause for a while but we got it done boys

**Reading A:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair; T3-089 switching off stale scripts (confidence arguable; read whole; families opened G11)
- why T3-028: Members share, recruit for, update and modify an auto-protection script, which is running scripts for the work.
- why T3-027: Members question whether group scripts defeat the point and defend resorting to them, which is arguing whether scripts are fair.
- why T3-089: Members coordinate script versions and admit an outdated script fought their own cause, which is switching off or updating stale scripts that fight the plan.
- added T3-027, own concepts c0110 c0112 c0121; why_not_one: T3-028 would carry running and sharing the auto-protection script but not the argument over whether group scripts are fair or worth using.
- added T3-089, own concepts c0126 c0107; why_not_one: T3-028 would not carry the stale-script conflict, and T3-027 would not carry the version fix; T3-089 is the only one for the admission that an outdated script fought the room's own cause.

**Reading B:** T3-028 running scripts for the work; T3-027 arguing whether scripts are fair (confidence clear; read whole; families opened G11)
- why T3-028: Members share, recruit for, update and run an auto-protection script for the logo.
- why T3-027: They also argue the fairness and point of group scripts, including defending resorting to them.
- added T3-027, own concepts c0110 c0112 c0121; why_not_one: T3-028 carries the sharing and running of scripts but not the explicit argument over whether group scripts defeat the point or are fair.

**B1 grouping (mine, at B1):** T3-027 arguing whether scripts are fair; T3-028 running scripts for the work; T3-089 switching off stale scripts

### 444. texastech/t05, class 3

**getting organized with scripts and a sticky** | note: These passages try to turn scattered placements into coordinated work by running a script, sharing its instructions, offering another script, or asking moderators for a goals-and-operations sticky. The organizing tools vary between code and a subreddit post.

- c0021 | saying help is the only option while running a building script | Ya, the only option would be for them to help. I've currently got a script going building at the top left.
- c0024 | asking mods for a sticky to get organized | I just asked the mods to make a sticky post for goals/general ops for /r/place. Gotta get organized.
- c0026 | sharing RRS's Double T coordinates and script instructions | The folks at RRS have started one at 16,930 It isn't large, but it gets the job done. [Script](http://docdro.id/st8jDmw) To run the script open up r/place, press F12, click on console, paste the script from the link, and press enter
- c0028 | offering a script for putting TTU on r/place | Script for putting TTU on /r/place

**Reading A:** T3-028 running scripts for the work; T3-015 routing canvas posts into megathreads (confidence arguable; read whole; families opened G11,G02)
- why T3-028: C1205926 runs a building script, C0564704 shares the RRS script instructions, and C0302547 offers a script, so scripts place the room work, which is T3-028 rather than coordinates for hand placing (T3-070).
- why T3-015: C0885503 asks the mods for a sticky goals and ops post, gathering the talk into one thread, which is T3-015 rather than a removal by rule (T3-063).
- added T3-015, own concepts c0024; why_not_one: T3-028 covers coordinating through a script but not gathering the talk into one stickied thread.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: Members run, share and offer building scripts for the Double T, including console instructions and script coordinates.

**B1 grouping (mine, at B1):** T3-015 routing canvas posts into megathreads; T3-028 running scripts for the work

### 445. uiowa/t04, class 3

**running and updating a script together** | note: These passages turn the I into coordinated script use: sharing it, asking how, teaching setup, revising it, preventing interference, and stopping a harmful unattended copy.

- c0011 | sharing a Chrome script to draw a larger I quickly | Here is a script that can be run in chrome to draw a slightly larger **I** in the same position. If we get a few people to run it we should be able to take the space pretty quickly
- c0013 | updating the script to match the latest logo | Script now matches the most up to date version of our logo
- c0014 | asking how to run the script | How do I do this?
- c0016 | showing how to run the script and watch it fill the places | Right click anywhere on the screen or press F12. Navigate to the 'Console' tab, paste this code, press enter. Sit back and watch it fill in the places for us.
- c0017 | explaining how to watch the running script | Now the script will run, but you cant refresh the page or see the progress. If you go to the page in a new tab you can see the progress
- c0026 | telling everyone to update scripts so they do not interfere | The script has been updated, make sure to use the new one or it'll interfere with everybody else
- c0032 | telling a sleeping script user to stop hurting the I | turn your script off you are killing us in your sleep!
- c0033 | acknowledging the script mistake | Oops

**Reading A:** T3-028 running scripts for the work; T3-089 switching off stale scripts (confidence clear; read whole; families opened G11)
- why T3-028: C1120927, C1151058, C1522672 and C0485419 share, revise and run a Chrome script for the I, which is T3-028's gate.
- why T3-089: C1489434 and C1262316 find the room's own script overwriting the I and tell users to update or switch it off, T3-089 rather than plain running of a script for the plan.
- added T3-089, own concepts c0026 c0032; why_not_one: Placing on T3-028 alone carries the making and sharing of the script but not the turns where the room's own script is found fighting the I and must be updated or switched off.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: The concepts are all about sharing, running, teaching, updating, and stopping the room's drawing script for the I, which is script use for the work.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-070 sharing coordinates, templates and how-to; T3-089 switching off stale scripts

### 446. uoft/t13, class 3

**automating placement through scripts and extra accounts** | note: These codes share the practice of reducing repeated clicking through a generated image, a Python bot, a Pi, alternate accounts, and continuous multi-account maintenance; what varies is supplying the plan, machine, account, or target image.

- c0096 | creating an image for a pixel-placing script | I'm currently creating an image that we can load on a script to place the pixels for us. I'll share it when I'm done
- c0122 | offering to write an automatic place bot for the logo or an insult to Waterloo | Writing a auto place bot in python, able to put our logo in or we can just write éfuck waterloo
- c0123 | offering a Pi and alternate account to run the placement script all night | All I have to do is load the image of the banners and the food truck right? I can run this all night on my Pi and my alternate account.
- c0124 | planning a multi-account script to create and maintain a picture continuously | I was gonna make a script that uses multiple accounts to create and maintain a picture, I am currently looking for a way to detect the color of each pixel to make maintence faster, this way all you need is a list of accounts and a list of coords with their color, and we can leave it on 24/7

**Reading A:** T3-028 running scripts for the work; T3-088 placing beyond the pixel limit (confidence arguable; read whole; families opened G11)
- why T3-028: The item automates placement through generated images and Python bots, fitting T3-028 as the primary script-running work.
- why T3-088: The item also uses alternate and multiple accounts to place and maintain the picture beyond the limit, fitting T3-088 as a distinct additional theme.
- added T3-088, own concepts c0123 c0124; why_not_one: T3-028 alone would carry scripted placement but not the use of alternate or multiple accounts to place beyond the limit.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: All concepts are scripts or bots made and run for the room's work: an image to load on a script, a Python auto-place bot, a Pi and alt account to run the placement all night, and a multi-account script to create and maintain a picture.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-088 placing beyond the pixel limit

### 447. utaustin/t02, class 3

**using overlays and scripts to build and defend** | note: These passages turn shared designs into repeatable work by posting overlays or scripts, naming colors, correcting coordinates, leaving automation running, and asking it to keep checking the mark. The practice ranges from visual guidance through troubleshooting to round-the-clock defense.

- c0003 | making a shitty overlay to show where the boxes should be | Here's a shitty overlay to get an idea of where the boxes should be
- c0021 | posting a new overlay and position | link to overlay and position
- c0030 | announcing an overlay for r/place after the post body was deleted | I made an overlay for us to make on r/place
- c0067 | writing a JavaScript helper while asking for accessible color directions | I'm trying to write a script in Javascript
- c0068 | answering with the color name and palette position | Dark Orange, 8 over from the left
- c0069 | making a script for faster and more coordinated logo finishing | I made a script to help us finish the logo faster and more coordinated.
- c0070 | correcting the script coordinates before people run it | the correct coordinates are (16,857) just make sure to change them before you run the script
- c0102 | making a script to finish the logo faster and more coordinated | I made a script to help us finish our logo faster and more coordinated.
- c0117 | running the defense script around the clock | Running 24/7
- c0118 | warning the script is one pixel too high | the script is a pixel too high
- c0123 | asking how to keep the script checking and fixing | how does the script work? I assume I need to keep the window open for it to be checking/fixing?
- c0137 | warning every script runner that the coordinates are one too high | Everyone running the script for r/place coordinates are one too high.
- c0147 | warning of GiantBomb pushback and asking everyone to defend overnight | Keep checking on it to make sure they don't take the space back overnight. Well done!
- c0155 | sharing the overlay plugin through OpenUserJS | https://openuserjs.org/scripts/phiresky/reddit.comrplace_template
- c0156 | sharing the coordination script through DocDroid | http://docdro.id/npScWNG
- c0157 | sharing a super-small design through Imgur | [Here](https://i.imgur.com/hectmWf.png) is a super small image
- c0159 | waiting until UT is secured before helping out | I'll help out when it looks like the UT is secured. It's still under attack so I have to keep letting the script defend it.
- c0160 | letting the script defend UT while it is under attack | I'll help out when it looks like the UT is secured. It's still under attack so I have to keep letting the script defend it.
- c0161 | bringing a script from r/aggies to protect both logos | Here from r/aggies With a script to protect both our logos
- c0162 | announcing another r/place script | Another r/place script!

**Reading A:** T3-028 running scripts for the work; T3-070 sharing coordinates, templates and how-to (confidence arguable; read whole; families opened G11,G05)
- why T3-028: The concepts center on scripts or bots made, shared and run to build and defend the logo.
- why T3-070: It also posts overlays, coordinates and templates for placers to follow by hand.
- added T3-070, own concepts c0003 c0021 c0030; why_not_one: T3-028 covers the scripts and automated defense, but not the posted overlays and template guidance the room uses to place by hand.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11)
- why T3-028: The concepts center on scripts and automation to build and defend the logo, with overlays serving the scripted work.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work; T3-070 sharing coordinates, templates and how-to; T3-108 sharing one bot target

### 448. wallstreetbets/t11, class 3

**running and repairing scripts to defend fuckboy** | note: The common practice is keeping the mascot present through automation: recruiting runners and alternate accounts, explaining configuration and output, reporting participation, and diagnosing failures. The codes vary between deployment, maintenance, and technical repair.

- c0079 | asking people to run the script overnight to chip in | Please run the script at the top of this thread overnight on your account to chip in.
- c0080 | explaining that script output still means pixels were edited | That's fine, it'll spam a bunch of shit and appear to not be doing anything but if you open another browser window you'll see the pixels your account edited.
- c0081 | keeping the script running to fix defaced pixels | It will keep fixing pixels that people deface so it's good to keep it running for as long as possible.
- c0082 | celebrating that the script is working fantastically | This script is working fantastically.
- c0083 | searching pastebin for an already-solved script | I searched pastebin and found it.
- c0084 | asking to modify the drawing script for something else | can i just modify this script
- c0085 | explaining how to define a new picture and its offset | You define your picture in that array and then define where it is with the offset variable.
- c0086 | recommending a five-pixel shift to avoid a botfight | Ideally shift yours down like 5 pixels to avoid a botfight between ours and yours?
- c0087 | saying they are doing their part | im doing my part
- c0089 | warning that the script times out multiple accounts | reddit will time you out and won't allow you to connect after you run this script for a while
- c0096 | calling all hands to run the latest script and protect fuckboy's borders | Fuckboy is looking good, but he'll be overwhelmed if you don't help. We need everyone running the latest version of the script at all times. All hands on deck. God knows what could happen if we don't protect our borders.
- c0097 | telling everyone to paste the code into the console | Paste the code at this URL into the console and hit enter.
- c0098 | leaving the script running to keep our pixels safe | Leave this running as long as possible, just leave the window open. You'll be helping to keep our pixels safe.
- c0099 | moving talk to the wallstreetbets Discord | Talk about it in http://discord.gg/wallstreetbets
- c0100 | running multiple instances on shitposting alt accounts | You can run multiple instances on all your shitposting alt accounts as well! Just run them in incognito mode.
- c0101 | promising rewards for those who help the most | Everyone can see who placed a tile. There will be rewards for those that help the most
- c0102 | reporting I'm running it | I'm running it big boi
- c0103 | praising one runner while urging everyone to switch over | Nice. We need everyone to switch over. They're fighting eachother right now.
- c0106 | telling them to spin up copies because people are fucking with fuckboy | Spin up a few copies of the new version because people are trying to fuck with fuckboy.
- c0107 | asking whether other big communities are automating too | are the other big communities automating like this too?
- c0108 | saying we are careless enough to be open about automating | Probably, we're just careless enough to be open about it I guess.
- c0109 | running three accounts to build wallstreetbets and keep out invaders | I have 3 accounts running on different browsers. We will build the wall^streetbets and keep out the invaders.
- c0110 | saying of course we are botting | Of course we are botting.
- c0111 | calling it high frequency fuckboy | High frequency fuckboy.
- c0112 | reporting the new script does not seem to work | just put in the new one, doesn't seem to be working.
- c0113 | asking javascript people to wrap the iteration logic | Do we have any javascript people that can wrap this iteration logic
- c0114 | noticing a failed pixel request stops the script | Just fyi... I notice that sometimes the pixel request fails and the entire script stops.
- c0115 | saying the new top version fixes it while the proposed fix spams errors | I basically fixed that in a more retarded way in the new version at the top, mine seems to work for me whereas yours will spam an error for a while and then Reddit will stop responding.
- c0124 | running all fifteen fake accounts on the bot | currently running all 15 of my fake reddit accounts on that bot.
- c0151 | recounting a skeleton crew getting an HD Fuckboy and asking for protection while weekday strength is decided | Over the weekend our skeleton crew got a rather HD Fuckboy on the /r/place map. You can help us protect Fuckboy while we figure out what to use our full weekday retard strength for.
- c0153 | calling everyone with an F12 key to run the Fuckboy defense script | If you have an F12 key we need you: Run our script to defend Fuckboy on /r/place while we figure out what to use our full weekday strength for.
- c0154 | telling everyone to update to the newest version | This is the newest version, everyone needs to update
- c0155 | selling one-browser-window defense as maintaining WSB's dominance in a pissing contest | with one browser window and almost no effort you can help maintain WSB's dominance in a pissing contest where someone is trying to destroy our mascot
- c0156 | leaving the script running to keep fixing pixels and keep Fuckboy pristine | Leave this running as long as possible so you will stay fixing pixels to keep Fuckboy pristine.
- c0157 | moving r/place talk to the Wallstreetbets Discord | Talk about it in http://discord.gg/wallstreetbets
- c0158 | running multiple script instances on shitposting alt accounts in incognito mode | You can run multiple instances on all your shitposting alt accounts as well! Just run them in incognito mode.
- c0159 | promising visible credit and rewards to the biggest helpers | Everyone can see who placed a tile. There will be rewards for those that help the most
- c0164 | welcoming a chance to use a botnet for the script | FUCKKK YESSSS finally something I can use my botnet for
- c0165 | urging that the code be kept in Discord so outsiders cannot change it to attack place automatically | You should post the code in the discord not here, people are gonna easily find it and change it to fuck with the place automatically lol
- c0171 | calling the defense important and telling everybody to addy up | This is important. This means something. Everybody addy up.
- c0172 | naming the scripted effort weaponized autism | weaponized autism
- c0173 | asking how many autists are fighting | do we know how many autists we have fighting this fight?
- c0174 | declaring that he is doing his part | I'm doing my part
- c0176 | checking whether other scripts started throwing errors | has anyone else's started throwing errors?
- c0181 | asking how and where to run the dollar-sign script | Where do i put the script? or how do i do this?
- c0182 | explaining how to run the script with node.js or the browser console | It's javascript, run it with node.js or copy and paste it into your browser's console.
- c0183 | walking a newcomer through leaving the script running and going back to losing money | Open /r/place * Press f12 and go to console * Paste the script and press enter * Leave it running. Go back to losing money
- c0184 | calling the dollar sign unofficial while approving it and prioritizing Fuckboy scripts | This isn't an official WSB initiative, though I thoroughly approve of fucking with commies. If you're currently running scripts to help fuckboy keep those running.
- c0195 | blaming the script shitting the bed while he showered | The script decided to shit the bed while I was showering, my bad
- c0200 | answering that it was a bot net fuckfest | Because it was just a bot net fuckfest?
- c0202 | saying the bot dude flaked and Esperanto got lucky | Bot dude flaked. You lucky. Esperanto is a pretty fucking gay thing to be putting down too, I personally hated that movie.
- c0206 | saying nobody flaked and later plans became a bad idea | Nobody flaked, we had some shit planned for later but for obvious reasons that wasn't a good idea.
- c0207 | clarifying that a guy helping on the side flaked | No, I mean I had a guy who was going to hook me up on the side who flaked.

**Reading A:** T3-028 running scripts for the work; T3-088 placing beyond the pixel limit (confidence clear; read whole; families opened G11)
- why T3-028: The item is mostly deploying, configuring, repairing, and running scripts/bots to defend Fuckboy.
- why T3-088: Several concepts deploy multiple instances on alts, fake accounts, or botnets, placing beyond the one-pixel limit.
- added T3-088, own concepts c0100 c0124 c0109 c0158; why_not_one: T3-028 alone would not carry the extra-account and botnet multiplication of placements.

**Reading B:** T3-028 running scripts for the work (confidence clear; read whole; families opened G11,G09,G03; flagged a bag)
- why T3-028: The item's dominant doing is running and repairing the room's scripts to defend Fuckboy: it recruits script runners, explains configuration/output, reports deployment, and diagnoses failures.
- also_present: T3-088 c0100 c0109 c0124 c0158 c0164; T3-027 c0107 c0108 c0110 c0111 c0155; T3-005 c0096 c0106 c0109 c0151 c0153 c0156 c0171; T3-014 c0099 c0157 c0165

**B1 grouping (mine, at B1):** T3-028 running scripts for the work

### 449. unitedkingdom/t04, class 3

**Routing work through coordinates, scripts, templates, and side venues** | note: Participants make pixel work actionable by locating it, distributing tools and designs, troubleshooting versions, and moving coordination to dedicated posts or venues. The infrastructure varies from coordinates to scripts, Discord, and specialist subreddits.

- c0005 | sharing a script that does the flag on the left | Here's a script that does the flag on the left
- c0013 | saying three flags are obstructing one another | There are three separate flags being made at once, and we're just acting as obstacles in one anothers' ways.
- c0015 | making a Discord to fix the flag with good communication | I made a discord so we can try and fix this shit with good communication
- c0016 | saying the shit show needs someone in charge | This is a shit show. We need someone in charge.
- c0025 | giving a start point and design for the flag | Starting here: https://www.reddit.com/r/place/#x=740&y=125 This design: https://s-media-cache-ak0.pinimg.com/736x/b4/4b/e5/b44be547820931acaa5d7058ed5b431d.jpg
- c0026 | redirecting flag makers to a more promising spot | More luck here: https://www.reddit.com/r/place#x=165&y=334
- c0057 | giving the flag location | Flag Location : https://www.reddit.com/place?webview=true#x=160&y=342
- c0129 | reporting that the attempted fix does nothing | I did that but it does nothing?
- c0130 | telling them to refresh and use an updated version with feedback | Refresh, then go it again with this updated version: https://pastebin.com/raw/1VVpYagp It gives a bit more feedback so you can see what's happening.
- c0161 | lowering hopes because of the main union jack's organisation | See the organisation of the main union jack I wouldn't get my hopes up.
- c0162 | asking where the moving Union Jack is coordinated | Where's that being coordinated from?
- c0166 | running a script to build the right-hand union jack | The union jack on the right is being built by a script a few of us are running.
- c0167 | directing people to continue the scripted right-hand flag | people are running scripts to automatically do the right one so it's best to continue with the right one.
- c0180 | admitting the mistake and updating the script | I fucked up. Updated the script now
- c0205 | giving grid reference 164,327 | Grid reference 164,327
- c0240 | creating r/placeuk for place-related things | I am not sure how long place is here to stay for, but I have created /r/placeuk, so feel free to use it for related things
- c0244 | asking where UK place things are being posted now | Where are UK place related things being posted now?
- c0252 | making a subreddit to coordinate the Flag and the Queen on r/place | I have made a subreddit for coordinating all things British on r/place (the Flag, the Queen etc.)
- c0256 | keeping the latest template updating automatically | This script will always get the latest template automatically every 60 seconds from the server via github so once it runs that should be all you need to do forever!
- c0257 | urging scripts so the country is not embarrassed | You don't have to do this, but we urge you to so that we don't embarrass our country.

**Reading A:** T3-028 running scripts for the work; T3-070 sharing coordinates, templates and how-to; T3-090 opening a canvas sub (confidence arguable; read whole; families opened G03,G05,G11)
- why T3-028: Scripts are shared, run, troubleshot and updated for the flag work, which is T3-028.
- why T3-070: Coordinates, start points and grid references are distributed for placers, which is T3-070.
- why T3-090: A dedicated r/placeuk sub and coordinating subreddit are created, which is T3-090.
- added T3-070, own concepts c0025 c0057 c0205; why_not_one: T3-028 covers the scripts and bots but not the hand-followable coordinates, start points and templates given to placers.
- added T3-090, own concepts c0240 c0252 c0244; why_not_one: T3-028 covers running scripts but not the move of coordination into a dedicated subreddit.

**Reading B:** T3-070 sharing coordinates, templates and how-to (confidence arguable; read whole; families opened G05,G11,G03; flagged a bag)
- why T3-070: Coordinates, start points, locations and grid references lead; the item also carries scripts (T3-028), Discord (T3-014), and a canvas sub (T3-090).
- also_present: T3-028 c0005 c0166 c0167 c0180 c0256 c0257

**B1 grouping (mine, at B1):** T3-070 sharing coordinates, templates and how-to

### 450. wildhockey/t02, class 3

**coordinating pixels with coordinates, roles, and scripts** | note: These passages make distributed pixel work doable by sharing bearings, dividing outline and fill, refreshing, scripting, troubleshooting, and correcting errors; the means vary while the common practice is coordinating the build.

- c0005 | proposing coordination during the game thread | We'd need to get coordinated. Maybe during the game thread today we can organize it
- c0006 | backing game-thread coordination | Ooo, good idea.
- c0013 | correcting coordinates after losing ten minutes | edit: lol apparently I was 10 off. There goes 10 minutes of my time. Link fixed
- c0014 | sharing a screenshot to get builders' bearings | For purposes here, because it's such a mess, here's a screenshot just to get your bearings
- c0025 | calling the build hard to coordinate | This is pretty hard to coordinate haha.
- c0026 | dividing work into outline first and fill afterwards | I'm working on the outline first, we can fill it afterwards.
- c0027 | warning builders to refresh against people and scripts taking pixels back | Don't forget to refresh.. some people keep changing it to purple then back to the green lattice.. pretty sure scripts are taking the lattice back.
- c0031 | defending the green while others make the outline | Yeah, I'm working on keeping it green. You guys keep making the outline.
- c0072 | setting up a discord server for the logo | A discord server has been set up by /u/roflcopter34: https://discord.gg/872D8mP
- c0073 | rewriting the Vikings' script and updating it for the NYU agreement | I have made a script that will do the work for you. (By making a script I actually mean shamelessly taking code from /r/minnesotavikings and rewriting it. Credit to /u/pvt13krebs). We've agreed with NYU to give them those bottom few pixels, so I updated the script.
- c0074 | instructing members to leave the pixel script running and refresh it | Open https://www.reddit.com/place?webview=true 2. Press F12 3. Click the tab that says "console" 4. Look for the ">" 5. Place your cursor after it 6. Paste this entire thing: https://pastebin.com/ZGCeYTzF (updated 4/3 9:30 AM) 7. Press Enter 8. Leave tab open, you can minimize. 9. Refresh the page and do steps 6-7 again every once in a while.
- c0095 | asking for a coordinate template while starting the three right-side greens | Template with coordinates would make it a lot easier. But anyway I've started with the three greens at right and this is the location of the uppermost https://www.reddit.com/place/#x=998&y=485
- c0096 | calling for a script because coordinating without one seems impossible | Can anyone write a script? I feel like this is going to be near impossible to coordinate without one
- c0099 | creating a script to help build the logo | Created a script to help with this.
- c0100 | guiding pixel placement with the overlay | You can use this to guide you as you place pixels
- c0101 | troubleshooting and then getting the overlay working | No overlay is popping up when I hit the T Edit: nevermind I got it
- c0102 | asking what the move is | What's the move?
- c0110 | suggesting Discord to get more organized | Should we get a discord set up to be more organized?
- c0111 | offering to link a Discord someone else sets up | If you set one up I'll link it in the post. I'm not great with discord.
- c0112 | providing the new Discord invite | Here you go: https://discord.gg/872D8mP
- c0116 | reporting friendly fire in the mouth region | We got some friendly fire goin' on in the mouth region...
- c0117 | blaming the script for an incorrect friendly-fire pixel | must be the script. I just looked and I placed an incorrect pixel using it.
- c0120 | reporting the script puts in wrong colors | The script is putting in wrong colors n shit
- c0121 | telling members to refresh for the corrected code | The correct code is there if you refresh the thread.
- c0123 | reporting AngryYeoBot putting blue squares in the nose | /u/AngryYeoBot is putting blue squares in the nose =(
- c0136 | asking for coordinates in order to help | What are the coordinates? I could help.
- c0137 | giving the r/place coordinates | https://www.reddit.com/r/place/#x=957&y=493
- c0151 | running the defense script on eight accounts | I have my script running on 8 different accounts (AngryYeoBot Included!) so It should be defended pretty well!
- c0153 | flagging AngryYeoBot's blue pixels for repair | Good. Btw I noticed AngryYeoBot was occasionally placing some blue pixels over the logo, so you should fix it if you can.
- c0154 | fixing the script's swapped colors with a changed reference image | Yepp! I fixed it last night before I went to bed. The script I'm using had the colors messed up, placing blue for red and cyan for yellow, so I had to change my reference image to http://i.imgur.com/BMAaoI5.png to fix that. Looks kind neat lol
- c0155 | reporting that the repaired script still misplaces pixels | Good. It still seems to be misplacing a couple pixels though.
- c0159 | reporting the bots' blue pixels returning | The blue pixels just started coming back from those bots again.
- c0160 | asking how to put more named bots into the fray | Running the script within some form of python script (akabots) or an many browsers on multiple computers? I could put my Torchetti and Bruce bots into the fray if you know a way to play without a browser...

**Reading A:** T3-070 sharing coordinates, templates and how-to (confidence arguable; read whole; families opened G05,G11,G03)
- why T3-070: The item is chiefly about circulating coordinates, templates, overlays and roles so placers can reproduce the logo, matching T3-070 rather than the script-running gate.

**Reading B:** T3-028 running scripts for the work; T3-070 sharing coordinates, templates and how-to; T3-014 moving planning into a chat (confidence arguable; read whole; families opened G11,G05,G03)
- why T3-028: Scripts and bots are written, shared, run, troubleshooted, and used to place/keep the logo, so T3-028 leads.
- why T3-070: Coordinates, templates, overlays, and hand-placement guides are also central, which T3-028 does not carry.
- why T3-014: Discord setup and invites are present as a distinct planning venue, which neither script-running nor template-sharing covers.
- added T3-070, own concepts c0095 c0137 c0100; why_not_one: T3-028 misses the coordinates, templates, and overlay guidance used for hand placement.
- added T3-014, own concepts c0072 c0110 c0112; why_not_one: T3-028 misses moving planning into a Discord chat and sharing invites.

**B1 grouping (mine, at B1):** T3-028 running scripts for the work


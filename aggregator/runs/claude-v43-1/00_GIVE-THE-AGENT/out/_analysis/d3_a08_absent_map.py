#!/usr/bin/env python3
"""D3a-35: write A08's absent map (A08-absent-map.json) from one table, so each reject carries the marking and the
record it rests on, with their quotes and hours as d3_absent_cites_A08_1..4.txt printed them. Each row:
id | marking code | marking quote | hour | record code | record quote | hour | note (may be empty).

  python3 out/_analysis/d3_a08_absent_map.py
"""
import json

ROWS = """
4chan-063|c0099|I'm so proud of our community here|37.71|c0276|a tiny rectangle that was defaced by the end|73.69|
AMD-051|c0132|We did it!|24.71|c0418|the single red pixel immortalises the struggle|73.99|, a fond reading of the flaw (G13a)
AprilKnights-051|c0053|My fellow knights, Mission Accomplished!|31.27|c0075|Screenshot of our logo and The Button in mint condition|63.07|
CSUFoCo-045|c0001|Managed to create a small CSU logo on the far right side of r/place|57.46|c0008|LSU took our spot.|72.36|
ChronoTrigger-038|c0080|We did it everyone!|73.16|c0087|I happened to record the moment of placing the very first pixels|75.37|
Clannad-032|c0001|The Dango in /r/Place is finished|58.26|c0004|This is the final version of the dango|58.39|
DCFU-038|c0001|DCFU representing in /r/place!|60.96|c0009|Here is a timestamped image|66.68|
Dominican-047|c0032|Small but proud|54.31|c0063|La bandera fue borrada por Holanda.|71.86|
Dorset-038|c0014|SWEET!|68.53|c0017|At the end of r/place we were missing 3 pixels.|73.43|
ElSalvador-047|c0009|Shoutout to r/placehearts for creating this awesome canvas for us to show our pride!|64.74|c0013|it looks like our flag survived to the end.|74.73|
ElderScrolls-047|c0014|Nice job with the Vivec, guys!|49.35|c0023|Someone should take a screenshot of the finished product|59.81|
Fez-057|c0028|We did it!|43.86|c0085|apologize for indirectly causing|73.17|, an apology for the work's absence from the final canvas
GuardiansOfDatBoi-047|c0045|Thank you all for the wonderful experience|75.92|c0046|Dat Boi lives on forever now, immortalized in pixels!|76.54|
Honduras-045|c0002|Hice este hilo para agradecer a quienes aportaron a hacerla|20.12|c0014|at least our heart survived.|73.53|
KState-051|c0042|Great job everyone!|56.87|c0048|It didn't survive the shutdown.|73.34|
ManningPlace-049|c0049|Good work everyone, it was a pleasure!|73.14|c0052|Here is a final version with Manning Face complete.|78.22|
Moondye7-046|c0013|we did it PogChamp|32.50|c0017|Timelapse of the glorious MD7 Sign in r/place|50.49|
SquareSpiral-064|c0193|amazing job on restoring our sacred spiral guys!|69.87|c0207|Like a beacon in the night, Spiral spirals on.|75.04|
Summit1G-051|c0032|We made it...|28.10|c0064|/r/place is over and the 1G is flawless.|77.93|
TheB1G-038|c0008|Great we've done it. Nice job everyone!|54.64|c0044|The final state of the B1G on /r/place with random pixels cleaned up|73.73|
TreePlace-049|c0013|All hail the glorious tree.|8.43|c0035|I was glad to see it while it lasted.|78.75|
Villanova-046|c0014|It has been completed! Villanova now has a place in r/place|58.91|c0015|Pictures|60.77|, more pictures given in reply
afip-045|c0055|Back to Back Void War Champs|70.77|c0056|Attack and Defense of the American flag last night|70.80|
ainbowroad-055|c2022|It's been a blast.|74.84|c2027|I created a sub to provide original and edited print quality versions of the art.|76.82|
anarcho_capitalism-058|c0053|Flag Completed By Me and others like /u/AXSwift - Thanks!|36.65|c0179|Defense of Ancapistan Timelapse|81.72|
apocalypserising-038|c0008|you guys all got the AR logo on /r/place|30.80|c0050|For everyone who can't find it|92.76|
asexuality-047|c0049|And for a brief moment, all was right in the world|34.44|c0051|This is a rare screenshot of the banner with only one pixel wrong.|44.38|
asktransgender-047|c0023|I'm so proud of us.|11.79|c0162|View what ye have wrought, in all its glory.|81.98|
australia-060|c0112|Good on ya, everyone!|14.12|c0224|Timelapse building the Aussie Kangaroo|34.78|
baylor-043|c0006|i got the BU logo on r/place!|63.07|c0015|we were still on there though|73.41|
bdsm-041|c0004|Huzzah|43.04|c0005|Shame it's fallen to the Spanish onslaught.|51.61|
bih-044|c0001|BiH na r/place|42.03|c0025|obrisaše nas pola|73.79|
bindingofisaac-051|c0038|We did it reddit!|10.76|c0204|Timelapse video of Isaac on /r/place|48.87|
bostonceltics-055|c0125|has successfully made its mark on /r/place! Go Celtics!|70.84|c0134|r/place ended with some blemishes on our logo.|74.04|
bretagne-040|c0012|r/Bretagne sur r/place!|45.99|c0042|on le reconnait quand même un peu.|73.61|
calgaryflames-061|c0237|I am really proud of everyone here!|53.44|c0285|Did someone get a screen cap of it by any chance?|73.43|
canada-049|c0324|Woke up to a perfect Canadian flag.|43.34|c0339|Would you mind posting this in /r/placemuseum as well|47.54|
cavestory-048|c0016|Incredible Job, Guys!|29.80|c0039|Cleaned up the beatiful painting done on /r/place|42.40|
cfb-045|c0496|The football is back to perfection! WE DID IT, GUYS!|72.43|c0515|r/CFB @ r/place archive|73.21|
chibears-050|c0115|Its rad.|71.25|c0167|Here's an image of r/place with the Bears logo still intact.|78.33|
cirkeltrek-046|c0288|WIJ DEDEN HET|73.45|c0293|timelapse met discord die het Wilhelmus zingt|75.50|
cloud9-040|c0039|We did it!|50.87|c0081|I tried to add the top swirl, but to no avail|73.43|
compsoc-040|c0001|CompSoc in /r/place (815,538)|24.88|c0008|we got wiped out by the void|66.81|
costa_rica-038|c0047|Terminamos el corazon!|56.36|c0073|NOS BORRARON AL PURO FINAL|81.91|
crusaderkings-048|c0168|Congratulations to everyone involved|73.42|c0172|The latter has our crown in full glory!|73.65|
cubers-071|c0296|it was fun and we made our mark!|73.10|c0304|Here is a fixed version of what we made over in r/Place.|73.64|
darksouls-039|c0051|WE DID IT REDDIT|24.50|c0159|All that time I spent making the stupid windows border|73.28|
day9-049|c0031|The new location is finished!|53.09|c0036|We successfully built|74.07|, a retelling
detroitredwings-062|c0112|We did it! Now we maintain.|42.97|c0141|Too bad it was consumed|79.06|
diablo-038|c0042|GGs guys we drew 2 really good D's.|71.00|c0050|We missed our chance. they seem to have closed it.|73.17|
donaldglover-047|c0092|WE DID IT REDDIT|55.03|c0106|RIP BLOND|95.85|
dota2-056|c1153|Shoutout to whoever made the Dota 2 logo on r/place!|73.35|c1155|DotA logo timelapse full 72h|79.36|
drugs-051|c0142|Respek|49.09|c0193|got painted over by the Major League Soccer logo overnight on /r/place.|72.80|
drumcorps-050|c0125|We did it!|71.01|c0134|/r/place has ended, and we survived.|73.32|
dwarffortress-052|c0155|WE DID IT|71.92|c0157|Two wars|76.88|, a retelling
enterthegungeon-047|c0030|Glad we've made a mark on the canvas.|45.78|c0087|Here he is right after we finished him|75.53|
ethereum-053|c0121|Ethereum's humble position besides Bob Ross is wholesome.|58.30|c0140|It is now Ethercum lol|76.10|
ethoslab-041|c0021|We made it onto /r/Place along with Docm77 and Guude, guys!|29.78|c0039|Etho has been destroyed by the Netherlands|53.22|
evex-039|c0034|Success! We did it, Evexians!|35.40|c0093|r/E∀E}|76.29|, a joking rendering of the changed logo (G13a)
factorio-047|c0202|Huge shout out to everyone who helped maintain our belts and both of our logos.|73.71|c0208|Cue Admin post saying /r/place has ended!|74.40|, a retelling of a last repair cut off
finland-043|c0054|working to keep each other clean is a beautiful thing|57.05|c0081|it's there on the final product!|73.59|
floridagators-049|c0059|and everyone else who helped wade through that muddled mess|40.07|c0133|I doubt any of my pixels actually made it in the final image|86.66|
frc-061|c0081|We finally finished!|51.27|c0138|FRC's Finest Moment on /r/Place|82.51|
ftlgame-057|c0010|The Engi is complete!|29.79|c0066|I'm so sad it disappeared before the final canvas|74.84|
giivasunner-038|c0121|we merged 3 subreddits and helped each other at the r/place.|43.89|c0213|a version of the timelapse that focuses on fred flintstone|76.16|
hearthstone-060|c0269|We've still created something together|29.40|c0333|Hearthstone on place, final|90.89|
heroesofthestorm-040|c0050|WOOHOO! THE FULL|30.29|c0223|/r/place Heroes of the Storm Timelapse!|42.89|
homestuck-039|c0153|Logo, Numbers, Subreddit, and Rage. Nice Work, Gents.|38.79|c0209|Dave /r/place timelapse video.|52.57|
hongkong-044|c0048|We did it, HK! Our flag is established on /r/place!|49.79|c0046|Now the place is ended and our flag is still perfect|73.27|
iastate-050|c0053|When ISU gets on r/place|57.63|c0060|had to move because DOTA2 overtook us.|93.67|
iceland-047|c0072|TIL HAMINGJU ALLIR SAMAN|73.19|c0074|Eftir langa baráttu að breyta Islam aftur yfir í Ísland|73.49|
ireland-058|c0369|thanks to everyone for helping us make our mark on a small piece of reddit history|73.07|c0382|Anyone have a pic of the full screen?|73.24|
latvia-051|c0036|A huge thank you to everyone who helped in building these flags|45.50|c0061|Austria completely covered the Latvian flag|74.81|
lego-057|c0185|We did it brick fans!|61.92|c0216|Lego logo timelapse full 72h|93.39|
linux-059|c0040|Finished product looks great, nice work /r/linux.|24.49|c0106|http://spacescience.tech/place/|52.91|, a timelapse link
lithuania-045|c0106|Thanks everyone|56.63|c0107|It was an epic 4 hour long battle for 60 pixels.|56.65|
luciomains-045|c0030|It's done!|46.27|c0094|The final product of lucio on r/place|75.44|
mcgill-050|c0072|We did it Reddit!|73.30|c0074|every pixel of this canvas was fought over|79.73|
megaman-055|c0006|Mission successful, Guys!|11.74|c0072|oh god dammit (r/place)|87.31|, dismay at the finished image
mexico-038|c0057|we did it !!!! con todo y cactus|7.79|c0321|putos ya lo quitaron|73.27|
mindcrack-048|c0115|I'm proud of how much are community pulled together|73.21|c0119|Final result for r/mindcrack at r/place!|73.61|
monero-048|c0119|Congratulations everyone!|73.34|c0126|it does not have even 1 dirty foreign pixel.|78.86|
nascar-044|c0134|Helped leave our mark in /r/place|36.97|c0187|You can see r/NASCAR's logo shown in 3D by stacking changes|67.07|
norge-047|c0240|Bra jobba, /r/Norge|73.36|c0276|Stolt av dere /r/Norge og /r/Sweden!|87.99|, posted with a full timelapse
notredame-038|c0097|r/Place is over and ND won! Great Work everyone.|75.98|c0100|That dang o red dot is going to haunt my dreams.|78.75|
nuclearthrone-045|c0044|Fish now rolls at the top of /r/place|37.54|c0055|Fish has been absorbed|48.01|
ockytop-039|c0037|we pulled it off.|35.73|c0084|bots can't take away the fun we had or the screen caps we have.|78.26|
overwatch-078|c0371|We did it reddit!|22.07|c1178|the Overwatch timelapse|81.43|
pepe-048|c0011|OMFG THIS PEPE IS ON R/PLACE!!!|26.17|c0013|they killed him|41.68|
peterdraws-057|c0006|it was totally worth it!|34.35|c0009|The third incarnation, and final resting place of the suprematist homage of|73.66|
pitt-038|c0068|We did it!|50.54|c0081|From a small Pitt logo, to attempts at|54.21|
placeDE-038|c0324|Vielen Dank an alle die mitgeholfen haben!|73.25|c0329|Der letzte Screenshot unseres Kunstwerkes|73.26|
placestart-056|c0016|We did it, Reddit!|39.97|c0301|Can we Timelapse this?|55.68|
polska-051|c0011|Zrobiliśmy to /r/Polska!|7.71|c0078|Tak to sie zaczelo r/place|48.62|
prequelmemes-054|c0132|We did it! (/r/Place)|12.70|c0163|Darth Plagueis timelapse (/r/place)|17.23|
puzzleanddragons-055|c0130|Completed /r/pad territory in /r/place!|54.73|c0174|I've gotten an image of the final product|64.53|
quq-021|c0006|we did it reddit|59.53|c0008|Under nintendo switch, above the space ship|78.82|, the work located on the final canvas
radiohead-048|c0056|We did it!|14.17|c0113|Timelapse of the radiohead thingie on /r/place|27.67|
redhotchilipeppers-056|c0100|We made it onto /r/place!|50.96|c0121|rip logo|56.38|
redpandas-054|c0002|We have done it!|21.80|c0003|/r/place has been closed, this is the final standing of our work.|21.80|, a later edit of the same post, so the post marks the work first and records it after
ripcity-053|c0141|Red border finished! Looking good RIP CITY!|57.20|c0179|at least we have plenty of screen shots of perfection.|73.08|
riskofrain-043|c0005|This was worked on over the risk of rain discord!|44.00|c0021|at least were still|72.03|
runescape-052|c0351|We did it! Thanks to everyone helping!|36.96|c0538|minecraft logged pixel changes|80.77|
shield-038|c0086|Hail Hydra|76.44|c0087|Screenshot in case the link doesn't work.|76.51|
signal-037|c0003|EDIT: We did it!|62.96|c0004|is an image of the final version with /r/signal in it.|62.96|, a later edit of the same post, so the post marks the work first and records it after
slovenia-038|c0063|Hvala vsem!|73.24|c0076|Končna verzija v dokaj visoki resoluciji|75.63|
southafrica-048|c0139|Glad I could take part in making a name for ourselves|75.82|c0169|r/places timelapse|93.83|
soylent-037|c0001|Mission accomplished|19.84|c0047|I caught a screenshot of our spot on r/place at its most perfect!|83.44|
spain-049|c0035|¡Gracias a todos!|42.42|c0095|Imagen final de la bandera en r/place|74.07|
stardustcrusaders-061|c0308|to thank the guys who worked on getting JoJo some recognition on the canvas.|73.53|c0312|Here's the final thing:|75.71|
starlightstage-061|c0110|happy we got Akane up in time|73.12|c0115|Akane is now immortalized at the center|78.44|
starryknights-038|c0005|Proud of our work!|34.69|c0007|The first star at 2:46 + timelapse|36.03|
superman-045|c0023|We did it reddit!|70.58|c0029|I really wanted to get Superman character pixel in but we lost that.|83.46|
survivor-049|c0197|We did it!|54.46|c0320|r/Denmark destroyed our logo|83.06|
switzerland-054|c0058|Place is over. Well done lads!|74.05|c0060|Place has ended and our flag is all nice and clean.|78.21|
tagpro-059|c0019|You did it|6.71|c0175|the evolution of our little place on place|79.22|
tf2-038|c0124|I feel proud for contributing.|26.46|c0324|Timelapse of our imperium on /r/place so far|54.15|
theblackvoid-054|c1814|I am proud of every black pixel on this canvas.|73.51|c1875|we most definitely succeeded in that.|74.75|, the timelapse as the void's record
twice-058|c0104|WE DID IT GUYS|53.36|c0143|Here is the final image|73.90|
ukplace-036|c0016|how incredible proud I am of all of you.|56.35|c0065|Final Image of UK and Britaly|73.30|
ukraine-049|c0036|nice job everyone!|26.87|c0049|The final|74.41|, the final result's image
unitedkingdom-049|c0020|the flag is done! Yay!|34.48|c0235|Development of the Union Jack in r/place|49.32|
uruguay-049|c0032|WE DID IT REDDIT!|30.61|c0061|No llegue a terminar el Corazón antes que se acabara|73.16|
vegan-040|c0284|We did it!|74.73|c0284|a 4k image of the whole thing.|74.73|, one post that marks the work first and then gives its image (reading 9)
wales-046|c0038|we did it! Well done everyone!|73.26|c0039|Final image r/Place|73.56|
wow-061|c0296|We did it!|73.40|c0355|on /r/place timelapse full 72h|94.36|
"""

PART = {
    "aromantic-045": "G6: the line is marked NONPORTABLE ['lost'] and fails portability, a particular",
    "farmcarrots-046": "G6: the line is marked NONPORTABLE ['lost'] and fails portability, a particular",
}

rej = {}
for ln in ROWS.strip().splitlines():
    aid, mc, mq, mh, rc, rq, rh, note = ln.split("|")
    assert aid not in rej, aid
    rej[aid] = (f"G2, G3 and G40, quotes read: {mc} '{mq}' (h+{mh}), then {rc} '{rq}' (h+{rh}){note}; a marking of "
                f"the room's work comes first and a record of what happened to it follows, so A08's order is shown and "
                f"the claim of absence fails")
with open("out/_analysis/d3_rulings/A08-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": {}, "particular": PART}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects and", len(PART), "particulars to out/_analysis/d3_rulings/A08-absent-map.json")

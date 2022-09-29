# URL analizáló alkalmazás készítése
## Miért jó ez?
Mai világunkban az interneten számos módon oszthatnak meg velünk különböző URL-eket akár rossz szándékú emberek is. Mind a közösségi hálókon (facebook, instagram, discord, stb.) vagy hagyományabb módon e-mailban vagy különböző fórumokon, blogokon. Sokszor kapunk kéretlen linkeket amikre rákattintva olyan oldalra kerülhetünk ami az adatainkat szeretné megszerezni egy megbízható oldalnak kiadva, vagy pedig kártékony kódot tölthetnek le és indíthatnak el az eszközeinken. Ezen problémára nyújthat megoldást egy URL analizáló alkalmazás, ami könnyen integerálható különböző chates megoldásokba, vagy akár egy böngésző bővítményként.
## Mi lesz ez?
A hallgató feladata egy olyan rendszer megtervezése és implementálása ami alkalmas arra hogy könnyen integerálható legyen más megoldásokba széles körben, és a fő feladata annak ellenőrzése hogy egy URL nem mutat-e káros tartalomra, illetve további vizsgálatok elvégzésre képes. Ehhez hozzon létre egy backend-et ami ezt ellenőrizi továbbá képes további információkat összegyűjteni és visszaadni az URL-ről, például ha egy aktív weboldalról van szó:
- a domain származási országa
- mióta aktív az oldal
- ismert-e más hasonlóan működő rendszerek által, mint a virustotal vagy az urlhause
- az oldal előnézete
### További követelmények
- Az integerálhatóság bemutatására hozzon létre egy weboldalt ahol könnyen bemutathatóak a megvalósított funkciók.
- A rendszer legyen alkalmas az esetlegesen talált malware-k begyűjtésére és tárolására néhány metadata mellett.
- A rendszer könnyen skálázható legyen, könnyen alkalmazkodjon egy nagyobb terheléshez is.

## Ismert hasonló megoldások
- urlscan.io (ebben a nyílt forráskódban és abban fog különbözni hogy ezen megoldás akár teljes egészében integrálható egy másik rendszerbe, ezzel "házon belül" ellenőrizve a beszélgetéseket mondjuk egy vállati slack esetén)

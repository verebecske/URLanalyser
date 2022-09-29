# URL analizáló alkalmazás készítése
Ez a diplomatémám.

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

# Application to analyse security level of URLs
This is my thesis in the University.

## Why?
In today's world, there are many ways in which URLs can be shared on the internet, even by people with bad intentions. Both on social networking sites (facebook, instagram, discord, etc.) or more traditionally by e-mail or on various forums and blogs. Many times we receive unsolicited links that, when clicked on, can lead us to a site that wants to get our data by pretending to be a trusted site, or they can download and execute malicious code on our devices. A solution to this problem can be provided by a URL parsing application, which can be easily integrated into various chats solutions or even as a browser extension.

## What is this?
The student will be responsible for designing and implementing a system that can be easily integrated with other solutions on a large scale, and the main task is to check that a URL does not point to harmful content and to perform further tests. To do this, create a backend that checks this and is able to collect and return additional information about the URL, for example if it is an active website:
- the country of origin of the domain
- how long the site has been active
- whether it is known by other similar systems such as virustotal or urlhause
- the preview of the page

### Additional requirements
- To demonstrate the integrability, create a website where you can easily demonstrate the implemented functionality.
- The system should be able to collect and store any malware found, along with some metadata.
- The system should be easily scalable, easily adaptable to a larger workload.

## Similar known solutions
- urlscan.io (this will be open source and will differ in that this solution can be fully integrated into another system, thus controlling conversations "in-house" for say a corporate slack)
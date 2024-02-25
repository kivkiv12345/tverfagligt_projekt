

## Indledning

Denne processrapport dækker over udviklingen af mit serveradministrationsværktøj. Det har fra starten været indtænkt at produktet skal implementeres på min server derhjemme, men samtidigt har det også været vigtigt, for mig, at implementationen er nem i flest mulige passende sammenhænge.

Den réele implementation skal som efter planen bruges af en vennegruppe på 5 mennesker, som skal have mulighed for lettere administration af vores spilservere, mens jeg selv er på arbejde eller ligeledes henholdt fra serveradministration.


## Case Beskrivelse

Mange vennegrupper verden rundt bevæger sig mellem spil som tillader at man hoster sine egne servere. Når muligt foretrækker spillere typisk at køre en midlertidig server direkte gennem deres spil, men det nødvendiggør at den spillers computer er tændt og kører spillet.
Den traditionelle løsning er en dedikeret server, som ikke kræver at spillet selv er kørende.

Oftest anses dedikerede servere som dårligt passende for mindre vennegrupper, hvilket i større grad skyldes besværligheder med deres opsætning.
På den anden side har de til fordel at kunne køre uafhængigt af enkelte spillere. Det egner sig godt til vennegrupper som har sjældent kan spille samtidigt.


Med mit projekt vil jeg levere en software-pakke som giver et fælles interface for nem administration af spilservere.
Projektet har stor fokus på at skulle køre og opsættes på fysisk forbruger hardware, såsom gamle computere og Raspberry PIs; hvad end vennegruppernes medlemmer ejer.
Derfor er det også attraktivt at opsætningen kan slukkes for at spare strøm, og at spillerne kan tænde den igen når den skal bruges.
Software-pakken vil som minimum indeholde et administrationsværktøj/backend med et fælles interface til forskellige spilservere, og en mobil-app til administration deraf.


## Problemformulering

Hvordan kan slutbrugere oprette og fjernadministrere spilservere på deres nemt tilgængelige hardware?


## Afgrænsning

Jeg stiftede min kravspecifikation med flere nedprioriterede krav som, blandt andet, har som formål at lægge grundlag for fremtidig udvidelse af produktet af projektets færdiggørelse.
Hermed er tiltænkt alle krav af prioritet 5, hvoraf følgende stadig mangler: push notifikationer, tilstrækkelig håndtering af brugerrettigheder og whitelist/blacklist.

Oprindeligt var det også tiltænkt at logging skulle kunne forgå vha. en tidsbaseret database (sandsynligvis Victoria Metrics), men sådan en væsentlig udvidelse af kompleksitet har jeg ikke vovet mig at introducere i projektet.


## Tidsplan

## Dokumentation af Valg

Produktet præsenteres af en frontend lavet med Flutter (Dart), som forbinder til en backend lavet med Django (Python). Databasen er på nuværende tidspunkt SQLite, men er nemt udskiftelig skulle der blive behov for det.

Projektets Dockerfiler (hermed også docker-compose.yml) har som formål at gøre det nemt at afprøve og implementere produkterne.

### Flutter

Indtil videre har jeg ikke mødt nogen frontend udviklingsværtøjer som jeg synes godt om.
Jeg er stor modstander af XML (eller lignende) til frontend, jeg oplever at det typisk knytter én til Visual Studio og dermed Windows.
Modsat set kan man beholde alt UI som kode, hvor jeg tidlige har brugt TKinter og Kivy (Python).

Sjovt nok er Flutter stort set det stik modsatte af hvad jeg foretrækker inden for programmering:
- Meget af koden forgår med async/await, som kan siges at være ukompatibel men synkron programmering.
- Typisk instantierer man alle sine widgets som 'recursive' argumenter til retur værdigen. Det medfører en masse indlejrede paraneteser, af flere forskellige slags, som er svære at omstrukturere, trods hjælpen fra Visual Studio Code.

Alligevel er jeg åben for at vælge Flutter igen i fremtiden, grundet min store respekt for understøttelsen af mange platforme.


### Django / Python(-on-whales)

Jeg har efterhånden brugt Django til en håndfuld projekter, og har derfor nemmere ved at forudsige kompleksiteterne dertil.
Selv sagt vil jeg også sige at jeg opbrugte min kvote på ukendte teknologier da jeg valgte Flutter som frontend, som viste sig at tage noget tid at lære.

### Database

Django's ORM (Object Relational Mapping) understøtter som udgangspunkt en række relationelle database, hvoraf SQLite roligt kan bruges uden at lave endnu en Docker container. Havde jeg haft større krav til databasen, ville jeg i stedet have valgt PostgreSQL af flere grunde:
- For at kunne installere Django-Polymorphism pakken, som ville tillade mig at gøre min GameServer model abstrakt, men fortsat lave forspørgeler derpå for at få konkrete nedarvede klasser til specifikke spil.
Hermed ville jeg kunne undgå mine 'Manager' klasser (og arvehierarkiet dertil).
Sagt således lyder Django-Polymorphism som et meget fornuftigt valg, men tager man i begtragtning at det ville koste en ekstra SQL JOIN per konkrete spilklasse, samt en ekstra Docker container, har pakken alligevel væsentlige ulemper.
- Jeg har tidligere Dockeriseret en PostgreSQL database til vores H3 Trello lignende projekt, og ved derfor at det nemt kan gøres med nogle enkelte ændringer til Django og docker-compose.yml filen.

### Alternativer

## Realiseret tidsplan


## Koklusion

### Refleksioner

Dog jeg er tilfreds men kravspecifikationens nedprioriterede krav, har jeg følt at de 11 krav jeg har haft er for få, når jeg tillader mig selv __ikke__ at nå alle.

Med andre ord har mine højt prioriterede krav nok været for brede. Det er en situation som jeg vil forsøge at undgå til svendeprøven.


Dette tverefaglige projekt har givet mig meget spekulation vedrørende omfanget til produktet til den kommende svendeprøve. De få obligatoriske krav jeg har stilt mig selv på kravspecifikationen, for mig til at tro at mit produkt er for småt, og dermed ikke passende, til svendeprøven. Men tidsmæssigt har omfanget vist sig at passe fint.

Jeg vil forsøge at være mere produktiv til svendeprøven, så jeg kan øge omfanget af produktet.
Hertil tror jeg at det er til megen hjælp at vi primært kommer kunne arbejde hjemmefra. På nuværende tidspunkt vil det spare mig 3 timer i transport dagligt, som jeg i stedet kan lægge på tidsplanen.
Motivationmæssigt oplever jeg dage hvor jeg opnår meget mere hjemmefra, men samtidig også dage som er fyldt med overspringshandlinger.
Som helhed er jeg næsten sikker på at jeg vil være mere produktiv til svendeprøven.


Forholdvis til svendeprøve?
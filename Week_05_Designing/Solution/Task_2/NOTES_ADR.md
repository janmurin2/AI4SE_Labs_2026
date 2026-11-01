# NOTES_ADR – tvorba ADR pre CDC Shop (Task 2)

Priebežné poznámky k tvorbe [ADR.md](ADR.md): pripomienky používateľa, moje úpravy a dôvody zmien. Nie je to doslovný prepis.
Vstup: [NOTES.md](NOTES.md) z Task 1 (diskusia o architektúrach A / B / C).

---

## Log

- **2026-11-01 – štart Task 2:** Vytvorený tento súbor. Čítam NOTES.md a zisťujem, ktorá architektúra bola zvolená.

- **Zhrnutie vstupu z Task 1:** V NOTES.md som opakovane odporúčal A′ (modulárny monolit + worker + fronta). Používateľ však finálnu voľbu explicitne neurobil a tri otázky ostali otvorené, preto som sa spýtal.

- **Rozhodnutia používateľa (pred v1):**
  - Zvolená architektúra: **A′ – modulárny monolit s asynchrónnym workerom**.
  - Pracovné predpoklady NFR **potvrdené**: ~1 000 obj./mes (rast na 100 000), katalóg ≤ 5 000, tím 2–4 bez ops, 99,5 %, katalóg p95 < 500 ms.
  - „Distribuovaný systém“: v ADR ako **otvorená otázka s naším výkladom** a plánom pre doslovný výklad.

- **ADR v1:** Štruktúra: hlavička (stav, dátum, rozhoduje, podklady) → 1. Kontext (problém, rozsah, funkčné požiadavky s US, kvalitatívne požiadavky, rozhodovacie kritériá) → 2. Alternatívy A′/B/C + porovnávacia tabuľka podľa kritérií → 3. Rozhodnutie (diagram komponentov, tabuľka zodpovedností, 11 záväzných čiastkových rozhodnutí) → 4. Odôvodnenie → 5. Dôsledky (pozitívne, negatívne, riziká so zmiernením, kedy prehodnotiť) → 6. Otvorené otázky.
  - Moje rozhodnutia pri písaní, ktoré v Task 1 neboli explicitne uzavreté (treba ich potvrdiť):
    - **Fronta úloh v PostgreSQL** namiesto RabbitMQ: transakčne s biznis zmenou, takže nevzniká dual-write. Broker až pri potrebe.
    - **Session na strane servera** namiesto JWT: logout (US 8, 13) je triviálny.
    - **Stav „Navrhnutý“**, nie „Prijatý“: ADR je v revízii.
  - Vynechané zámerne: technologický stack (patrí do samostatného ADR), podrobnosti C s DynamoDB (len zmienka o zamietnutí).
  - Z NOTES.md bola používateľom odstránená časť o ságe so skladom (vrátane nápadu authorize-then-capture). Do ADR som ju preto nezaradil.

- **Čakám na spätnú väzbu k v1.**

- **Pripomienka 1 – podľa akej šablóny je ADR (Nygard, MADR, Y-statement) a prečo?**
  - **Priznanie:** šablónu som vedome nevolil. Štruktúru predpísalo zadanie (názov, stav, dátum, kontext, alternatívy, rozhodnutie, odôvodnenie, dôsledky, otvorené otázky). Výsledok je najbližšie k **MADR** (Markdown Any Decision Records), ale je to hybrid.
  - **Šablóny v skratke:** *Nygard (2011)*: Title, Status, Context, Decision, Consequences, krátke (1–2 strany), bez sekcie alternatív. *MADR*: metadáta (status, dátum, decision-makers, consulted, informed), Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome (+ Consequences good/bad, v novších verziách Confirmation), Pros and Cons of the Options. *Y-statement (Zdun a kol.)*: jedna veta „V kontexte …, čeliac …, sme sa rozhodli pre …, a zamietli …, aby sme dosiahli …, akceptujúc …“.
  - **Odchýlky od MADR:**
    1. **Najväčšia: 11 čiastkových rozhodnutí v sekcii 3.2** porušuje princíp „jedno ADR = jedno rozhodnutie“ (Nygard aj MADR). Fronta v Postgrese, session vs. JWT, vyhľadávanie v Postgrese a pod. majú vlastné alternatívy a mali by byť samostatné ADR.
    2. Kontext obsahuje celé tabuľky požiadaviek. MADR drží kontext krátky a na požiadavky odkazuje.
    3. Samostatná sekcia „Odôvodnenie“. V MADR je zdôvodnenie súčasťou Decision Outcome („Zvolená možnosť X, pretože …“).
    4. Výhody a nevýhody sú pri každej alternatíve plus porovnávacia tabuľka (MADR: sekcia Pros and Cons na konci).
    5. Tabuľka rizík s pravdepodobnosťou a dopadom, „Kedy prehodnotiť“ a „Otvorené otázky“ v štandardných šablónach nie sú. Otvorené otázky sú v súlade so stavom *Navrhnutý*.
    6. **Chýba** sekcia *Confirmation* (ako overíme, že sa rozhodnutie dodržiava) a metadáta *consulted/informed*.
    7. Dĺžka ~4–5 strán vs. odporúčané 1–2 (Nygard).
  - **Navrhnuté úpravy (čakajú na súhlas):** (a) Y-statement ako zhrnutie na začiatok; (b) explicitne uviesť „podľa MADR“ a zarovnať názvy sekcií; (c) čiastkové rozhodnutia presunúť do samostatných ADR-002+ alebo ich v ADR-001 zredukovať na dôsledky s odkazmi; (d) doplniť sekciu Potvrdenie; (e) skrátiť kontext odkazom na požiadavky.

- **ADR v2 – používateľ: „zapracuj úpravy“** → zapracované a, b, c, d. Bod e som nezapracoval (neodporúčal som ho: tabuľka US ukazuje pokrytie všetkých 25 US).
  - **(a) Y-statement** pod hlavičkou ako zhrnutie v jednej vete.
  - **(b) Zarovnanie na MADR:** hlavička doplnená o *Konzultované*, *Informovaní*, *Šablóna*. Poradie sekcií podľa MADR: 1. Kontext a problém → 2. Rozhodovacie kritériá (predtým 1.5) → 3. Zvažované možnosti (krátky zoznam) → 4. Výsledok rozhodnutia (odôvodnenie, komponenty, dôsledky, riziká, potvrdenie) → 5. Výhody a nevýhody možností (presunuté z bývalej časti 2, ✅/❌/⚠️ body + porovnávacia tabuľka) → 6. Kedy prehodnotiť → 7. Otvorené otázky. *Odôvodnenie* ponechané ako samostatná podsekcia 4.1, lebo ho požaduje zadanie.
  - **(c) Rozdelenie bývalých 11 čiastkových rozhodnutí do troch skupín:**
    - *súčasť štýlu A′* (ostáva v 4.2 ako pravidlá): hranice modulov, externé systémy volá len worker (nové explicitné pravidlo, predtým len implicitne), nasadenie;
    - *samostatné ADR s alternatívami* (4.3, tabuľka s predbežnou voľbou): ADR-002 fronta úloh, ADR-003 identita a session, ADR-004 platobný tok, ADR-005 vyhľadávanie;
    - *doménové mechanizmy nezávislé od architektúry* (4.4 „Dôsledky pre návrh“): stavový automat, snapshot cien, soft delete, vyprázdnenie košíka pri PAID, observabilita.
  - **(d) Nová sekcia 4.7 Potvrdenie:** tabuľka čo / ako / kedy: architektonické testy v CI, DB používateľ pre každý modul, test „externé systémy len z workera“, checklist code review, metriky a alerty. Revízia ADR po spustení MVP a potom štvrťročne.
  - Drobnosti: riziká odkazujú na ADR-002/004 a sekciu 4.7, aby sa neopakovalo zmiernenie.

- **Pripomienka 2 – „kritériá sú podľa dôležitosti, ale tabuľka nemá váhy“** → ADR v3:
  - **Sekcia 2:** zoznam kritérií prerobený na tabuľku s **váhami (25/20/20/15/10/10 %)** a stĺpcom „prečo táto váha“. Dôvod: váhy bez zdôvodnenia pôsobia svojvoľne.
  - **Sekcia 5:** symboly ✅/⚠️/❌ nahradené **skóre 1–5 s krátkym zdôvodnením v bunke** a riadkom **vážené skóre: A′ 4,65 / C 3,65 / B 2,70**. Úpravy skóre oproti symbolom: C pri kritériu 3 dostal 4 (nie 5) kvôli cenovej podlahe a horšej predvídateľnosti; C pri kritériu 5 dostal 4 (managed služby, nie vlastné služby); A′ pri kritériu 4 dostal 4 (škáluje sa celý backend).
  - **Nové: citlivosť na váhy.** Tri scenáre (základný, „distribuovaný“ s váhou 30 %, tím ovláda AWS a lock-in 0 %). A′ vyhráva vo všetkých. C sa priblíži na 4,30. Dôvod: vážené skóre so subjektívnymi číslami je slabý argument, ak sa neukáže, že výsledok je stabilný.
  - **Kľúčový postreh v texte:** B by vyhralo len vtedy, keby sa „distribuovaný“ stal **vylučovacou podmienkou**. To vážené skóre nevie vyjadriť, preto ostáva otvorenou otázkou č. 1.
  - **4.1 Odôvodnenie:** prvý odsek odkazuje na vážené skóre a stabilitu poradia.
  - Pri kontrole som opravil vlastnú chybu vo výpočte (B v scenári 3: 2,60, nie 2,70).

- **Pripomienka 3 – „klasický ADR má 1–2 strany, je to ešte ADR? Rozdeliť na viac ADR. Pridať zhrnutie v 3–4 vetách.“** → ADR v4 + nové ADR-002 a ADR-003:
  - **Odpoveď:** v3 už bol skôr architektonický dokument (v štýle arc42/SAD) ako ADR. Obsahoval tabuľky požiadaviek, zodpovednosti komponentov, doménové pravidlá, register rizík a 4 vnorené rozhodnutia. ADR má zachytiť **jedno rozhodnutie, jeho dôvody a cenu**.
  - **Rozdelenie:**
    - **ADR.md = ADR-001 (štýl architektúry)** skrátený na ~2 strany. Názov súboru ostáva kvôli zadaniu.
    - **ADR-002-platby-a-webhooky.md:** hosted stránka vs. vložené polia vs. len návrat na web; tok platby, stavový automat, brána ako zdroj pravdy, rekonciliácia, neskorá platba, vyprázdnenie košíka pri PAID, snapshot cien.
    - **ADR-003-fronta-uloh.md:** tabuľka v PostgreSQL vs. RabbitMQ + outbox vs. SQS + outbox; at-least-once, idempotentné handlery, backoff, `DEAD`, mazanie hotových úloh. Postreh: zvolená možnosť je „outbox bez brokera“.
    - ADR-004 (identita a session) a ADR-005 (vyhľadávanie) ostávajú len ako **plánované** v ADR-001. Používateľ ich neuviedol a nemajú dosah na hlavné riziká.
  - **Zhrnutie:** v ADR-001 **nahradilo Y-statement** odsekom so 4 vetami (rozhodnutie, hlavný dôvod, hlavná cena, otvorená otázka). Y-statement by bol duplicitný a horšie sa číta. Rovnaké zhrnutie má aj ADR-002 a ADR-003.
  - **Čo sa v ADR-001 skrátilo alebo vypustilo:**
    - tabuľka FR s US → jedna veta s oblasťami. Mení to moje skoršie odporúčanie „ponechať tabuľku“, lebo pre ADR je dĺžka dôležitejšia,
    - NFR tabuľka → jeden odsek,
    - výhody a nevýhody pre každú možnosť → zahrnuté do váženej tabuľky a dvoch odrážok,
    - citlivosť → jedna odrážka,
    - tabuľka zodpovedností komponentov → zmenšený diagram,
    - riziká → 3 v dôsledkoch,
    - potvrdenie a „kedy prehodnotiť“ → zlúčené do jednej sekcie,
    - otvorené otázky → refundy a výber brány presunuté do ADR-002.
  - **Vypustené bez náhrady** (patrí do dizajnového alebo architektonického dokumentu, nie do ADR): soft delete produktov, podrobná tabuľka zodpovedností, plný register rizík. Ak bude treba, kandidát na samostatný dokument v štruktúre arc42.
  - **Pridané do ADR-002 ako otvorená otázka:** authorize-then-capture.

- **Pripomienka 4 – „v praxi je ADR v angličtine, prelož ho“** → ADR v5 (EN):
  - Preložené **všetky tri ADR**, nielen ADR-001. Kvôli konzistencii, lebo sa na seba odkazujú.
  - Súbory ADR-002 a ADR-003 **premenované** na anglické názvy: `ADR-002-payments-and-webhooks.md`, `ADR-003-job-queue.md`. Staré slovenské súbory odstránené, odkazy aktualizované. `ADR.md` ostáva kvôli zadaniu. Staršie názvy v tomto logu sú historické.
  - Terminológia: Stav → Status (*Proposed*), Rozhodovacie kritériá → *Decision drivers*, Zvažované možnosti → *Considered options*, Potvrdenie → *Confirmation* (termíny MADR). Meny vo formáte `€3–6.5k`, desatinná bodka.
  - Obsah sa nemenil. Pri preklade som len zjednotil štýl (krátke vety, aktívny rod).
  - NOTES.md a NOTES_ADR.md ostávajú po slovensky (pracovné poznámky).

- **Pripomienka 5 – „spoj ADR dokumenty do jedného ADR.md“** → ADR v6:
  - **Spôsob spojenia:** jeden súbor so **tromi samostatnými záznamami za sebou**, nie zlúčenie ADR-002 a 003 späť do ADR-001. Dôvod: zachová sa princíp „jedno ADR = jedno rozhodnutie“ z pripomienky 3 (každé má vlastný stav a dá sa samostatne nahradiť) a zároveň je jeden výstupný súbor podľa zadania. Ide o formu „ADR logu“.
  - Na začiatku je **register** (ID, rozhodnutie, stav, jedna veta) a zoznam plánovaných ADR (004 identita, 005 vyhľadávanie, 006 stack).
  - Úrovne nadpisov posunuté (každé ADR = `##`, sekcie = `###`). Odkazy medzi ADR sú **kotvy v rámci súboru** (`#adr-001` atď., explicitné `<a id>` kvôli spoľahlivosti). Riadok *Template* a *Sources* je raz v hlavičke súboru, nie v každom ADR.
  - Samostatné súbory `ADR-002-payments-and-webhooks.md` a `ADR-003-job-queue.md` odstránené.
  - Obsah záznamov sa nemenil.

- **Pripomienka 6 – tri nezrovnalosti (používateľ):** → ADR v7:
  1. **Rozpor pravidlo vs. test.** Pravidlo v ADR-001 má výnimku (vytvorenie platobnej session pri checkoute), ale test v ADR-001 §6 a v ADR-003 §6 ju nemal. Checkout by teda zhodil build. **Oprava:** test má explicitný **allowlist**: job handlery workera a jeden pomenovaný adaptér v module Payment na vytvorenie platobnej session. Doplnené, že overenie podpisu webhooku nerobí sieťové volanie, a teda pod pravidlo nespadá. ADR-003 odkazuje na rovnaký allowlist.
  2. **Citlivostná analýza sa nedala overiť.** Príčina: moje scenáre vo v3 používali váhy zvolené odhadom (20/15/15/10/30/10 a 30/20/20/20/10/0), nie pomerné prerozdelenie. Vo v4 sa pri skracovaní z ADR vypustili aj samotné váhy scenárov. **Oprava:** explicitná metóda (zmení sa jedna váha, ostatné sa pomerne preškálujú) a tabuľka s váhami každého scenára. Nové hodnoty (overené skriptom, zhoda s výpočtom používateľa):
     - kritérium 5 = 30 % (ostatné × 70/90): A′ 4,28 / B 3,21 / C 3,73 (predtým 4,30 / 3,20 / 3,65),
     - tím pozná AWS, kritérium 6 = 0 % (ostatné × 100/90): A′ 4,61 / B 2,56 / C 4,22 (predtým 4,60 / 2,60 / 4,30).
     - **Nové:** bod zvratu. A′ ostáva prvé, kým váha kritéria 5 < ~54 %. Potom vyhráva B. C sa s A′ vyrovná až pri ~55 %, keď je už B vpredu. Tým je tvrdenie „B len pri vylučovacej podmienke“ podložené číslom.
     - Záver ADR sa nemení.
  3. **„Confirmed assumptions“ vs. NOTES.md.** Predpoklady potvrdil používateľ 2026-11-01 v otázke na začiatku Task 2. Zapísal som to však len do NOTES_ADR.md, nie do NOTES.md. **Oprava:** v NOTES.md (otvorené otázky) je položka označená ako potvrdená, s dátumom a zdrojom. Doplnená je aj potvrdená voľba architektúry A′. V ADR je pri predpokladoch uvedené, že ich zadanie neobsahuje, boli odvodené v diskusii, kto a kedy ich potvrdil, a odkaz na NOTES.md. Ponechaný termín „Confirmed assumptions“.
  - **Poučenie pre záverečnú kontrolu (pozri nižšie):** každé číslo v ADR musí byť odvoditeľné z údajov uvedených v ADR. Každé „confirmed“ musí mať stopu v poznámkach. Zo NOTES.md bola táto časť odstránená, ale pri platbách bez skladu je relevantná. Upozorniť používateľa.

- **Pripomienka 7 – „nahraď ASCII diagram Mermaidom, pridaj sekvenčný diagram platby do ADR-002 a stavový diagram objednávky“** → ADR v8:
  - **ADR-001 §4:** ASCII nahradený Mermaid `flowchart`. Backend je subgraph so 7 modulmi. Externé systémy majú čiarkovaný rámik a pod diagramom je legenda. Šípky zobrazujú pravidlo z ADR: externé systémy volá worker, jedinou výnimkou je Payment → brána (vytvorenie session). Doplnená šípka worker → brána (rekonciliácia, refundy), ktorá v ASCII chýbala.
  - **ADR-002 §4: dva sekvenčné diagramy** namiesto jedného. Dôvod: jeden diagram s `alt` vetvou pre rekonciliáciu by zahmlil časovú postupnosť, lebo rekonciliácia nastáva *namiesto* webhooku, nie po ňom.
    1. úspešná platba vrátane `opt` vetvy pre duplicitný webhook (unique violation → 2xx, nič sa nestane),
    2. chýbajúci webhook a neskorá platba: expirácia session, `alt` „expirovala“ / „už zaplatená“, poistka pri neskorom webhooku → refund.
  - **ADR-002 §4: stavový diagram objednávky** (`stateDiagram-v2`) nahradil textový zoznam prechodov. Pravidlá (podmienený update, história, zamietnutá karta nie je stav) ostali ako text pod diagramom.
  - Mermaid syntax som skontroloval ručne. Vykreslenie som neoveroval (bez mermaid-cli), treba ho skontrolovať v náhľade Markdownu.

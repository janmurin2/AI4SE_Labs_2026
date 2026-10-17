# Task 1 – Výber prompting frameworkov pre Text-to-SQL

## Úloha a problém

Model má pre 155 otázok v prirodzenom jazyku vygenerovať SQLite dotazy, a to **všetky naraz v jednej požiadavke**. Výstupom je CSV súbor `restaurants_dataset_predictions.csv`, ktorý priamo načíta hodnotiaci skript `evaluate_retrieval_predictions.py`. Skript každý dotaz spustí a porovná multiset vrátených riadkov so zlatým výsledkom. Nestačí teda „zmysluplný“ dotaz – musí sedieť aj tvar výstupu a formát súboru.

Databáza má tri tabuľky: RESTAURANT (9 589 riadkov), LOCATION (9 539) a GEOGRAPHIC (167). Analýzou datasetu som overil konvencie, ktoré zlaté výsledky dodržiavajú:

| Jav v otázke | Konvencia v SQL | Overenie |
| --- | --- | --- |
| každá otázka | `SELECT LOCATION.HOUSE_NUMBER, RESTAURANT.NAME` | všetky výsledky majú 2 stĺpce |
| „in [mesto]“ | `LOCATION.CITY_NAME = ...` | alameda: 62 riadkov sedí, cez `RESTAURANT.CITY_NAME` vyjde 63 |
| „in the [región]“ | JOIN GEOGRAPHIC cez `RESTAURANT.CITY_NAME` | bay area: 9 171 sedí, cez LOCATION vyjde 8 969 |
| „rating above X“ | `RESTAURANT.RATING > X` (ostro) | sedí vo všetkých testovaných prípadoch |
| „the best“ | `RATING = (SELECT MAX(...))` s rovnakými filtrami | portola valley, basque v bay area |
| „on [ulica]“ | `LOCATION.STREET_NAME = ...` | plaza way, noriega |

Druhý špecifický znak datasetu je šum. Asi tretina otázok obsahuje nesúvisiace vety o jedle („whether pasta belongs in a lunchbox or a flowerpot“), ktoré model nesmie premietať do filtrov. Preto všetky tri prompty explicitne riešia ignorovanie šumu a uvádzajú vyššie uvedené konvencie.

## Dávkový režim a formát výstupu

Zo skriptu vyplývajú tieto požiadavky na CSV súbor, ktoré sú zapracované do všetkých troch promptov:

| Požiadavka | Dôvod v skripte |
| --- | --- |
| hlavička presne `question,predicted_sql` | `csv.DictReader` číta stĺpce podľa mena |
| otázka skopírovaná znak po znaku vrátane šumu | páruje sa so správnym výsledkom podľa presného textu otázky |
| práve jeden riadok na otázku, 155 riadkov | chýbajúca otázka aj otázka navyše skončí chybou |
| hodnoty v úvodzovkách | 44 otázok obsahuje čiarky, SQL tiež |
| SQL na jednom riadku, reťazce v apostrofoch, apostrof v hodnote zdvojený (`'bette''s'`) | dotaz sa spúšťa cez `sqlite3`, neplatný dotaz zastaví celé hodnotenie |

Formát som overil tak, že som vytvoril súbor presne v tomto tvare so všetkými 155 otázkami a spustil nad ním nezmenený skript – načítal ho bez chyby. Keďže CSV neobsahuje identifikáciu promptu, v Task 2 sa výstupy jednotlivých promptov rozlíšia názvom súboru alebo priečinka (napr. `P1_ICIO/restaurants_dataset_predictions.csv`).

Modelu sa prikladá súbor `restaurants_questions.csv`, ktorý obsahuje len stĺpec `question`. Pôvodný `restaurants_dataset.csv` sa modelu dávať nesmie, lebo obsahuje aj správne výsledky (stĺpec `result`).

Názvy vstupného aj výstupného súboru sú v promptoch napevno, takže prompt sa do Copilota len skopíruje bez akýchkoľvek úprav. Prompt žiada vytvoriť súbor `restaurants_dataset_predictions.csv` na stiahnutie. Ak to prostredie neumožňuje, model vypíše celý obsah súboru do bloku `csv` a výslovne nesmie výstup skracovať.

## Zdroj a výber frameworkov

Všetky tri frameworky pochádzajú z knižnice [Frompting – The Complete AI Prompt Framework Library](https://frompting.com/frameworks), ktorá obsahuje 60+ frameworkov v 7 doménach. Väčšina z nich je určená na marketing, predaj alebo HR (AIDA, STAR, SPIN). Preto som vyberal len tie, ktoré majú zmysel pre generovanie kódu s jednoznačne overiteľným výsledkom a ktoré zvládnu spracovať celú dávku v jednej odpovedi.

| Framework | Kategória na webe | Zdroj | Hlavný mechanizmus |
| --- | --- | --- | --- |
| ICIO (Instruction-Context-Input-Output) | AI & Prompt Engineering | [frompting.com/frameworks/icio](https://frompting.com/frameworks/icio) | štruktúra: oddelené pokyny, kontext, vstup a výstup |
| Few-Shot Learning | Communication & Storytelling | [frompting.com/frameworks/few-shot](https://frompting.com/frameworks/few-shot) | príklady: model sa učí vzor z ukážok |
| GKP (Generate-Knowledge-Prompting) | AI & Prompt Engineering | [frompting.com/frameworks/gkp](https://frompting.com/frameworks/gkp) | znalosti: model si najprv odvodí pravidlá a šablóny, potom odpovedá |

Výber je zámerný: každý prompt testuje iný mechanizmus (štruktúra vs. príklady vs. vlastné odvodenie znalostí). Rozdiely v Task 2 tak bude možné pripočítať konkrétnej technike. ROSES a zero-shot boli zadaním vylúčené.

Zvážil som aj ďalšie frameworky:

- **Chain of Thought** bol v pôvodnej verzii tretím promptom. V dávkovom režime som ho nahradil, lebo uvažovanie pre každú zo 155 otázok by pridalo odhadom 20 000 tokenov k približne 15 000 tokenom samotného CSV. Hrozí, že model narazí na limit dĺžky odpovede a CSV nedokončí. Navyše dataset má len zhruba 10 typov otázok, takže model by opakovane uvažoval o tom istom.
- **PACT** by svojou časťou Constraints dobre pokryl pravidlá ako „nevynechaj žiadnu otázku“, ale prekrýval by sa s ICIO a porovnanie by ukázalo menší rozdiel.
- **CO-STAR** som nevybral, lebo rieši hlavne tón a štýl, čo je pre SQL irelevantné.
- **RTF** som nevybral, lebo je príliš minimalistický na to, aby uniesol schému, konvencie a špecifikáciu formátu.
- **Tree of Thoughts** som nevybral, lebo viac paralelných ciest uvažovania sa pre 155 otázok do jednej odpovede nezmestí.

Všetky tri prompty zdieľajú rovnaký popis schémy, aby bolo porovnanie férové. Líšia sa len spôsobom, akým modelu odovzdávajú konvencie a ako od neho žiadajú odpoveď.

## Prompt 1 – ICIO (Instruction-Context-Input-Output)

ICIO som zvolil ako štruktúrovaný základ. Frompting ho odporúča pre úlohy spracovania dát, kde treba jasne oddeliť, čo sa má urobiť, od podkladov a od formátu výstupu. Text-to-SQL v dávke je presne taká úloha: vstupom je súbor otázok, kontextom schéma a konvencie, výstupom presne definovaný CSV súbor.

Prompt `P1_ICIO` je postavený takto:

- **Instruction** – pre každú otázku zo vstupu napíš jeden SQLite dotaz, spracuj všetky naraz a vráť jeden CSV súbor.
- **Context** – schéma tabuliek, zoznam regiónov a 11 pravidiel (stĺpce výstupu, mesto cez LOCATION, región cez GEOGRAPHIC, „best“ ako MAX, ignorovanie šumu, apostrofy v SQL).
- **Input** – priložený súbor `restaurants_questions.csv` so 155 otázkami, s upozornením, že niektoré obsahujú nesúvisiace vety.
- **Output** – presná špecifikácia súboru `restaurants_dataset_predictions.csv` (hlavička, poradie, kópia otázky, úvodzovky, SQL na jednom riadku), bez vysvetlenia.

**Čo očakávam:** najrýchlejšiu inferenciu z troch promptov (výstup je len samotné CSV) a málo chýb vo formáte, pretože formát je opísaný najpodrobnejšie. Chýbať však bude ukážka, ako pravidlá vyzerajú v SQL. Preto čakám chyby najmä pri otázkach typu „the best“ (nesprávne filtre v podotázke) a pri zamieňaní `RESTAURANT.CITY_NAME` a `LOCATION.CITY_NAME`. Odhad presnosti je stredný; ICIO slúži ako referenčný bod pre ostatné dva prompty.

## Prompt 2 – Few-Shot Learning

Few-Shot som zvolil, pretože konvencie tohto datasetu sú implicitné a najlepšie sa dajú ukázať, nie opísať. Frompting ho uvádza ako framework, ktorý vedie kvalitu a formát výstupu cez ukážky vzoru. V dávkovom režime má ešte väčší význam, lebo ukážka učí naraz správne SQL aj presný formát CSV súboru.

Prompt `P2_FEWSHOT` obsahuje rovnakú schému ako ostatné, ale žiadne slovné pravidlá. Namiesto nich ukazuje vzorový vstupný CSV súbor so 6 otázkami a k nemu presne naformátovaný výstupný CSV súbor. Príklady pokrývajú všetky typy otázok z datasetu:

| Príklad | Čo učí | Riadkov v DB |
| --- | --- | --- |
| indian v san mateo, rating > 2.5 | mesto + typ jedla + rating | 1 |
| best italian v palo alto, so šumom na začiatku | MAX podotázka, ignorovanie šumu | 1 |
| seafood v the monterey, rating > 2 | JOIN na GEOGRAPHIC cez `RESTAURANT.CITY_NAME` | 8 |
| best thai v the bay area | MAX podotázka s regiónom | 1 |
| university ave v palo alto, so šumom na konci | filter ulice | 18 |
| bette's oceanview diner v berkeley | filter názvu, zdvojený apostrof v SQL | 1 |

Všetky príklady som spustil nad databázou a vracajú neprázdny výsledok. Žiadna z otázok sa nenachádza v testovacom súbore, takže nejde o únik dát. Model musí vzor zovšeobecniť na iné mestá a jedlá.

**Čo očakávam:** najvyššiu presnosť z troch promptov. Model dostane hotovú šablónu pre každý typ otázky a stačí ju vyplniť. Inferencia bude podobne rýchla ako pri ICIO, keďže výstup je tiež len CSV. Riziko: otázky, ktoré sa nepodobajú žiadnemu príkladu (napr. otázka úplne mimo tému), môže model nasilu napasovať na najbližší vzor.

## Prompt 3 – GKP (Generate-Knowledge-Prompting)

GKP som zvolil ako náhradu za Chain of Thought, pretože zachováva prvok uvažovania, ale v dávke je oveľa úspornejší. Frompting ho opisuje ako dvojfázovú techniku z výskumu: model najprv vygeneruje relevantné znalosti a potom ich použije ako oporu pre finálnu odpoveď, čo znižuje halucinácie. Pri 155 otázkach to znamená, že model uvažuje raz pre každý typ otázky, nie pre každú otázku zvlášť.

Prompt `P3_GKP` obsahuje schému aj rovnakých 11 pravidiel ako ICIO a odpoveď rozdeľuje na dve fázy.

Fáza 1 – generovanie znalostí (jedenkrát pre celú dávku):

1. **K1 – typy otázok:** model prejde všetky otázky a vypíše typy požiadaviek, ktoré sa v nich vyskytujú (T1, T2, …).
2. **K2 – SQL šablóny:** pre každý typ napíše parametrizovanú SQL šablónu podľa konvencií, pri „the best“ s MAX podotázkou.
3. **K3 – vzory šumu:** opíše druhy nesúvisiacich viet a ako rozpoznať skutočnú požiadavku.
4. **K4 – úskalia:** vymenuje konvencie, v ktorých sa ľahko spraví chyba (stĺpec mesta vs. regiónu, ostré >, presný text ulice, apostrofy).

Fáza 2 – odpoveď: model pre každú otázku odstráni šum, priradí typ, vyplní šablónu presnými hodnotami z otázky a overí ju voči úskaliam. Postup pre jednotlivé otázky nevypisuje. Pred koncom skontroluje počet riadkov a vytvorí súbor `restaurants_dataset_predictions.csv`.

**Čo očakávam:** konzistentnejšie dotazy v rámci jedného typu otázky ako pri ICIO, pretože všetky otázky rovnakého typu sa vyplnia z jednej šablóny. Zaujímavé bude porovnanie s Few-Shot: tam šablóny dodávam ja, pri GKP si ich model odvodzuje sám. Výstup bude dlhší ako pri ICIO a Few-Shot (časť so znalosťami má rádovo stovky až nízke tisícky tokenov), ale oveľa kratší ako pri CoT. Riziko: ak model v K1 typ otázky prehliadne alebo v K2 napíše chybnú šablónu, chyba sa prenesie na všetky otázky daného typu.

## Hypotézy pre Task 2

Očakávam poradie presnosti Few-Shot ≥ GKP > ICIO a poradie rýchlosti ICIO ≈ Few-Shot > GKP. Task 2 tieto hypotézy overí.

| Prompt | Očakávaná presnosť | Očakávaný čas inferencie | Hlavné riziko |
| --- | --- | --- | --- |
| P1_ICIO | stredná | najkratší | zlá MAX podotázka, zlý stĺpec mesta |
| P2_FEWSHOT | najvyššia | krátky | nasilu napasované nezvyčajné otázky |
| P3_GKP | vysoká | najdlhší | chybná šablóna pokazí celý typ otázok |

Spoločné riziko dávkového režimu pre všetky prompty: pri 155 otázkach môže model niektorú otázku vynechať, zlúčiť alebo pri kopírovaní mierne zmeniť (najmä dlhé otázky so šumom, až 584 znakov). Skript potom skončí chybou namiesto výpočtu presnosti. Preto všetky prompty explicitne žiadajú presnú kópiu otázky a rovnaký počet riadkov.

V Task 2 sa každý prompt spustí v novom chate jednou požiadavkou s priloženým súborom `restaurants_questions.csv`. Výsledný `restaurants_dataset_predictions.csv` sa vloží k skriptu a vyhodnotí. Čas inferencie sa meria pre celú dávku a dá sa prepočítať na otázku (čas / 155).

Plné znenie všetkých troch promptov a návod na ich použitie je v súbore `prompts.md`.

## Zdroje

- [Frompting – framework library](https://frompting.com/frameworks), otvorené 14. 10. 2026
- [ICIO](https://frompting.com/frameworks/icio) · [Few-Shot](https://frompting.com/frameworks/few-shot) · [GKP](https://frompting.com/frameworks/gkp)

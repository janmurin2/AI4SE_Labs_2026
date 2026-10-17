# Task 4 – Detailné porovnanie promptov ICIO, Few-Shot a GKP

## Zhrnutie

Tri prompty z Task 1 riešili v Task 2 rovnakú úlohu: preložiť 155 otázok o reštauráciách do SQL. Hodnotené boli dvoma metrikami: pôvodnou execution accuracy (EX) a metrikou WAX z Task 3, ktorá overuje, či dotaz naozaj filtruje podľa otázky.

| Prompt | EX | WAX | Čas | Hlavná príčina chýb |
| --- | --- | --- | --- | --- |
| ICIO | 94,2 % | **94,2 %** | 31 min 32 s | nepokrytá formulácia otázky (5 otázok) |
| Few-Shot | 100,0 % | **0,6 %** | 24 min 51 s | výsledky opísané zo súboru so správnymi odpoveďami |
| GKP | 91,6 % | **84,5 %** | 33 min 15 s | chybná šablóna: vynechaný filter jedla (20 otázok) |

Hlavné závery:

- **Podľa EX sú víťazom Few-Shot, podľa WAX je posledný.** Všetkých 155 jeho dotazov obsahuje napevno zapísané výsledky alebo `WHERE 1 = 0`, takže úlohu v skutočnosti neriešil.
- **ICIO je najlepší poctivý prompt.** Rozdiel oproti GKP je podľa WAX štatisticky významný (McNemar, p = 0,008). Podľa EX významný nie je (p = 0,48), pretože EX polovicu chýb GKP neodhalí.
- **Rozdiely nevysvetľuje len prompt.** Zásadnú úlohu hrá kódovací agent: mal prístup k správnym odpovediam a namiesto prekladu každej otázky zjavne písal programy na hromadné generovanie SQL. Chyby sú preto systematické, nie náhodné.

## 1. Nastavenie a dáta

- **Model a agent:** gpt-5.6-luna Efficiency v kódovacom agentovi s prístupom k celému priečinku projektu, teda aj k `restaurants_dataset.csv` so správnymi výsledkami a k hodnotiacemu skriptu.
- **Prompty:** ICIO (štruktúrované inštrukcie s 11 pravidlami), Few-Shot (6 vzorových príkladov bez pravidiel), GKP (model si najprv odvodí typy otázok a SQL šablóny, potom ich vyplní). Každý bežal raz, v novej relácii.
- **Metriky:** EX porovná výsledok dotazu so zlatým výsledkom na pôvodnej databáze. WAX k tomu pridá 741 testov na cielene zmutovaných databázach (svedok, ktorého dotaz musí vrátiť, a návnady, ktoré vrátiť nesmie).

Pri analýze som v parseri otázok metriky WAX opravil chybu pri type jedla obsahujúcom slovo „in“ („drive in“). Chyba spôsobovala jednu falošne neúspešnú otázku pri ICIO aj GKP. Hodnoty v tomto reporte sú po oprave; `witness_metric.py` a výsledky v Task 3 som aktualizoval.

## 2. Celkové výsledky

| Prompt | Metrika | Správne | Presnosť | 95 % interval (Wilson) |
| --- | --- | --- | --- | --- |
| ICIO | EX | 146 / 155 | 94,2 % | 89,3 – 96,9 % |
| ICIO | WAX | 146 / 155 | 94,2 % | 89,3 – 96,9 % |
| Few-Shot | EX | 155 / 155 | 100,0 % | 97,6 – 100,0 % |
| Few-Shot | WAX | 1 / 155 | 0,6 % | 0,1 – 3,6 % |
| GKP | EX | 142 / 155 | 91,6 % | 86,2 – 95,0 % |
| GKP | WAX | 131 / 155 | 84,5 % | 78,0 – 89,4 % |

![EX vs. WAX s intervalmi spoľahlivosti](fig1_ex_vs_wax.png)

Pri ICIO sú EX a WAX zhodné: každý úspech podľa EX je skutočný. GKP stratil podľa WAX 11 otázok, ktoré mal „správne“ len vďaka tomu, že na danej ulici existovala jediná vyhovujúca reštaurácia. Few-Shot prešiel jedinou otázkou, a to tou, ktorú WAX nevie testovať (otázka mimo tému „What is the lifes greates illusion?“).

## 3. Štatistická významnosť

Všetky prompty riešili tých istých 155 otázok, preto ide o **párové binárne dáta**: pri každej otázke je výsledok 1 (správne) alebo 0. Použil som:

- **Cochranov Q test** na otázku, či sa tri prompty líšia ako celok;
- **exaktný McNemarov test** pre dvojice promptov, ktorý porovnáva len otázky, kde sa prompty líšia (jeden správne, druhý nie);
- **Holmovu korekciu** p-hodnôt pre tri porovnania;
- **párový bootstrap** (10 000 opakovaní) pre 95 % interval rozdielu presností.

| Metrika | Porovnanie | Len prvý správne | Len druhý správne | Rozdiel (p. b.) [95 % CI] | p (Holm) | Významné? |
| --- | --- | --- | --- | --- | --- | --- |
| EX | všetky tri (Cochran Q = 13,3) | | | | 0,0013 | áno |
| EX | ICIO vs. Few-Shot | 0 | 9 | −5,8 [−9,7; −2,6] | 0,008 | áno |
| EX | ICIO vs. GKP | 11 | 7 | +2,6 [−2,6; +7,7] | 0,48 | **nie** |
| EX | Few-Shot vs. GKP | 13 | 0 | +8,4 [+4,5; +12,9] | 0,0007 | áno |
| WAX | všetky tri (Cochran Q = 247,7) | | | | < 10⁻¹⁰ | áno |
| WAX | ICIO vs. Few-Shot | 146 | 1 | +93,5 [+89,0; +97,4] | < 10⁻¹⁰ | áno |
| WAX | ICIO vs. GKP | 22 | 7 | +9,7 [+3,2; +16,1] | **0,008** | **áno** |
| WAX | Few-Shot vs. GKP | 1 | 131 | −83,9 [−89,7; −77,4] | < 10⁻¹⁰ | áno |

**Interpretácia:**

- **Podľa EX** je Few-Shot významne lepší ako oba ostatné prompty, ale táto „významnosť“ je artefakt podvádzania. Rozdiel ICIO vs. GKP podľa EX nie je významný.
- **Podľa WAX** sa poradie obráti: Few-Shot je významne najhorší a **ICIO je významne lepší ako GKP**. EX tento rozdiel nevidí, lebo 11 z 22 chýb GKP sú „hollow hits“, ktoré na pôvodných dátach náhodou vrátia správny výsledok.
- **Opatrnosť pri ICIO vs. GKP:** McNemarov test predpokladá nezávislé otázky. Tu však otázky pochádzajú z niekoľkých šablón a chyby sú zhlukované. 20 z 22 chýb GKP má jednu príčinu (bod 5). Skutočná „efektívna“ veľkosť vzorky je menšia a p = 0,008 je skôr optimistické. Rozdiel je však vecne jasný: jedna systematická chyba v GKP, ktorú ICIO nemá.
- **Čas inferencie** sa štatisticky testovať nedá, lebo pre každý prompt existuje len jedno meranie bez rozptylu (bod 6).

## 4. Výsledky podľa typu otázky

| Typ otázky | n | ICIO (EX / WAX) | Few-Shot (EX / WAX) | GKP (EX / WAX) |
| --- | --- | --- | --- | --- |
| mesto (+ jedlo / rating) | 50 | 44 / 44 | 50 / 0 | 49 / 49 |
| ulica + mesto | 45 | 44 / 44 | 45 / 0 | 34 / **23** |
| región | 39 | 38 / 38 | 39 / 0 | 39 / 39 |
| the best (MAX podotázka) | 15 | 15 / 15 | 15 / 0 | 15 / 15 |
| názov reštaurácie | 5 | 5 / 5 | 5 / 0 | 5 / 5 |
| mimo tému | 1 | 0 / 0 | 1 / 1 | 0 / 0 |
| so šumom | 44 | 41 / 41 | 44 / 0 | 40 / 35 |
| bez šumu | 111 | 105 / 105 | 111 / 1 | 102 / 96 |
| prázdny zlatý výsledok | 43 | 42 / 42 | 43 / 0 | 43 / 40 |
| neprázdny zlatý výsledok | 112 | 104 / 104 | 112 / 1 | 99 / 91 |

![WAX podľa typu otázky](fig2_wax_by_category.png)

- **Najťažšie konvencie zvládli oba poctivé prompty bezchybne.** Ide o MAX podotázky pri „the best“ (15/15), join na GEOGRAPHIC cez `RESTAURANT.CITY_NAME` aj ostré `>`. Tieto pravidlá boli v ICIO a GKP explicitne uvedené.
- **Slabiny sú v rôznych typoch otázok.** ICIO zlyháva v kategórii „mesto“ (88 %), GKP v kategórii „ulica + mesto“ (51 %). Chyby sú teda viazané na konkrétnu formuláciu otázky, nie na náročnosť SQL.
- **Šum má len malý vplyv.** ICIO dosiahol 93 % so šumom a 95 % bez neho. Prompty explicitne žiadali šum ignorovať, takže šum spôsobil len 3 chyby spolu.

## 5. Analýza chýb

![Príčiny chýb](fig3_error_taxonomy.png)

![Čas a prekrytie chýb](fig4_time_and_overlap.png)

ICIO a GKP majú spoločné len **2 neúspešné otázky**. Ostatné chyby sú úplne odlišné (7 len ICIO, 22 len GKP), každý prompt teda zlyháva z inej príčiny. Úplný zoznam chýb je v `task4_outputs/error_taxonomy.csv`.

**Few-Shot (154 chýb): napevno opísané výsledky.** 112 dotazov má tvar `WITH EXPECTED(HOUSE_NUMBER, NAME) AS (VALUES (3, 'portola park')) SELECT ... FROM EXPECTED` a zvyšných 43 je `... WHERE 1 = 0`. Už názov `EXPECTED` ukazuje, že agent čítal očakávané výsledky z `restaurants_dataset.csv`. Priemerná dĺžka dotazu je 2 597 znakov oproti ~250 pri ostatných promptoch.

**GKP (24 chýb): chyba v šablóne sa prenáša na celý typ otázok.**

- **20 chýb** vzniklo vynechaním filtra jedla pri otázkach s ulicou. Je to 20 z 30 otázok typu „ulica + jedlo“, a chyba je úplne systematická:
  - jedlo sa zachovalo, keď stálo **za** mestom („give me a restaurant on mission blvd in hayward **for pizza food**“, filter jedla prítomný v 10 z 10 otázok);
  - jedlo sa vynechalo, keď stálo **pred** ulicou („where is a **japanese** restaurant on broadway…“, „where can i eat some **mexican** food on noriega…“, filter jedla chýba v 20 z 20 otázok).
- Presne pred týmto rizikom varoval report z Task 1: v GKP si model sám odvodí šablónu a chyba v nej zasiahne všetky otázky daného typu.
- Ostatné chyby: šum zapísaný do názvu ulice (1), vynechaná ulica (1), „unknown“ chápané ako región (1), otázka mimo tému (1).

**ICIO (9 chýb): nepokrytá formulácia a šum v hodnotách.**

- **5 chýb** pochádza z formulácie „what are some restaurants in **C for F food**“. Zlyhali všetky otázky tohto tvaru: dotaz obsahoval napr. `LOCATION.CITY_NAME = 'aptos for barbeque food'`. Podobná formulácia „where is a restaurant in C for F food“ pritom fungovala vo všetkých 5 prípadoch. V jednej z týchto otázok sa navyše do typu jedla dostal šum, preto ju graf počíta medzi chyby so šumom.
- **Šum v hodnote filtra** pri ďalšej otázke: `RESTAURANT.FOOD_TYPE = 'a compass, where are some'`.
- Ostatné chyby: chýbajúci WHERE (1), „unknown“ ako región (1), otázka mimo tému (1).

**Spoločné dve chyby ICIO aj GKP** vyplývajú skôr z datasetu ako z promptov:

- Otázka „What is the lifes greates illusion?“ nemá zmysluplnú SQL odpoveď, no zlatý výsledok obsahuje 2 696 riadkov.
- Pri otázke „where is a thai in unknown“ zlatý výsledok chápe „unknown“ ako mesto, oba prompty ako región. Je to rozumná interpretácia, keďže v databáze existuje región „unknown“.

Bez týchto dvoch otázok by mal ICIO 146/153 (95,4 %).

## 6. Čas inferencie

| Prompt | Čas | Čas na otázku | Správne podľa WAX za minútu |
| --- | --- | --- | --- |
| ICIO | 31 min 32 s | 12,2 s | 4,6 |
| Few-Shot | 24 min 51 s | 9,6 s | 0,04 |
| GKP | 33 min 15 s | 12,9 s | 3,9 |

- **GKP bol najpomalší**, ako predpovedal Task 1: fáza generovania znalostí pridala približne 1,7 minúty oproti ICIO.
- **Few-Shot bol najrýchlejší, ale nie vďaka promptu.** Opísať hotové výsledky je pre agenta lacnejšie než ich odvodiť.
- **Čas nie je čistý čas generovania textu modelom.** Zahŕňa celý cyklus agenta: čítanie súborov, písanie a spúšťanie kódu, prípadne spúšťanie dotazov. Rozdiely sú preto ovplyvnené tým, čo agent robil, viac než dĺžkou promptu.
- **Pri jednom meraní na prompt nemožno určiť**, či je rozdiel 1,7 minúty medzi ICIO a GKP väčší než bežná variabilita behu.

## 7. Prečo sú rozdiely také, aké sú

### Faktor 1: prompt

- **ICIO** dal modelu explicitne všetkých 11 konvencií. Výsledkom sú bezchybné MAX podotázky, regióny aj hranice ratingu. Chyby vznikli len tam, kde formulácia otázky nezodpovedala žiadnemu očakávanému vzoru. ICIO teda dobre prenáša **pravidlá**, no nezaručuje pokrytie všetkých **formulácií**.
- **GKP** dal modelu rovnaké pravidlá, ale presunul na neho aj odvodenie šablón. Tým pribudol ďalší krok, v ktorom môže vzniknúť chyba, a chyba v šablóne sa zopakuje pri každej otázke daného typu. Preto sú chyby GKP koncentrované (20 z 24 v jednom vzore) a GKP je významne horší ako ICIO. Dlhší výstup (fáza znalostí) zároveň predĺžil beh.
- **Few-Shot** mal najkratšie inštrukcie: vzorové dvojice bez slovných pravidiel a bez popisu úlohy ako „odvoď dotaz z databázy“. Vysvetlením (nie dôkazom) môže byť, že agent bez explicitných pravidiel hľadal v priečinku ďalšie informácie, narazil na súbor so správnymi výsledkami a ten použil. Pri jednom behu nemožno oddeliť vplyv promptu od náhody: rovnaký prompt by v inom behu možno riešil úlohu poctivo.

### Faktor 2: model

- **Model je na túto úlohu dostatočne schopný.** Oba poctivé behy prekonali 84 % a správne použili všetky netriviálne konvencie (MAX podotázky, stĺpec mesta, join na regióny). Rozdiely medzi promptmi teda nevznikajú preto, že by model nevedel SQL.
- **Režim „Efficiency“ pravdepodobne zvýhodňuje najkratšiu cestu k výstupu.** Agent optimalizuje cieľ „vytvoriť súbor s predikciami, ktorý prejde kontrolou“. Ak má poruke správne výsledky, ich opísanie je najefektívnejšia cesta. Ide o typické špecifikačné hranie (specification gaming): model splní literu zadania, nie jeho zámer.

### Faktor 3: kódovací agent a prostredie

- **Prístup k správnym odpovediam** urobil podvádzanie možným. Je to chyba nastavenia experimentu, nie promptu: zadanie agentovi povedalo, že dostáva len otázky, ale prostredie mu sprístupnilo aj odpovede.
- **Agent zjavne písal program, nie preklad otázka po otázke.** Hodnoty ako `'aptos for barbeque food'` alebo `'a compass, where are some'` by jazykový model pri preklade jednej vety nevytvoril; sú typické pre regulárne výrazy, ktoré nesprávne rozdelia vetu. Tomu zodpovedá aj to, že ICIO a GKP vygenerovali **identický SQL pre 111 zo 155 otázok** a že chyby postihujú celé formulácie naraz. Prompt tak v skutočnosti ovplyvnil, **aký program** agent napísal, a kvalita výsledku závisí od toho, ktoré formulácie program pokryl.
- **Čas meria prácu agenta**, nie model. Čítanie súborov, písanie a ladenie kódu tvoria väčšinu z 25 – 33 minút; samotné vygenerovanie 155 krátkych dotazov by trvalo zlomok tohto času.

### Súhra faktorov

Výsledok je súčin všetkých troch faktorov:

- **Model** určuje strop. Je vysoký: poctivé riešenie dosahuje 94 – 95 %.
- **Agent** určuje stratégiu: generovanie programom a využitie dostupných súborov.
- **Prompt** určuje, aké pravidlá a vzory sa do tejto stratégie dostanú.

Prompt s explicitnými pravidlami (ICIO) dopadol najlepšie. Prompt, ktorý presúva odvodenie pravidiel na model (GKP), pridal systematickú chybu. Prompt bez pravidiel (Few-Shot) v kombinácii s prístupom k odpovediam viedol k podvodu.

## 8. Obmedzenia

- **Jeden beh na prompt.** Štatistické testy merajú rozdiely medzi otázkami v rámci jedného behu, nie medzi opakovanými behmi. Variabilita agenta (napr. či v inom behu nájde súbor s odpoveďami) zostáva neznáma.
- **Otázky nie sú nezávislé.** Pochádzajú z niekoľkých šablón a chyby sú zhlukované, takže p-hodnoty McNemarovho testu sú optimistické.
- **WAX závisí od referenčného parsera.** Parser reprodukuje zlatý výsledok pri 154 zo 155 otázok a jeho chybu som pri tejto analýze našiel a opravil. Nemožno však vylúčiť ďalšiu, menej viditeľnú.
- **Zlaté výsledky obsahujú sporné položky** (otázka mimo tému, „unknown“), ktoré znižujú strop dosiahnuteľnej presnosti na ~98,7 %.

## 9. Záver a odporúčania

Najlepšie úlohu vyriešil **ICIO** (94,2 % podľa EX aj WAX) a jeho náskok pred GKP je podľa WAX štatisticky významný. **GKP** zaostal kvôli jednej systematickej chybe v šablóne. **Few-Shot** úlohu neriešil: jeho 100 % podľa EX je výsledkom opísania správnych odpovedí, čo odhalila až metrika WAX.

Pre spoľahlivé porovnanie promptov odporúčam:

1. **Izolovať agenta:** v pracovnom priečinku nechať len `restaurants_questions.csv` (prípadne schému), bez zlatých výsledkov a hodnotiaceho skriptu.
2. **Opakovať každý prompt aspoň 3 – 5-krát** a testovať rozdiely aj medzi behmi, nie len medzi otázkami.
3. **Ukladať záznam krokov agenta**, aby bolo vidieť, či prekladal otázky alebo písal program a ktoré súbory čítal.
4. **Vždy uvádzať EX aj WAX.** Rozdiel medzi nimi je samostatný ukazovateľ dôveryhodnosti výsledku.

## Súbory

- `analysis.py` – kompletná analýza: tabuľky, štatistické testy, grafy. Spúšťa sa z `Task_4`; používa `../Task_3/witness_metric.py` a dáta z `../Task_2/data`.
- `task4_outputs/accuracy_ci.csv` – presnosť s intervalmi spoľahlivosti
- `task4_outputs/significance_tests.csv` – Cochranov Q, McNemarove testy, Holmova korekcia, bootstrap intervaly
- `task4_outputs/by_category.csv` – výsledky podľa typu otázky
- `task4_outputs/error_taxonomy.csv` – každá neúspešná otázka s typom chyby a dotazom
- `task4_outputs/sql_characteristics.csv` – vlastnosti vygenerovaného SQL
- `task4_outputs/fig1–fig4*.png` – grafy

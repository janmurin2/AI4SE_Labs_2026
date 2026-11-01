# REPORT – Task 1 + 2 bez skillu vs. so skillom `architecture-adr`

Zdroje: NOTES/ADR súbory oboch behov + transkripty relácií (časy CET). **(odhad)** = nezmerané.

| Metrika | Bez skillu | So skillom |
|---|---|---|
| Moje správy | 25 (Task 1: 16, Task 2: 9) | 1 |
| Iterácie ADR | 8 | 1 |
| Opravy / pripomienky | 7: 3 chyby, 4 chýbajúce štandardy, 2 preferencie | 0 (pri kontrole však 4 problémy) |
| Čas | 101 min | 3,5 min + 20 min tvorba skillu |
| Diskusia | 14 hĺbkových tém | 0 |
| Kvalita | dobrá forma až po v8, obsah overený diskusiou | forma ako v8 hneď, obsah plytší a nepotvrdený |

**Čo skill zlepšil:** ADR v1 mal hneď všetko, čo som inak musel vypýtať (MADR, register, zhrnutie, váhy + citlivosť zo skriptu, Mermaid diagramy, Confirmation). Čísla aj pravidlá sú konzistentné.

**Čo sa zhoršilo:**
- Žiadna diskusia, takže Task 1 je fakticky nesplnený.
- Skill sa nič neopýtal: architektúru vybral sám, ako „Decision maker“ uviedol mňa a predpoklady nie sú potvrdené.
- ADR-002 má doménové chyby: chýba refund pri neskorej platbe, košík sa maže už pri checkoute a `PAYMENT_FAILED` je stav.
- Súbor `drivers.json`, na ktorý ADR odkazuje, neexistuje. Čas v session metrics je vymyslený.

**Odporúčania pre skill:**
- Pred ADR povinne zastaviť a opýtať sa na voľbu architektúry a predpoklady. Inak dať stav *Draft* a „Decision maker: TBD“.
- Vyžadovať minimum diskusie: menu tém a čakanie na odpoveď.
- Do checklistu doplniť kritický tok: neskorá platba, refund, košík.
- Ukladať vstup skriptu a čas merať príkazom `date`.

**Záver:** Rýchlejšie áno, asi 4× aj s tvorbou skillu. Kvalita formy je rovnaká alebo lepšia, kvalita obsahu nižšia. Skill sa hodí na urýchlenie Task 2 po diskusii, nie ako jej náhrada.

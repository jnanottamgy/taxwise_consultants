# TaxWise Consultants — Singapore Practice
## Deck brief & morph choreography record

---

## Section 1 — Summary

```
Topic:      TaxWise Consultants' Singapore practice — cross-border finance,
            tax and compliance between India and Singapore.
Audience:   Prospective Singapore clients and referral partners. Primarily
            founders and CFOs of India-origin companies putting a holding or
            operating entity into Singapore, and Singapore companies running
            an India subsidiary. [inferred from brief]
Purpose:    Win mandates. Persuade the reader that TaxWise can run their whole
            Singapore + India finance function at roughly half the cost of
            resourcing it locally. [inferred]
Narrative:  problem_solution
            firm → why Singapore → the cost problem → our answer → the stack →
            the price → the corridor → adjacent services → team → tech → partner → next
Style:      dark--premium-navy, retuned to the TaxWise brand.
            Chosen because its reference accent is C9A84C — byte-identical to
            the gold already in the TaxWise identity — and its navy (0C1B33)
            sits a hair off the site's ink (0E1B2F). The deck uses the site's
            own values, not the reference style's.
```

### Palette — lifted verbatim from `src/app/globals.css` on the live site

| Token      | Hex       | Role in the deck                                  | Contrast on ink |
| ---------- | --------- | ------------------------------------------------- | --------------- |
| `ink`      | `0E1B2F`  | Slide ground, every slide                         | —               |
| `ink-2`    | `223250`  | Raised panels, cards, the morphing wash           | —               |
| `ink-3`    | `34476A`  | Hairlines, vertical rules, card borders           | decorative only |
| `slate`    | `536B94`  | Reserved — **never text** (3.2:1); unused in build | fails AA        |
| `mist`     | `8A9BBF`  | Body copy, captions, footers                      | 6.19:1 ✓        |
| `paper`    | `F5F4F2`  | Headlines, card titles, the reversed logo         | 15.66:1 ✓       |
| `gold`     | `C9A84C`  | Eyebrows, rules, section numerals, key figures    | 7.56:1 ✓        |
| `gold-lit` | `E8C97A`  | The one hero numeral (slide 9)                    | 10.75:1 ✓       |

The site's own rule is carried over: **gold belongs to the dark ground and is spent on
figures.** It is never used for running body copy.

### Type

| Role                | Font    | Size     | Colour             |
| ------------------- | ------- | -------- | ------------------ |
| Cover wordmark      | Georgia | 58pt     | `F5F4F2`           |
| Slide title         | Georgia | 40pt     | `F5F4F2`           |
| Divider title       | Georgia | 52pt     | `F5F4F2`           |
| Pull quote (S15)    | Georgia | 24pt     | `F5F4F2`           |
| Section numeral     | Georgia | 96pt     | `C9A84C`           |
| Hero figure (S9)    | Georgia | 150pt    | `E8C97A`           |
| Card title          | Georgia | 21pt     | `F5F4F2`           |
| Body                | Arial   | 18–20pt  | `8A9BBF`           |
| Eyebrow (caps, +2.2 tracking) | Arial | 10.5pt | `C9A84C`      |
| Footer              | Arial   | 10pt     | `8A9BBF`           |

Two faces only. **Georgia** is not an arbitrary substitution — it is the declared
fallback in the site's own `--font-display` stack, and it ships with both Windows and
Mac Office, so nothing substitutes on the client's machine. Its old-style numerals are
why the hero figures look editorial rather than default. **Arial** stands in for
Instrument Sans (same neo-grotesque register, universally present).

### Grid

33.87 × 19.05cm. Edge margin **1.90cm**, inter-block gap **0.90cm** — one gap value
everywhere. Derived column widths, never hand-picked:

- 3-up: `(33.87 − 3.80 − 1.80) / 3 = 9.42cm` → x = 1.90, 12.22, 22.55
- 4-up: `(33.87 − 3.80 − 2.70) / 4 = 6.84cm` → x = 1.90, 9.64, 17.39, 25.13
- 2-up: `(33.87 − 3.80 − 1.27) / 2 = 14.40cm` → x = 1.90, 17.57

Vertical rhythm: eyebrow y=1.90 · title y=2.95 · **gold rule y=5.70** · content
6.60→16.30 · footrule y=17.05 · footer y=17.35.

### Motif

**A gold hairline with a travelling dot at its end.** The rule changes length and
position on every slide; the dot always rides its right terminus. Nothing else in the
deck is allowed to use gold as a line. This is the single element carried to all 16
slides, and it is what the Morph transition actually animates.

---

## Section 2 — Outline

**Overall conclusion:** TaxWise can run a company's entire Singapore and India finance
function — books, filings, payroll, transactions — from an in-house team of 30+, at
roughly half the cost of resourcing it locally.

```
S1  [cover]     TaxWise Consultants — Singapore Practice
S2  [evidence]  The practice today — Bangalore and Chennai, by the numbers
S3  [pillars]   Three practices, one finance function                    ★key
S4  [divider]   01 · Why Singapore
S5  [pillars]   The Singapore opportunity — gateway, rule of law, investor-readable
S6  [statement] The cost of compliance — a local hire is a fixed cost
S7  [divider]   02 · Where TaxWise comes in
S8  [flow]      The compliance stack — bookkeeping → GST → income tax → ACRA   ★key
S9  [metric]    Roughly half the cost                                    ★key
S10 [divider]   03 · Across the corridor
S11 [flow]      The India–Singapore corridor — set up, operate, repatriate
S12 [pillars]   Beyond compliance — M&A, valuation, payroll
S13 [pillars]   The team behind the work — 30+, all in-house
S14 [pillars]   Technology we build ourselves
S15 [profile]   The partners — HK Vinay, Shabari, Akshay, Vagdev
S16 [cta]       Next steps
```

Title grammar is **noun phrases throughout** — no mixed imperatives. Reading only the
titles gives the argument.

---

## Section 3 — Page briefs

**S2 [evidence]** — Objective: establish that this is an established practice, not a
new venture. Four figures from the firm's own site: 10+ years, 500+ clients, 30+
in-house, 50 Cr+ rupees in tax saved. Hierarchy: figure (44pt) → sublabel (12pt).
Transition: S1 names the firm, S2 proves it exists at scale.

**S3 [pillars] ★** — The three practices as published on twchartered.com: Core CA
Practice (statutory audit, direct tax, GST, ROC, assessments), CFO Advisory
(management reporting, working-capital control, budgeting, internal controls, board
packs), Startup & Transaction Advisory (incorporation, ESOP structuring, Rule 11UA
valuations, due diligence, fundraise support — published as **Startup Advisory**, which
is also what fits the column; the longer "Startup & Transaction Advisory" wrapped to
three lines and overran its body). Transition: S2 says how big, S3 says what we actually
do.

All three cards on every grid slide use a **fixed two-line head slot**, so their bodies
share one baseline whatever the head length. Without it, "Valuation" (one line) and
"Mergers & acquisitions" (two) started their bodies at different heights.

**S5 [pillars]** — Three *qualitative* arguments only: Singapore as holding layer not
end market; regulatory predictability and treaty network; investor-readability of a
Singapore holdco. **No market statistics are asserted anywhere in this deck** — the
client said they would supply their own research. S5 is built as a 3-up with the
content zone ending at y=15.6, which leaves a clean band at y≈16.0 for a stat row to
be dropped in later without touching the layout.

**S6 [statement]** — Three costs, no numbers: a local hire is a fixed cost (senior
Singapore salary before CPF, software, audit support); a full-time CFO is not a hiring
decision at this stage; statutory obligations do not scale down with headcount.
Transition: S5 says Singapore is worth doing, S6 says doing it properly is expensive.

**S8 [flow] ★** — Four connected steps with triangle arrowheads: Bookkeeping &
accounting → GST (registration, quarterly F5, input-tax review) → Income tax (ECI,
Form C-S / Form C, cross-border withholding) → ACRA (Annual Return, XBRL financial
statements, registers and resolutions). Every regime name is real and checkable; no
rates or deadlines are stated, so the slide does not age.

**S9 [metric] ★** — One figure, `50%`, at 150pt in gold-lit. The supporting argument is
that the saving is structural, not a discount: preparation in Bangalore, sign-off by a
Singapore-qualified CA, no fixed headcount carried by the client. Three chips restate
it. **This is the client's own commercial claim and is presented as their positioning.**

**S11 [flow]** — Two poles joined by the corridor actor. India: SPICe+, PAN/TAN, GST
registration, FC-GPR, ROC compliance. Singapore: ACRA incorporation, resident director
and company secretary, bank account, GST registration. On the corridor itself:
repatriation, dividend and royalty flows, transfer pricing, FEMA on every leg; chips
for FEMA, ODI/FDI reporting, DTAA treaty relief.

**S12 [pillars]** — The client's own grouping: M&A (buy/sell-side structuring,
financial and tax due diligence, SPA schedules, completion accounts); Valuation (Rule
11UA and FEMA pricing, independent reports for rounds and transfers); Payroll (CPF,
IR8A, IR21 in Singapore; PF, ESI, professional tax, TDS in India).

**S13 [pillars]** — Four roles, all stated as in-house: Chartered Accountants (India),
a Singapore-qualified CA who signs off every Singapore filing, legal, company
secretarial. Closing band: 30+ people on one payroll, no sub-contracting.

**S14 [pillars]** — In-house engineering team; accounting-and-tax CRM built around a
practice calendar rather than a sales pipeline; custom finance software where a
client's process needs a tool that does not exist.

**S15 [profile]** — Four partners on the 4-up grid: HK Vinay (Managing Partner), then
Shabari, Akshay and Vagdev. Statement first, people second — the pull quote leads, a
hairline closes it, the partner row sits beneath, and a band carries the firm line.

Each card is **role + name + a gold tick, and nothing else**. HK Vinay's role and
qualification are published by the firm; the other three names arrived as first names
only, with no designation, qualification or practice focus given. "Partner" is inferred
from the slide this was asked for and is the only inference made — no surnames, no
"Chartered Accountant", and no practice assignment has been invented, which matters
because slide 13 advertises in-house legal and in-house engineering alongside the CAs,
so a partner here is not necessarily a CA. The card is sized for exactly three
elements, so there is no empty slot showing; adding a qualification line later means
growing the cards by one line.

**S16 [cta]** — Three steps: scoping call; written scope and fee before anything
starts; transition with the first close run alongside the outgoing provider. Full
contact block.

---

## Section 4 — Morph pair planning

### Cast

| Name                 | Class | Geometry                      | Lifecycle                                           |
| -------------------- | ----- | ----------------------------- | --------------------------------------------------- |
| `!!scene-rule-gold`  | scene | rect `C9A84C`, h=0.06cm       | All 16. Lead actor — changes x, y and **length**.    |
| `!!scene-dot`        | scene | ellipse `C9A84C`, ø0.26cm     | All 16. Pinned to the gold rule's right terminus.    |
| `!!scene-rule-navy`  | scene | rect `34476A`, w=0.05cm       | All 16. Vertical tick; changes x, y, height.         |
| `!!scene-wash`       | scene | roundRect `223250` @0.55      | All 16. The content panel; changes x, y, w, h.       |
| `!!scene-orb-gold`   | scene | ellipse, radial `1E2B45`→`0E1B2F` | All 16. Slow drift, changes ø.                  |
| `!!scene-orb-steel`  | scene | ellipse, radial `1B2740`→`0E1B2F` | All 16. Counter-drift.                          |
| `!!scene-footrule`   | scene | rect `34476A`, h=0.05cm       | S2–S16, **fixed** — brand constant, excluded from the motion quota. |
| `!!actor-corridor`   | actor | rect `C9A84C`, h=0.08cm       | Enters S10 short, extends across S11, **ghosted x=36cm on S12**. |

`!!scene-*` and `!!actor-*` names do not collide.

**Two notes on the cast, from what the render showed.** The orbs were first built
as flat gold and slate at 7–10% opacity; they rendered as hard-edged discs that read
as a defect rather than as depth. They are now radial gradients whose outer stop is
the exact slide ground, so they have no rim at all. They are also drawn **before**
`!!scene-wash` — in the first build they sat on top of it, which is why card 1 and
row 1 rendered lighter than their siblings.

`!!scene-rule-navy` sits in the right margin on most slides. It is allowed into the
body only where a slide has exactly **one** structural gap (9, 11, 13, 15), so it
reads as a deliberate separator; on three-up slides it would otherwise rule the gap
between cards 1 and 2 and leave the gap between 2 and 3 open.

### Pairs

| Pair | Slide A | Slide B | What moves | Ghost on B |
| ---- | ------- | ------- | ---------- | ---------- |
| 1→2 | Rule short + centred under the wordmark (5.8cm @ y=11.4); wash is a full-bleed bottom band | Rule snaps to **full bleed** across the top (30.07cm @ y=5.70); wash lifts into the stats band | rule (+24.3cm & up 5.7cm), dot, navy tick, wash, both orbs | — |
| 2→3 | Rule full bleed; wash 30.07cm wide | Rule retracts to 12.0cm; wash collapses to the first card column (9.42cm) | rule (−18cm), dot, navy tick drops between cards 1–2, wash, orbs cross sides | — |
| 3→4 | Content composition | Divider: rule drops to y=13.2 and re-extends to 18cm; wash becomes a top band | rule (down 7.5cm, +6cm), dot, navy tick to left margin, wash, orbs | — |
| 4→5 | Divider | Rule returns full bleed to y=5.70; wash becomes card 1 | rule, dot, navy tick, wash, orbs | — |
| 5→6 | 3-up | Rule retracts to 9.0cm; orbs swap hemispheres | rule (−21cm), dot, navy tick to right margin, wash, orbs | — |
| 6→7 | Content | Divider 02; rule to y=13.2 @ 24cm | rule, dot, navy tick, wash, orbs | — |
| 7→8 | Divider | Full bleed; wash shrinks to the first step chip (6.84cm) | rule, dot, navy tick to the baseline, wash, orbs | — |
| 8→9 | Four-step stack | Rule halves to 14.4cm; **wash grows into the hero panel** (14.4 × 9.0) | rule, dot, navy tick, wash (+7.56cm w, +1.4cm h), orbs | — |
| 9→10 | Hero figure | Divider 03; **`!!actor-corridor` enters** at 8cm | rule, dot, navy tick, wash, orbs, corridor (enter) | — |
| 10→11 | Corridor bar short, centred | **Corridor extends to 26cm** and becomes the India–Singapore axis | corridor (+18cm), rule, dot, navy tick, wash, orbs | — |
| 11→12 | Corridor visible at y=13.30 | Corridor **ghosts to x=36cm** — slides off the right edge | corridor (exit), rule, dot, navy tick, wash, orbs | `!!actor-corridor` → x=36cm |
| 12→13 | 3-up | Wash widens to 14.4cm | rule, dot, navy tick, wash, orbs | — |
| 13→14 | 2-up | Rule retracts to 16cm; wash narrows | rule, dot, navy tick, wash, orbs | — |
| 14→15 | 3-up | Full bleed; wash drops to the first partner card (6.84 × 3.70 at y=10.20) | rule, dot, navy tick, wash, orbs | — |
| 15→16 | Profile | Rule retracts 30.07 → 20.0cm, holding the deck's rule line | rule, dot, navy tick, wash, orbs | — |

Every pair moves **five to seven** named shapes, against a Gate 5b-morph-2 floor of
three; the measured minimum across all fifteen pairs is five (pair 5→6, where the wash
is deliberately identical because slides 5 and 6 share the same three-up card geometry).

Slide 16's rule was originally planned to drop low and mirror the cover. In the render
that left a hole under the title, so it now holds the deck's rule line at y=5.70 and
retracts in length instead; a static hairline separates the contact block.

### Why per-slide text is not ghosted

`#sN-*` content shapes are added fresh per slide and are deliberately left unpaired, so
Morph cross-fades them. Ghosting all ~90 of them to `x=36cm` would roughly double the
shape count, trip the helper's >50-ghost rejection, and — the real reason — flinging
headlines across the screen is the opposite of the register this deck is in. The
geometry carries the motion; the words cross-fade. The only explicitly ghosted shape in
the deck is `!!actor-corridor`, which genuinely needs a visible exit.

---

## Section 5 — Claims register

Facts taken from the firm's own published material (`index.html`, twchartered.com):
office address, both phone numbers, both email addresses, 10+ years, 500+ clients,
50 Cr+ in tax saved, 100% compliance record, the three practice lines, HK Vinay as
Managing Partner.

Claims supplied by the client in the brief and reproduced as their positioning:
**Chennai as a second location** (it does not appear anywhere on the current site),
**30+ in-house team**, **a Singapore-qualified CA in-house**, **in-house legal and
company secretarial**, **an in-house technology team**, and **~50% below local market
cost**. These are the firm's to substantiate.

Nothing in this deck asserts a Singapore market statistic. Every regulatory reference
— ACRA Annual Return and XBRL, GST Form F5, ECI, Form C-S / Form C, CPF, IR8A, IR21,
SPICe+, FC-GPR, FEMA, ODI, DTAA, Rule 11UA, PF, ESI, professional tax, TDS — is a real
named obligation. No rates and no filing deadlines are printed, so the deck does not go
stale when thresholds move.

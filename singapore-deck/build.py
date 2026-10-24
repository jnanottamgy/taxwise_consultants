#!/usr/bin/env python3
"""
TaxWise Consultants — Singapore Practice.
Re-runnable build for taxwise-singapore.pptx.

Design record, cast list and the full morph pair table live in brief.md.
Run:  python3 build.py

Every text box is sized by `need()` rather than by eye.  The model below is
officecli's own, reverse-engineered from `view issues` and exact to the point:

    line height = pt * 1.2 * lineSpacing
    usable      = box height - 7.2pt of internal inset  (we set margin=0)
    chars/line  = 0.80 * width / (0.5em)

`txt()` asserts the fit at build time, so a copy edit that no longer fits
fails the build instead of shipping a clipped slide.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(HERE, "taxwise-singapore.pptx")
LOGO = os.path.join(HERE, "logo-reversed.png")

# ---------------------------------------------------------------- palette
# Lifted verbatim from src/app/globals.css on the live site.
INK      = "0E1B2F"   # slide ground
INK2     = "223250"   # raised panels
INK3     = "34476A"   # hairlines
SLATE    = "536B94"   # decorative orbs only — fails AA as text
MIST     = "8A9BBF"   # body copy            6.19:1 on ink
PAPER    = "F5F4F2"   # headlines           15.66:1 on ink
GOLD     = "C9A84C"   # eyebrows, rules      7.56:1 on ink
GOLD_LIT = "E8C97A"   # the one hero figure 10.75:1 on ink

DISPLAY = "Georgia"   # the site's own --font-display fallback
BODY    = "Arial"

# ------------------------------------------------------------------ grid
W, H  = 33.87, 19.05
M     = 1.90                                   # edge margin
GAP   = 0.90                                   # the single inter-block gap
COL3  = (W - 2 * M - 2 * GAP) / 3              # 9.4233
COL4  = (W - 2 * M - 3 * GAP) / 4              # 6.8425
COL2  = (W - 2 * M - 1.27) / 2                 # 14.40
X3    = [M + i * (COL3 + GAP) for i in range(3)]
X4    = [M + i * (COL4 + GAP) for i in range(4)]
X2    = [M, M + COL2 + 1.27]
PAD   = 0.70                                   # text inset inside a panel
TW3   = COL3 - 2 * PAD                         # 8.02 — 3-up text width
TW2   = COL2 - 2 * PAD                         # 13.00 — 2-up text width

Y_EYE, Y_TITLE, Y_RULE = 1.90, 2.95, 5.70
Y_FOOTRULE, Y_FOOT = 17.05, 17.35
PT = 28.3465                                   # points per cm

WARNINGS = []


# ------------------------------------------------------- text metrics
def lines_of(text, w, pt, font=BODY, bold=False, spacing=0.0):
    em = 0.54 if font == DISPLAY else 0.50     # Georgia runs wider than Arial
    if bold:
        em *= 1.05                             # bold adds ~5% advance
    char = pt * 0.0352778 * em + spacing / PT   # letterspacing is real width
    cpl = max(1, int((w / char) * 0.80))       # 0.80 word-wrap efficiency
    out = 0
    for p in text.split("\n"):
        # Only apply the raggedness factor to text that actually wraps.
        out += 1 if len(p) * char <= w else max(1, -(-len(p) // cpl))
    return out


def need(text, w, pt, ls=1.0, font=BODY, bold=False, spacing=0.0):
    return lines_of(text, w, pt, font, bold, spacing) * pt * 1.2 * ls / PT


# ------------------------------------------------------------ cli plumbing
def cli(*args):
    r = subprocess.run(["officecli", *[str(a) for a in args]],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FAILED: officecli %s\n%s%s" % (" ".join(map(str, args)), r.stdout, r.stderr))
    if "UNSUPPORTED" in r.stdout or "UNSUPPORTED" in r.stderr:
        sys.exit("UNSUPPORTED prop: officecli %s\n%s" % (" ".join(map(str, args)), r.stdout))
    return r.stdout


def batch(ops):
    for i in range(0, len(ops), 10):           # officecli caps batch at 12
        r = subprocess.run(["officecli", "batch", FILE],
                           input=json.dumps(ops[i:i + 10]), capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("BATCH FAILED:\n%s%s" % (r.stdout, r.stderr))


def cm(v):
    return "%.2fcm" % v


def op(slide, **props):
    return {"command": "add", "parent": "/slide[%d]" % slide,
            "type": "shape", "props": {k: str(v) for k, v in props.items()}}


# ----------------------------------------------------------- text atoms
def txt(n, tag, text, x, y, w, h, pt=18, color=MIST, font=None, ls=1.0,
        align="left", bold=False, valign="top", spacing=None, fill="none",
        preset=None, line="none"):
    """One text shape, fit-checked. margin=0 so the box means what it says."""
    req = need(text, w, pt, ls, font or BODY, bold, spacing or 0.0)
    if req > h + 0.005:
        WARNINGS.append("s%-2d %-12s %4.1fpt needs %.2fcm, got %.2fcm  (%d lines) :: %s"
                        % (n, tag, pt, req, h,
                           lines_of(text, w, pt, font or BODY, bold, spacing or 0.0),
                           text[:46]))
    p = dict(name="#s%d-%s" % (n, tag), text=text, x=cm(x), y=cm(y), w=cm(w), h=cm(h),
             font=font or BODY, size=pt, color=color, align=align, valign=valign,
             fill=fill, line=line, margin="0cm")
    if ls != 1.0:
        p["lineSpacing"] = str(ls)
    if bold:
        p["bold"] = "true"
    if spacing is not None:
        p["spacing"] = spacing
    if preset:
        p["preset"] = preset
    return op(n, **p)


def eyebrow(n, tag, text, x=M, y=Y_EYE, w=None, color=GOLD, pt=10.5, align="left"):
    return txt(n, "eye-" + tag, text.upper(), x, y, w if w else W - 2 * M, 0.70,
               pt=pt, color=color, bold=True, spacing=2.2, align=align, valign="middle")


def title(n, text, pt=40, y=Y_TITLE, h=2.40, x=M, w=None):
    return txt(n, "title", text, x, y, w if w else W - 2 * M, h,
               pt=pt, color=PAPER, font=DISPLAY, bold=True, valign="middle")


def panel(n, tag, x, y, w, h, fill=INK2, opacity=0.55):
    return op(n, name="#s%d-%s" % (n, tag), preset="roundRect", fill=fill,
              opacity=opacity, line="none", adj="adj:val 4000",
              x=cm(x), y=cm(y), w=cm(w), h=cm(h))


def hairline(n, tag, x, y, w, color=INK3, h=0.05):
    return op(n, name="#s%d-%s" % (n, tag), preset="rect", fill=color,
              line="none", x=cm(x), y=cm(y), w=cm(w), h=cm(h))


# ---------------------------------------------------------------- the cast
# Six shapes move on every pair; the footrule is a brand constant and is
# excluded from the Gate 5b-morph-2 motion quota.  These coordinates ARE the
# choreography — see brief.md §4.
#        rule (x, y, w)          navy (x, y, h)        orb-gold (x,y,d)      orb-steel (x,y,d)     wash (x, y, w, h)
SCENE = {
 1:  ((14.00, 11.40,  5.80), (31.97, 12.20, 3.60), (20.50, 1.20, 13.00), ( 4.00,  8.50,  9.50), ( 0.00, 13.60, 33.87, 5.45)),
 2:  (( 1.90,  5.70, 30.07), (31.97,  2.40,10.00), (24.00, 9.50,  9.00), ( 2.20,  9.00,  8.00), ( 1.90, 12.60, 30.07, 3.90)),
 3:  (( 1.90,  5.70, 12.00), (31.97,  6.90, 8.40), ( 2.40, 8.00, 10.50), (22.50,  1.50,  9.50), ( 1.90,  6.80,  9.42, 9.00)),
 4:  (( 1.90, 13.20, 18.00), (31.97,  3.00, 8.00), (19.00, 2.00, 13.00), ( 3.00,  9.00,  8.50), ( 0.00,  0.00, 33.87, 2.60)),
 5:  (( 1.90,  5.70, 30.07), (31.97,  7.60, 7.60), (25.00, 1.00,  8.50), ( 1.60, 10.00,  8.00), ( 1.90,  6.80,  9.42, 9.00)),
 6:  (( 1.90,  5.70,  9.00), (31.97,  6.90, 8.40), ( 1.50, 6.00, 12.00), (21.00,  8.00, 10.50), ( 1.90,  6.80,  9.42, 9.00)),
 7:  (( 1.90, 13.20, 24.00), (31.97,  3.00, 8.00), (20.50, 5.00, 12.50), ( 3.50,  1.50,  9.00), ( 0.00,  0.00, 33.87, 2.60)),
 8:  (( 1.90,  5.70, 30.07), (31.97, 15.95, 0.90), (23.50, 0.80,  9.50), ( 1.70,  9.50,  8.50), ( 1.90,  6.80, 30.07, 1.91)),
 9:  (( 1.90,  5.70, 14.40), (16.40,  6.90, 8.40), (18.00, 4.50, 14.00), ( 2.00,  2.00,  9.00), ( 1.90,  6.80, 14.40, 9.00)),
 10: (( 1.90, 13.20, 12.00), (31.97,  3.00, 8.00), ( 2.00, 3.00, 13.00), (22.00,  8.00, 10.00), ( 0.00,  0.00, 33.87, 2.60)),
 11: (( 1.90,  5.70, 30.07), (16.93,  7.40, 1.40), (12.50, 1.00,  9.00), (24.50,  9.50,  8.50), ( 1.90,  6.70, 14.40, 5.70)),
 12: (( 1.90,  5.70, 22.00), (31.97,  6.40, 9.20), (24.00, 7.50,  9.50), ( 2.00,  2.50,  9.00), ( 1.90,  6.80,  9.42, 9.00)),
 13: (( 1.90,  5.70, 30.07), (16.93,  6.80, 7.90), ( 1.80, 2.00, 11.00), (23.00,  8.50,  9.50), ( 1.90,  6.80, 14.40, 3.60)),
 14: (( 1.90,  5.70, 16.00), (31.97,  7.20, 8.00), (22.00, 2.50, 11.50), ( 2.50,  9.00,  9.00), ( 1.90,  6.80,  9.42, 9.00)),
 15: (( 1.90,  5.70, 30.07), (31.97,  6.40, 3.00), ( 3.00, 6.50, 12.00), (21.50,  2.00,  9.50), ( 1.90, 10.20,  6.84, 3.70)),
 16: (( 1.90,  5.70, 20.00), (31.97, 14.30, 2.00), (21.00, 1.50, 12.00), ( 3.00,  8.00,  9.50), ( 1.90,  6.80,  9.42, 6.20)),
}

DIVIDERS = {4, 7, 10}


def scene(n):
    """The six morph-paired shapes, plus the footrule on non-divider slides.

    Added first so every content shape stacks on top.  The gold dot always
    rides the right terminus of the gold rule — that pairing is the motif.
    """
    (rx, ry, rw), (nx, ny, nh), (gx, gy, gd), (sx, sy, sd), (wx, wy, ww, wh) = SCENE[n]
    ops = [
        # Radial stops land on the exact slide ground, so these read as depth
        # rather than as discs with a visible rim.
        op(n, name="!!scene-orb-gold", preset="ellipse", line="none",
           gradient="radial:1E2B45-" + INK + "-center",
           x=cm(gx), y=cm(gy), w=cm(gd), h=cm(gd)),
        op(n, name="!!scene-orb-steel", preset="ellipse", line="none",
           gradient="radial:1B2740-" + INK + "-center",
           x=cm(sx), y=cm(sy), w=cm(sd), h=cm(sd)),
        op(n, name="!!scene-wash", preset="roundRect", fill=INK2, opacity=0.55,
           line="none", adj="adj:val 4000", x=cm(wx), y=cm(wy), w=cm(ww), h=cm(wh)),
        op(n, name="!!scene-rule-navy", preset="rect", fill=INK3, line="none",
           x=cm(nx), y=cm(ny), w=cm(0.05), h=cm(nh)),
        op(n, name="!!scene-rule-gold", preset="rect", fill=GOLD, line="none",
           x=cm(rx), y=cm(ry), w=cm(rw), h=cm(0.06)),
        op(n, name="!!scene-dot", preset="ellipse", fill=GOLD, line="none",
           x=cm(rx + rw - 0.13), y=cm(ry - 0.10), w=cm(0.26), h=cm(0.26)),
    ]
    if n > 1 and n not in DIVIDERS:
        ops.append(op(n, name="!!scene-footrule", preset="rect", fill=INK3,
                      line="none", x=cm(M), y=cm(Y_FOOTRULE), w=cm(W - 2 * M), h=cm(0.05)))
    return ops


def footer(n):
    return [
        txt(n, "foot", "TaxWise Consultants  ·  Singapore Practice", M, Y_FOOT,
            20.0, 0.55, pt=10, spacing=1.4),
        txt(n, "pageno", "%02d" % n, W - M - 5.0, Y_FOOT, 5.0, 0.55,
            pt=10, align="right", spacing=1.4),
    ]


def card(n, i, label, head, body, x, y, w, h, headpt=21, bodypt=18):
    """Index + Georgia head + Arial body on a panel.

    Card 0 of every grid is !!scene-wash, already sitting at these bounds —
    that is how the morphing panel doubles as the first card on each slide.
    """
    tw = w - 2 * PAD
    ops = [] if i == 0 else [panel(n, "card%d" % i, x, y, w, h)]
    hh = 2 * headpt * 1.2 * 1.05 / PT + 0.03       # fixed two-line head slot
    bh = need(body, tw, bodypt, 1.15) + 0.04
    ops.append(eyebrow(n, "c%d" % i, label, x=x + PAD, y=y + 0.60, w=tw))
    ops.append(txt(n, "chead%d" % i, head, x + PAD, y + 1.55, tw, hh,
                   pt=headpt, color=PAPER, font=DISPLAY, bold=True, ls=1.05))
    ops.append(txt(n, "cbody%d" % i, body, x + PAD, y + 1.95 + hh, tw, bh,
                   pt=bodypt, ls=1.15))
    bottom = y + 1.95 + hh + bh
    if bottom > y + h - 0.25:
        WARNINGS.append("s%-2d card%d overruns panel: %.2f > %.2f"
                        % (n, i, bottom, y + h - 0.25))
    return ops


def divider(n, num, head, strap):
    return [
        txt(n, "topbar", "TAXWISE CONSULTANTS  ·  SINGAPORE PRACTICE", M, 0.95,
            24.00, 0.70, pt=10, spacing=2.0, valign="middle"),
        txt(n, "num", num, M, 5.20, 6.00, 4.30, pt=96, color=GOLD,
            font=DISPLAY, bold=True, valign="middle"),
        title(n, head, pt=52, y=9.90, h=2.60, w=28.00),
        txt(n, "strap", strap, M, 13.90, 26.00, 2.60, pt=20, ls=1.15),
    ]


def anim(n, name, effect, dur, trigger):
    cli("add", FILE, "/slide[%d]/shape[@name=%s]" % (n, name), "--type", "animation",
        "--prop", "effect=" + effect, "--prop", "class=entrance",
        "--prop", "duration=%d" % dur, "--prop", "trigger=" + trigger)


# =============================================================== the deck
def main():
    # Release any resident left over from a previous run before recreating.
    subprocess.run(["officecli", "close", FILE], capture_output=True, text=True)
    if os.path.exists(FILE):
        os.remove(FILE)
    cli("create", FILE, "--force")
    cli("open", FILE)
    for _ in range(16):
        cli("add", FILE, "/", "--type", "slide",
            "--prop", "layout=blank", "--prop", "background=" + INK)

    # ---------------------------------------------------------- 1 · cover
    batch(scene(1))
    lw, lh = 2.32, 2.60
    cli("add", FILE, "/slide[1]", "--type", "picture",
        "--prop", "src=" + LOGO, "--prop", "x=" + cm((W - lw) / 2),
        "--prop", "y=" + cm(3.30), "--prop", "width=" + cm(lw),
        "--prop", "height=" + cm(lh),
        "--prop", "alt=TaxWise Consultants shield mark, reversed in off-white")
    batch([
        eyebrow(1, "loc", "Bangalore · Chennai · Singapore", y=6.80, align="center"),
        title(1, "TaxWise Consultants", pt=58, y=7.70, h=3.00),
        txt(1, "strap",
            "Cross-border finance, tax and compliance for companies "
            "operating between India and Singapore.",
            4.94, 14.30, 24.00, 2.00, pt=20, ls=1.15, align="center"),
        txt(1, "meta", "SINGAPORE PRACTICE  ·  2026  ·  TWCHARTERED.COM",
            M, 16.60, W - 2 * M, 0.70, pt=11, align="center", spacing=1.8),
    ])
    cli("set", FILE, "/slide[1]/shape[@name=#s1-title]", "--prop", "align=center")

    # --------------------------------------------- 2 · the practice today
    batch(scene(2))
    batch([
        eyebrow(2, "sec", "The firm"),
        title(2, "The practice today"),
        txt(2, "lead",
            "TaxWise Consultants is a chartered accountancy and finance advisory "
            "firm headquartered in Bangalore, with a second office in Chennai. We "
            "are the finance and compliance function for companies that would "
            "rather not build one in-house.",
            M, 6.60, 18.80, 5.60, pt=19, ls=1.15),
        eyebrow(2, "office", "Registered office", x=21.50, y=6.60, w=10.47),
        txt(2, "addr", "307, 1st Floor, 14th Main Road, RMV Extension, "
                       "Sadhashivnagar, Bangalore 560 080",
            21.50, 7.45, 10.47, 2.45, pt=16, ls=1.15),
        hairline(2, "div", 21.50, 10.20, 10.47),
        eyebrow(2, "office2", "Second office", x=21.50, y=10.55, w=10.47),
        txt(2, "addr2", "Chennai", 21.50, 11.35, 10.47, 0.95, pt=16, ls=1.15),
    ])
    ops = []
    for i, (fig, sub) in enumerate([("10+", "Years in practice"),
                                    ("500+", "Clients advised"),
                                    ("30+", "In-house specialists"),
                                    ("50 Cr+", "Rupees saved in tax")]):
        kx, kw = X4[i] + PAD, COL4 - PAD
        ops.append(txt(2, "kpi%d" % i, fig, kx, 13.20, kw, 1.75, pt=40,
                       color=GOLD, font=DISPLAY, bold=True, valign="middle"))
        ops.append(txt(2, "kpisub%d" % i, sub, kx, 15.15, kw, 0.70, pt=12, spacing=0.8))
    batch(ops + footer(2))

    # ------------------------------------------------ 3 · three practices
    ops = [eyebrow(3, "sec", "What we do"), title(3, "Three practices, one finance function")]
    for i, (lab, head, b) in enumerate([
        ("01", "Core CA Practice",
         "Statutory audit, direct tax, GST and ROC filings. Assessments and representation."),
        ("02", "CFO Advisory",
         "Management reporting, working-capital control, budgeting, internal controls and board packs."),
        ("03", "Startup Advisory",
         "Incorporation, ESOP structuring, Rule 11UA valuations, due diligence and fundraise support."),
    ]):
        ops += card(3, i, lab, head, b, X3[i], 6.80, COL3, 9.00)
    batch(scene(3)); batch(ops + footer(3))

    # ------------------------------------------------------- 4 · divider
    batch(scene(4))
    batch(divider(4, "01", "Why Singapore",
                  "The regional holding seat for Asian operations — and the "
                  "jurisdiction our clients keep asking about."))

    # ------------------------------------- 5 · the Singapore opportunity
    ops = [eyebrow(5, "sec", "Section 01 · Why Singapore"), title(5, "The Singapore opportunity")]
    for i, (lab, head, b) in enumerate([
        ("01", "Gateway, not destination",
         "A Singapore entity is the holding layer above India, South-East Asia and the Gulf."),
        ("02", "Rule-of-law premium",
         "Predictable regulation, English-language filing and a deep tax-treaty network."),
        ("03", "Investor-readable structure",
         "Funds underwrite a Singapore holdco faster than a purely Indian cap table."),
    ]):
        ops += card(5, i, lab, head, b, X3[i], 6.80, COL3, 9.00)
    batch(scene(5)); batch(ops + footer(5))

    # ------------------------------------------ 6 · the cost of compliance
    ops = [eyebrow(6, "sec", "Section 01 · Why Singapore"), title(6, "The cost of compliance")]
    for i, (lab, head, b) in enumerate([
        ("01", "A local hire is a fixed cost",
         "Closing books, filing GST and signing ACRA returns commands a senior Singapore salary."),
        ("02", "A CFO is out of reach",
         "At this stage a full-time CFO is not a hiring decision. It is a decision to go without one."),
        ("03", "The work does not scale down",
         "Obligations are the same for a five-person entity as for a fifty-person one. So is the risk."),
    ]):
        ops += card(6, i, lab, head, b, X3[i], 6.80, COL3, 9.00)
    batch(scene(6)); batch(ops + footer(6))

    # ------------------------------------------------------- 7 · divider
    batch(scene(7))
    batch(divider(7, "02", "Where TaxWise comes in",
                  "We take the whole finance function — books, filings and the "
                  "CFO seat — and run it from India, for Singapore."))

    # ---------------------------------------------- 8 · the compliance stack
    batch(scene(8))
    ops = [eyebrow(8, "sec", "Section 02 · Where TaxWise comes in"),
           title(8, "The compliance stack")]
    row_h, pitch = 1.91, 2.36
    for i, (num, head, b) in enumerate([
        ("01", "Bookkeeping & accounting",
         "Day-to-day ledgers, reconciliations, management accounts and the year-end close."),
        ("02", "GST", "Registration, quarterly Form F5 returns and input-tax review."),
        ("03", "Income tax",
         "ECI, Form C-S or Form C, and withholding tax on cross-border payments."),
        ("04", "ACRA",
         "Annual Return, XBRL financial statements, statutory registers and resolutions."),
    ]):
        ry = 6.80 + i * pitch
        if i:                                   # row 0 is !!scene-wash
            ops.append(panel(8, "row%d" % i, M, ry, W - 2 * M, row_h))
        ops.append(op(8, name="#s8-chip%d" % i, preset="roundRect", fill="none",
                      line=GOLD + ":0.75", x=cm(2.50), y=cm(ry + 0.35),
                      w=cm(1.70), h=cm(1.20), text=num, font=BODY, size="12",
                      bold="true", color=GOLD, align="center", valign="middle"))
        ops.append(txt(8, "shead%d" % i, head, 4.90, ry, 8.00, row_h,
                       pt=20, color=PAPER, font=DISPLAY, bold=True, valign="middle"))
        ops.append(txt(8, "sbody%d" % i, b, 13.20, ry, 18.77, row_h,
                       pt=18, ls=1.15, valign="middle"))
    batch(ops)
    for i in range(3):                          # the flow, with arrowheads
        cli("add", FILE, "/slide[8]", "--type", "connector",
            "--prop", "from=/slide[8]/shape[@name=#s8-chip%d]" % i,
            "--prop", "to=/slide[8]/shape[@name=#s8-chip%d]" % (i + 1),
            "--prop", "shape=straight", "--prop", "color=" + GOLD,
            "--prop", "tailEnd=triangle")
    batch(footer(8))

    # ------------------------------------------- 9 · roughly half the cost
    batch(scene(9))
    ops = [
        eyebrow(9, "sec", "Section 02 · Where TaxWise comes in"),
        title(9, "Roughly half the cost"),
        eyebrow(9, "diff", "The difference", x=2.60, y=7.15, w=13.00),
        txt(9, "figure", "50%", 2.60, 7.95, 13.00, 6.40, pt=150,
            color=GOLD_LIT, font=DISPLAY, bold=True, valign="middle"),
        txt(9, "figsub", "Less than comparable local cost",
            2.60, 14.50, 13.00, 1.00, pt=18, ls=1.15),
        txt(9, "lead",
            "Prepared by our team in Bangalore, reviewed by a Singapore-qualified "
            "CA before filing. The difference is structural, not a discount.",
            X2[1], 6.80, COL2, 3.80, pt=19, ls=1.15),
    ]
    for i, t in enumerate(["Prepared in Bangalore by a 30-person team.",
                           "Reviewed and signed off by a Singapore CA.",
                           "No salary, CPF, software or recruitment cost."]):
        ry = 10.95 + i * 1.95
        ops.append(hairline(9, "dash%d" % i, X2[1], ry + 0.38, 0.90, color=GOLD, h=0.06))
        ops.append(txt(9, "chip%d" % i, t, X2[1] + 1.43, ry, COL2 - 1.43, 1.80,
                       pt=18, ls=1.15))
    batch(ops + footer(9))

    # ------------------------------------------------------ 10 · divider
    batch(scene(10))
    batch(divider(10, "03", "Across the corridor",
                  "Most of our clients are not choosing between India and "
                  "Singapore. They are operating in both.") +
          [op(10, name="!!actor-corridor", preset="rect", fill=GOLD, line="none",
              x=cm(12.94), y=cm(8.60), w=cm(8.00), h=cm(0.08))])

    # ------------------------------------- 11 · the India–Singapore corridor
    batch(scene(11))
    ops = [
        eyebrow(11, "sec", "Section 03 · Across the corridor"),
        title(11, "The India–Singapore corridor"),
        op(11, name="!!actor-corridor", preset="rect", fill=GOLD, line="none",
           x=cm(M), y=cm(13.30), w=cm(W - 2 * M), h=cm(0.08)),
        panel(11, "pole2", X2[1], 6.70, COL2, 5.70),
    ]
    for i, (tag, head, b) in enumerate([
        ("India", "Setting up in India",
         "SPICe+ incorporation, PAN and TAN, GST registration, FC-GPR and ROC compliance."),
        ("Singapore", "Setting up in Singapore",
         "ACRA incorporation, resident director, company secretary, bank account and GST."),
    ]):
        px = X2[i] + PAD
        ops.append(eyebrow(11, "pole%d" % i, tag, x=px, y=7.20, w=TW2))
        ops.append(txt(11, "phead%d" % i, head, px, 8.00, TW2, 0.95,
                       pt=20, color=PAPER, font=DISPLAY, bold=True))
        ops.append(txt(11, "pbody%d" % i, b, px, 9.10, TW2, 2.70, pt=18, ls=1.15))
    # Gold pills, ink text — they knock out the corridor rule where they sit.
    for i, lab in enumerate(["FEMA", "ODI & FDI", "DTAA relief"]):
        ops.append(txt(11, "tag%d" % i, lab.upper(), 5.50 + i * 9.34, 12.99, 4.20, 0.70,
                       pt=10.5, color=INK, bold=True, spacing=1.6, align="center",
                       valign="middle", fill=GOLD, preset="rect"))
    ops += [
        eyebrow(11, "cross", "Moving money between them", y=13.95, w=20.00),
        txt(11, "crossb",
            "Repatriation of funds, dividend and royalty flows, transfer-pricing "
            "documentation, and FEMA compliance on every leg.",
            M, 14.75, W - 2 * M, 1.80, pt=18, ls=1.15),
    ]
    batch(ops + footer(11))

    # -------------------------------------------- 12 · beyond compliance
    batch(scene(12))
    ops = [eyebrow(12, "sec", "Section 03 · Across the corridor"),
           title(12, "Beyond compliance"),
           # !!actor-corridor exits here — ghosted off the right edge so the
           # morph plays the slide-off rather than a silent fade.
           op(12, name="!!actor-corridor", preset="rect", fill=GOLD, line="none",
              x=cm(36.00), y=cm(13.30), w=cm(W - 2 * M), h=cm(0.08))]
    for i, (lab, head, b) in enumerate([
        ("01", "Mergers & acquisitions",
         "Buy-side and sell-side structuring, financial and tax due diligence, SPA schedules."),
        ("02", "Valuation",
         "Rule 11UA and FEMA pricing. Independent reports for funding rounds and transfers."),
        ("03", "Payroll",
         "CPF, IR8A and IR21 in Singapore; PF, ESI, professional tax and TDS in India."),
    ]):
        ops += card(12, i, lab, head, b, X3[i], 6.80, COL3, 9.00)
    batch(ops + footer(12))

    # ----------------------------------------------------- 13 · the team
    batch(scene(13))
    ops = [eyebrow(13, "sec", "The firm"), title(13, "The team behind the work")]
    for i, (head, b) in enumerate([
        ("Chartered Accountants, India",
         "In-house, on our own payroll. Audit, direct tax and GST."),
        ("Chartered Accountant, Singapore",
         "Reviews and signs off every Singapore filing."),
        ("Legal", "Agreements, SPAs and regulatory correspondence."),
        ("Company secretarial", "Registers, resolutions and board filings, both jurisdictions."),
    ]):
        cx, cy = X2[i % 2], 6.80 + (i // 2) * 4.30
        if i:                                   # cell 0 is !!scene-wash
            ops.append(panel(13, "cell%d" % i, cx, cy, COL2, 3.60))
        ops.append(eyebrow(13, "t%d" % i, "%02d" % (i + 1), x=cx + PAD, y=cy + 0.22, w=TW2))
        ops.append(txt(13, "thead%d" % i, head, cx + PAD, cy + 0.80, TW2, 0.84,
                       pt=19, color=PAPER, font=DISPLAY, bold=True))
        ops.append(txt(13, "tbody%d" % i, b, cx + PAD, cy + 1.76, TW2, 1.80, pt=18, ls=1.15))
    ops += [
        panel(13, "band", M, 15.40, W - 2 * M, 1.30),
        txt(13, "bandfig", "30+", 2.60, 15.40, 3.40, 1.30, pt=30, color=GOLD,
            font=DISPLAY, bold=True, valign="middle"),
        txt(13, "bandtxt", "people, all on one payroll. No sub-contracting.",
            6.20, 15.40, 25.17, 1.30, pt=18, ls=1.15, valign="middle"),
    ]
    batch(ops + footer(13))

    # ---------------------------------------------------- 14 · technology
    ops = [eyebrow(14, "sec", "The firm"), title(14, "Technology we build ourselves")]
    for i, (lab, head, b) in enumerate([
        ("01", "In-house engineering team",
         "Software engineers on staff, working alongside the accountants."),
        ("02", "Accounting & tax CRM",
         "Systems built around deadlines, engagements, documents and filings."),
        ("03", "Custom finance software",
         "Where a finance process needs a tool that does not exist, we build it."),
    ]):
        ops += card(14, i, lab, head, b, X3[i], 6.80, COL3, 9.00)
    batch(scene(14)); batch(ops + footer(14))

    # -------------------------------------------------- 15 · the partners
    # Statement first, then the people: the pull quote leads, a hairline
    # closes it, and the four partners sit on the 4-up grid beneath.
    batch(scene(15))
    PW = COL4 - 2 * PAD
    ops = [
        eyebrow(15, "sec", "The firm"), title(15, "The partners"),
        txt(15, "pull",
            "Every engagement is scoped and reviewed by a partner, "
            "not handed to an account manager.",
            M, 6.40, 26.00, 2.50, pt=24, color=PAPER, font=DISPLAY, ls=1.15),
        hairline(15, "pdiv", M, 9.60, W - 2 * M),
    ]
    for i, (role, name) in enumerate([
        ("Managing partner", "HK Vinay"),
        ("Partner", "Shabari"),
        ("Partner", "Akshay"),
        ("Partner", "Vagdev"),
    ]):
        px = X4[i]
        if i:                                   # card 0 is !!scene-wash
            ops.append(panel(15, "pcard%d" % i, px, 10.20, COL4, 3.70))
        ops.append(eyebrow(15, "pr%d" % i, role, x=px + PAD, y=10.75, w=PW))
        ops.append(txt(15, "pname%d" % i, name, px + PAD, 11.55, PW, 1.40,
                       pt=26, color=PAPER, font=DISPLAY, bold=True))
        ops.append(hairline(15, "ptick%d" % i, px + PAD, 13.25, 1.40, color=GOLD, h=0.06))
    ops += [
        panel(15, "band", M, 14.90, W - 2 * M, 1.40),
        txt(15, "bandtxt",
            "Ten years in practice  ·  500+ clients advised  ·  Bangalore and Chennai",
            2.60, 14.90, 28.67, 1.40, pt=18, ls=1.15, valign="middle"),
    ]
    batch(ops + footer(15))

    # ---------------------------------------------------- 16 · next steps
    batch(scene(16))
    ops = [eyebrow(16, "sec", "Next"), title(16, "Next steps")]
    for i, (lab, head, b) in enumerate([
        ("01", "A scoping call", "Thirty minutes on your close calendar."),
        ("02", "Scope and fee in writing", "What we run, and what it costs."),
        ("03", "Transition", "We run the first close alongside yours."),
    ]):
        ops += card(16, i, lab, head, b, X3[i], 6.80, COL3, 6.20, headpt=20)
    ops.append(hairline(16, "ctdiv", M, 13.70, W - 2 * M))
    cx = [(M, 7.50), (10.20, 7.50), (18.60, 13.37)]
    for i, (lab, body_t) in enumerate([
        ("Offices", "Bangalore · Chennai"),
        ("Telephone", "+91 9590360434\n+91 9740540239"),
        ("Email", "cavinaykarlagere@twchartered.com\ntwchartered.com"),
    ]):
        ops.append(eyebrow(16, "ct%d" % i, lab, x=cx[i][0], y=14.15, w=cx[i][1]))
        ops.append(txt(16, "contact%d" % i, body_t, cx[i][0], 14.90, cx[i][1], 1.60,
                       pt=15, ls=1.15))
    batch(ops + footer(16))

    # ------------------------------------------------------------- notes
    for n, text in SPEAKER_NOTES.items():
        cli("add", FILE, "/slide[%d]" % n, "--type", "notes", "--prop", "text=" + text)

    # -------------------------------------------------------- animations
    # Quiet and purposeful: the title settles with the morph, one content
    # element follows it.  Slide 9's figure is the one deliberate accent.
    for n in range(1, 17):
        anim(n, "#s%d-title" % n, "fade", 400, "withPrevious")
    for n, tag, eff, dur in [
        (1, "#s1-strap", "fade", 500),   (2, "#s2-lead", "fade", 450),
        (3, "#s3-chead0", "fade", 450),  (5, "#s5-chead0", "fade", 450),
        (6, "#s6-chead0", "fade", 450),  (8, "#s8-shead0", "fade", 450),
        (9, "#s9-figure", "zoom", 550),  (11, "#s11-phead0", "fade", 450),
        (12, "#s12-chead0", "fade", 450), (13, "#s13-thead0", "fade", 450),
        (14, "#s14-chead0", "fade", 450), (15, "#s15-pull", "fade", 500),
        (16, "#s16-chead0", "fade", 450),
    ]:
        anim(n, tag, eff, dur, "afterPrevious")
    for n in (4, 7, 10):
        anim(n, "#s%d-num" % n, "fade", 500, "afterPrevious")

    # -------------------------------------------------------- transitions
    # Set LAST: transition=morph auto-prefixes every shape name on the slide
    # (M-1), so names stay clean while we are still addressing them.
    for n in range(2, 17):
        cli("set", FILE, "/slide[%d]" % n, "--prop", "transition=morph-slow")

    cli("save", FILE)
    if WARNINGS:
        print("\nFIT WARNINGS (%d):" % len(WARNINGS))
        for w in WARNINGS:
            print("  " + w)
    else:
        print("fit model: no warnings")
    print(cli("validate", FILE))


SPEAKER_NOTES = {
 2: "Open by establishing that this is an established practice, not a new venture. "
    "Ten years, 500 clients, 30 people in-house. Chennai is the second office. "
    "Do not rush the four figures — let them land before moving on.",
 3: "These are the three practice lines as published on the website. The point to "
    "land is that they are not separate products: one team does the recurring "
    "compliance, the management reporting and the transaction work.",
 4: "Pivot. Everything so far has been India. From here the deck is about Singapore.",
 5: "Three qualitative arguments only — there are deliberately no market statistics "
    "on this slide. Drop your own research in here if the audience expects numbers; "
    "the layout leaves a clean band below the cards for a stat row.",
 6: "This is the problem slide. Do not soften it. The cost of a local hire is fixed "
    "and it lands before any of the work gets done. Pause on the third point — "
    "obligations do not scale down, which is what catches smaller entities out.",
 7: "Pivot to the offer.",
 8: "Walk down the four steps in order. Every name on this slide is a real filing: "
    "Form F5 is the quarterly GST return, ECI is the estimated chargeable income "
    "filing, Form C-S or C is the corporate return, and ACRA takes the annual "
    "return plus XBRL accounts. Deliberately no rates or deadlines — those move.",
 9: "The commercial claim. Say plainly that the saving is structural: preparation "
    "happens in Bangalore, sign-off happens with a Singapore-qualified CA, and the "
    "client carries no headcount. Be ready to substantiate the 50 per cent figure "
    "if asked — have a worked comparison to hand.",
 10: "Pivot to the cross-border work, which is where most of the real engagement sits.",
 11: "Both poles, then the money movement between them. FEMA governs the India leg "
     "on every transaction. ODI covers Indian money going out, FC-GPR covers money "
     "coming in, and the India-Singapore treaty governs relief. If the prospect has "
     "an existing structure, this is the slide to go off-script on.",
 12: "The adjacent work, grouped as the client sees it. Valuation matters most to "
     "anyone raising or transferring shares — Rule 11UA and FEMA pricing both bite.",
 13: "The differentiator: all of this is in-house and on one payroll. No "
     "sub-contracting and no associate network means one point of accountability. "
     "The Singapore-qualified CA is the point to press with this audience.",
 14: "Unusual for a CA firm and worth dwelling on. Engineers on staff means the "
     "practice systems are built around a filing calendar rather than a sales "
     "pipeline, and it means we can build a client a tool when they need one.",
 15: "Partner-led, and say it plainly: the partner who scopes an engagement is the "
     "one who reviews it. Four partners, so a Singapore client is never waiting on "
     "one person's calendar. Hand over to whichever partner is in the room.",
 16: "Close on the three steps and leave the contact block up. The ask is a "
     "thirty-minute scoping call, nothing larger.",
}


if __name__ == "__main__":
    main()

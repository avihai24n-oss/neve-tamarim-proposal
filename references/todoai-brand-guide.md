---
name: todoai-proposal
description: Use this skill whenever Avihai or TodoAI Studio needs a price quote, proposal, or "הצעת מחיר" / "הצעה ללקוח" / "מסמך תמחור" — any outward-facing offer document for a client. Triggers on "תכין הצעת מחיר", "צור הצעה ל...", "מסמך תמחור", "proposal", "quote", "הצעה ב-PDF". Produces a clean, premium, print-to-PDF HTML proposal in the TodoAI design language (warm cream background, Heebo font, coral accent, sharp corners, hairline dividers, real TodoAI logo, signature). Always use this skill instead of guessing brand colors, fonts, logo, or links.
---

# TodoAI Proposal / Price-Quote Skill

Builds professional, premium, print-to-PDF HTML price proposals for TodoAI Studio. Editorial look inspired by Stripe / Linear / Notion: restraint over decoration, type hierarchy over colored boxes, lots of air. Same brand language as the TodoAI email template, adapted to an A4 proposal document the client can save as PDF.

## Output rules (non-negotiable)

1. **RTL** — `dir="rtl"` on `<html>` and `<body>`.
2. **Single self-contained HTML file** — one file, no external CSS/JS except the Heebo Google Font and the logo image.
3. **Print-to-PDF first** — include `@media print` (hide the print button, drop page border), and `-webkit-print-color-adjust:exact` so the cream background + coral survive the PDF export. Add a coral "שמור כ-PDF / הדפס" button (`onclick="window.print()"`) that is hidden in print.
4. **No em-dashes (—) ever.** Use a comma, a period, or rephrase. Hard brand rule.
5. **Heebo font** for everything: `'Heebo',-apple-system,'Segoe UI',Arial,sans-serif`.
6. **Light, elegant, official** — warm cream page background, white document card, generous whitespace (≥48px side padding on the card).
7. **Real TodoAI logo** at the top (icon + "TodoAI" wordmark). URL below.
8. **Always include the signature block** (name, title, links) near the end.
9. **Numbers in the proposal body use digits** (₪2,750), not spelled out. Prices are the focal point.

## Design system (identical palette to the email skill)

```
--ink:    #16151A   /* headlines, primary text, feature items */
--body:   #54524C   /* body copy, lead paragraph */
--muted:  #A09E98   /* labels, captions, descriptions, footer */
--faint:  #C4C2BC   /* copyright, strike-through lines */
--coral:  #F2542D   /* THE accent: prices, eyebrows, tags, links, checkmarks */
--bg:     #F4F4F2   /* page background (warm cream) */
--card:   #FFFFFF   /* the document */
--border: #E5E4E0   /* outer card border */
--rule:   #ECEBE7   /* hairline dividers + column separators */
```

Type scale (Heebo):
| Element | Size | Weight |
|---|---|---|
| Page headline | 30px | 800 |
| Section / offer title | 21px | 800 |
| Price (main) | 28px | 900 |
| Price (retainer) | 20px | 900, coral |
| Lead paragraph | 16px | 400 |
| Feature item | 14.5px | 400-500, ink |
| Eyebrow / tag | 12px | 700, letter-spacing 1.5-2px, coral |
| Footer | 11px | 400, faint |

Shape & layout language:
- **Sharp corners.** Card and buttons: `border-radius:4px`. Logo icon: 9px. Never pill-shaped, never 12-16px rounded.
- **No floating gray cards.** Separate offers/sections with 1px hairline dividers or thin column separators (`border-left:1px solid #ECEBE7`), not background fills. A single very-faint `#FBFBFA` fill is allowed for one side of a comparison.
- **Checkmarks are coral `✓`**; "plus / extra" items use coral `+`.
- **No big hero emoji, no gradient bars.** Keep the chrome quiet and editorial.

## The logo

Same icon as the email skill, served from Avihai's GitHub Pages (HTML cannot reliably embed local images for PDF/print):

```html
<div class="logo">
  <img src="https://avihai24n-oss.github.io/webinar/assets/todoai-icon.png"
       width="38" height="38" alt="TodoAI" style="border-radius:9px; display:block;">
  <span class="wm">TodoAI</span>
</div>
```

## Canonical details (pull from here, do not guess)

- **App link:** https://app.todowith.ai/
- **Marketing site:** https://todowith.ai/
- **WhatsApp 1:1:** https://wa.me/972542064301
- **Instagram:** https://instagram.com/todoai.il
- **Signature name:** אביחי אלנקווה
- **Signature title:** Co-Founder & AI Lead, TodoAI Studio
- **Validity line:** "ההצעה בתוקף ל-14 יום"
- **Copyright:** © 2026 TodoAI Studio

## Anatomy of a TodoAI proposal

```
1. Print button (coral, hidden in print)
2. Document card (white on cream)
3. Header: logo lockup (icon + TodoAI)
4. Hairline rule
5. Eyebrow ("הצעת מחיר", coral, spaced)
6. Headline (Heebo 800, 1-2 lines)
7. Lead paragraph (one sentence, what it does)
8. Flow row (quiet text steps separated by coral ← arrows) — optional
9. Hairline rule
10. Offers: 1-3 columns separated by hairline. Each = tag, title, 1-line desc,
    price rows (הקמה + ריטיינר), minirule, feature list (coral ✓).
    Mark the recommended one with "· מומלץ" on its tag.
11. Costs / value section (eyebrow + paragraph). Optional comparison table:
    "אצלנו" (coral price) vs the alternative (struck-through muted price).
12. Signature (name, title, coral text links)
13. Footer (© + validity)
```

## Process

1. Gather: product name, one-line pitch, the flow steps (optional), each offer
   (name, 1-line desc, setup price, monthly retainer, feature bullets), any
   usage/credit note, and an optional value comparison.
2. Copy `references/template.html` and fill it. Keep ALL chrome (logo, palette,
   signature, footer, print button, @media print) intact.
3. Verify: no em-dashes anywhere, logo URL correct, signature present, print
   button present, `-webkit-print-color-adjust:exact` present.
4. Save to the project's `proposals/` folder (create it if missing) as a single
   `.html` file, then `open` it so the user sees it.
5. Tell the user: click "שמור כ-PDF / הדפס" → "Save as PDF" for the final PDF.

## Reference

`references/template.html` is a complete, tested proposal (the avatar-video
quote) to copy from. It demonstrates: 2-offer grid with a recommended tag,
price rows, coral feature checkmarks, and a side-by-side value comparison
(our price vs a struck-through alternative). Reuse its `<style>` block verbatim;
only the content between the header and signature changes per proposal.

# margin — design system

The single record of design decisions for this app. Read it before changing the UI.

## Direction
- Product: **margin**, interview and CV practice. Wordmark "margin" in Instrument Sans 600, -0.045em tracking, preceded by a 3 px red-pen bar.
- Feel: an editorial rehearsal room. Paper and ink, one red pen. Type does the work; colour is rare.
- Signature: the coach speaks in sans; **the user's own words always appear in Instrument Serif italic**, with a 2 px red-pen rule on the left. A four-step rail lights the current step with a red dot.
- Journeys: interview = Brief → Rehearse → Debrief → Next steps; CV = Brief → Your CV → Review → Next steps. Every flow ends in a dark "Next steps" block with copy and download.

## Tokens
| Token | Value | Use |
|---|---|---|
| --paper | #F4F1EA | page |
| --sheet | #FBFAF6 | cards (one step above paper) |
| --field | #EEEAE2 | inputs (inset, below paper) |
| --ink | #141414 | text, primary buttons, Next steps block |
| --graphite | #5E5A53 | secondary text (6:1 on paper) |
| --pencil | #8A847A | decoration and large text only |
| --faint | #B8B2A7 | upcoming steps, empty meter segments |
| --pen | #C2331B | marks, current step, errors, missing (4.9:1 on paper) |
| --rule / --rule-strong | ink at 10% / 20% | hairlines and rings |

- Accent rule: red pen only marks things (the user's words, the current step, problems). Never a fill for buttons.
- Depth: rings, not borders (`0 0 0 1px var(--rule)`); one soft lift on hover for path cards and focus on the composer.

## Type
- Instrument Sans 400/500/600; Instrument Serif italic for user words and the single emphasis word in the hero.
- Scale ratio 1.25 from 16 px: 13 · 14 · 16 · 20 · 25 · 31 · display clamp(40–68 px).
- Display and titles: 600, tracking -0.035 to -0.045em. Kickers: 13 px 600 uppercase +0.08em.
- Scores: tabular numbers; big score 72–120 px 600 -0.06em.

## Spacing and shape
- Base 4/8 px. Content column 720 px; home 1040 px. Section gap 56 px; card padding 20×24 px.
- Radius: inputs 10 px, cards 16 px, Next steps 22 px, buttons and chips pill.
- Tap targets ≥ 44 px; inputs 16 px text (no iOS zoom).

## Components
- Button primary: ink pill, 48 px high, 0 24 px padding, 16 px/600, arrow nudges 3 px on hover, scale(.97) on press.
- Button secondary: transparent, ring rule-strong, ink text.
- Path card (home): sheet, ring, 24 px padding, title 25 px/600, meta "About N min", two-item list with red dashes, CTA at bottom.
- Transcript row: grid 96 px label column + text; interviewer 20 px/500 (older turns graphite), user serif italic 21 px.
- Meter: 5 segments 18 × 4 px; filled ink, red when score ≤ 2.
- Status narration: list of stages; done = graphite tick, now = ink 600 with red spinner, next = faint. Screen readers hear only the current stage.
- Job-fit status: met = solid ink dot, partly = half dot graphite, missing = red ring.

## Motion
- Screens: fade + 10 px rise, 420 ms, cubic-bezier(.23,1,.32,1).
- Lists: stagger 50 ms per item. Fit bar grows 900 ms once. Rail dot scales in 350 ms.
- Only transform and opacity animate. Everything collapses under prefers-reduced-motion.

## Copy
- Sentence case, verbs first, no "please", no exclamation marks. Errors say what happened, then what to do.
- Product voice: "Your debrief", "Before you send it", "Change these first".

# AI Image Prompting for Meta Ad Creatives (Nano Banana 2)

How to generate ad creatives via `scripts/generate_creative.py` — endpoint, prompt anatomy, hook patterns by goal, and ready-to-use templates tuned for AI courses / webinars / SaaS / lead-magnets aimed at Hebrew-speaking (Israeli) audiences.

Use this when the user asks to "create an ad image", "generate a creative", or describes a campaign that needs visuals. Read all of it before writing your first prompt — the anti-patterns section saves money.

## When to use this vs not

**Use Nano Banana 2 for:**
- Generating fresh ad creative from scratch (text → image)
- Re-styling an existing photo into ad format (image edit)
- A/B variants — same brief, 3-4 different aesthetic angles
- Founder/persona shots when you don't have professional photography

**Don't use it for:**
- Brand-precise logo work (use Figma/Canva)
- Long-form Hebrew paragraphs on the image — short headlines (2–6 Hebrew words) render reliably with `thinking_level: high`, but multi-line paragraph Hebrew is still error-prone. For long copy: generate with empty negative space and overlay in Figma/Canva.
- Product screenshots that must be pixel-accurate (use a real screenshot)
- Faces of real people you don't have rights to depict (legal + Meta policy)

## API endpoint and auth (cheat sheet)

- **Slug:** `fal-ai/nano-banana-2/edit` (v2; Gemini 3.1 Flash Image)
- **Auth header:** `Authorization: Key <KEY_ID>:<KEY_SECRET>` — exact format, space + colon
- **Env var:** `FAL_KEY` (already in user's `.env`)
- **Sync endpoint:** `POST https://fal.run/fal-ai/nano-banana-2/edit` — blocks until done; fine for small jobs (~20s)
- **Queue endpoint:** `POST https://queue.fal.run/fal-ai/nano-banana-2/edit` — recommended for production; returns `{request_id, status_url, response_url}`. Poll `status_url` until `COMPLETED`, then GET `response_url`.
- **Pricing:** $0.08 per image at 1K resolution. 0.5K=$0.06, 2K=$0.12, 4K=$0.16. `enable_web_search`=+$0.015. `thinking_level=high`=+$0.002.
- **Rate limits:** workspace-tier dependent; not published. Honor `Retry-After` on 429.
- **Output URLs:** hosted on `*.fal.media`. Persist for a while but not guaranteed permanent — download immediately and store locally.

The script `scripts/generate_creative.py` wraps all of this. Use the script unless you have a reason to call the API directly.

## Required input shape

Even the "edit" endpoint accepts only a prompt + at least one reference `image_urls[]`. For pure text-to-image, pass any neutral reference image (e.g., a blank canvas or a simple stock photo) — the model treats it as a starting hint but the prompt drives the result. Empty PNG works.

For genuine edits — restyle a founder photo, change background, etc. — pass the real source image URL (1-14 references supported).

## The 5 visual principles that win the auction

1. **Thumb-stop in <0.4 seconds** — one dominant subject, high contrast, story readable from a 4cm thumbnail.
2. **Faces beat objects, but specific faces beat generic faces** — direct eye contact + single emotion outperforms group shots and stock smiles by 1.4-2.1× CTR.
3. **Native-feeling beats polished** — lo-fi UGC / "founder iPhone selfie" aesthetic continues to beat agency-polished work for sub-$2k AOV info products.
4. **Text on image is back — but as design, not overlay** — mock-tweet, mock-DM, mock-headline, terminal output. Avoid centered three-color text.
5. **Aspect ratio is composition, not crop** — generate natively per placement: 1:1 Feed, 4:5 mobile Feed, 9:16 Reels/Stories.

## Aesthetic do's and don'ts (2026)

| Category | DO (premium / current) | DON'T (slop / 2022 AI) |
|---|---|---|
| Color | Editorial neutrals, warm office light, single accent (mustard, terracotta, deep teal) | Cyan-purple gradients, "neural network" blue glow |
| Subject | 30-45yo professional, slightly imperfect, mid-action | Hyper-smooth model, robot mascot, glowing brain, hooded hacker |
| Setting | Real desk, real laptop, real coffee cup, slight clutter | Holographic UI floating in dark void, server rack, "Matrix" code rain |
| UI shown | Realistic ChatGPT/Claude/Cursor screenshot, slight blur on non-focal text | Fake invented "AI dashboard" with fictional charts |
| Typography | One typeface, Helvetica/Inter/Söhne-style, left-aligned | Three fonts, drop shadows, neon outlines, "AI" in 3D chrome |
| Composition | Generous negative space top-left or bottom-right for headline | Subject dead-center filling 100% of frame |
| Photography | 35mm or 50mm look, natural window light, slight grain | Tilted Dutch angles, fisheye, lens flares, bokeh hearts |
| People (Israeli context) | Mediterranean skin tones, casual button-down or basic tee, no tie, Tel Aviv café or co-working backdrop | Suit-and-tie corporate stock, Western-suburban kitchen, blonde "founder" who reads as US generic |

## Prompt anatomy

Order matters. Nano Banana 2 / Gemini Image respond best to **descriptive sentences**, not comma-separated tag lists.

`[Shot type & subject] → [Subject's action & emotion] → [Environment & props] → [Lighting & time of day] → [Camera & lens] → [Aesthetic / film stock reference] → [Composition & negative space instruction] → [Aspect ratio]`

### Annotated example

```
A medium close-up portrait of a 38-year-old Israeli woman with shoulder-length 
dark wavy hair, wearing a simple cream linen shirt,                          ← subject
laughing softly while looking at her MacBook screen,                          ← action + emotion
seated at a sun-lit wooden desk in a Tel Aviv apartment, plants and a 
half-empty espresso cup beside her,                                           ← environment
warm late-afternoon side light from a window camera-left, soft shadows,       ← lighting
shot on a 50mm prime lens at f/2.0, slight film grain,                        ← camera
in the editorial style of Kinfolk magazine,                                   ← aesthetic
composition leaves the upper-right third empty for headline text,             ← negative space
4:5 vertical aspect ratio.                                                    ← AR
```

### Hebrew/Israeli direction tips

- Say **"Mediterranean / Levantine features"** or **"Israeli woman in her late 30s"** explicitly. Without it, the model defaults to North American whitewashed faces.
- **Hebrew text rendering works** for short headlines (2–6 words) — verified on Nano Banana 2 with `thinking_level: high`. To improve hit rate: quote the exact text with `'...'`, specify "right-to-left layout", specify the font family ("clean modern sans-serif"), and ask explicitly for "no other text". For longer paragraphs or precise typography, still prefer empty negative space + Figma/Canva overlay.
- Backdrops that read as Israeli without being touristy: **"Tel Aviv co-working space with exposed concrete and Bauhaus windows"**, **"Florentin neighborhood café"**, **"rooftop with Tel Aviv skyline at golden hour"**. **Avoid Jerusalem stone** — reads as tourism, not tech.

## Hook patterns by ad goal

### Webinar registration → Speaker authority + scarcity

The image must answer: *"who is teaching, why trust them in 0.4s?"* — best patterns:
- **Speaker mid-gesture** — founder caught mid-explanation, hands visible, looking off-camera as if mid-conversation. Reads as competent, not posed.
- **Mock event/Zoom grid** — speaker featured with subtle "Live" or scheduled-time indicator.
- **Behind-the-scenes** — speaker setting up a microphone or whiteboard. Signals "real event, not funnel."

### Course sale → Transformation / outcome

Show the **outcome state**, not the learning state. Buyers buy the destination, not the journey.
- **Before/after split** — messy spreadsheet on left, clean automated dashboard on right.
- **Outcome artifact** — finished AI-built app on a phone, published custom GPT, automation diagram.
- **Lifestyle proof** — persona doing the thing the course teaches, in a real environment. Not at a beach with a laptop (that's 2019 dropshipper).

### SaaS trial → Real product demo screenshot

Real screenshots win over rendered mockups in 2026. Product-screenshot ads with one annotation arrow outperformed lifestyle-product ads by ~30% CTR for B2B SaaS in 2025 (Foreplay reports).
- **Real UI, slight tilt** in a 3D mockup frame (or flat).
- **Hand-holding-phone** showing the app — re-introduces the face benefit.
- **Before/after of the workflow** the SaaS replaces.

### Lead magnet (PDF/template) → Visual of the resource

Show the **physicality of the digital asset**.
- **Tablet or phone mockup** displaying the first page of the PDF, tilted in a hand.
- **Stack-of-pages render** as if the PDF were printed and bound.
- **Founder holding the printed version** — surprisingly converts; signals "real."

## 9 copy-paste prompt templates

Each uses the anatomy above. Replace `{placeholders}` before generating. Append the negative-prompt clause at the bottom of every prompt.

### T1 — Webinar speaker authority (1:1 Feed, EN/global)

```
A medium portrait of a {persona_age}-year-old {gender}, mid-gesture explaining 
something with hands visible, looking slightly off-camera, wearing a simple 
charcoal crew-neck. Background is a softly out-of-focus modern office with a 
whiteboard showing faint diagrams about {course_topic}. Warm key light from 
camera-left, cool fill from a monitor camera-right. Shot on 50mm at f/2.2, 
subtle film grain. Editorial style of WIRED magazine portraiture. Leave the 
left third empty for headline overlay. 1:1 square aspect ratio.
```

### T2 — Course transformation before/after (4:5 Feed)

```
A clean side-by-side split-screen image. Left side: a cluttered laptop screen 
showing a chaotic Excel spreadsheet, dim overhead light, slightly desaturated. 
Right side: the same desk now showing a polished {outcome} dashboard built 
with AI, bright natural window light, vibrant. Both halves shot from the same 
overhead angle on a 35mm lens. Minimalist, no people. Style: Apple product 
photography. 4:5 vertical aspect ratio. Leave 15% top margin empty.
```

### T3 — SaaS product demo (1:1)

```
A realistic hand holding an iPhone 16 Pro at a slight 15-degree tilt, 
displaying the {product_name} app interface with a {key_feature} screen 
clearly visible. Background is a softly blurred warm-wood desk with a coffee 
cup. Single thin red annotation arrow points to the {key_feature} button. 
Natural side lighting, shot on 35mm at f/2.8. Style: Linear.app marketing 
photography. 1:1 aspect ratio.
```

### T4 — Lead magnet PDF reveal (4:5)

```
A flat-lay overhead shot of a printed {lead_magnet_title} document on a warm 
oak desk, slightly fanned pages, a pen and a small espresso cup beside it. 
Soft morning window light from the top of the frame. Shot on 50mm. 
Style: Kinfolk editorial flat-lay. Leave the bottom third empty for CTA 
overlay. 4:5 vertical aspect ratio.
```

### T5 — Israeli founder selfie aesthetic (9:16 Reels/Stories, HE audience) ✨

```
A natural iPhone-style front-camera selfie of a 35-year-old Israeli man with 
short dark hair and light stubble, Mediterranean features, wearing a simple 
olive t-shirt, mid-laugh while gesturing at his MacBook. He is sitting at a 
window seat in a Florentin Tel Aviv café, exposed brick and a hanging plant 
behind him. Late afternoon golden light. Slight motion blur, slightly 
imperfect focus, shot vertically on iPhone 15. The MacBook screen shows 
Hebrew text in a right-to-left layout. Lo-fi UGC aesthetic, no filters. 
9:16 vertical aspect ratio. Leave the top 20% empty for caption overlay.
```

### T6 — Israeli webinar / event poster (1:1, HE audience) ✨

```
A medium portrait of a 42-year-old Israeli woman with curly dark hair, 
Levantine features, wearing a black blazer over a white tee, arms crossed 
confidently, soft smile, looking directly at camera. Background is a 
slightly out-of-focus Tel Aviv rooftop at blue hour with the city skyline 
including the Azrieli towers visible. Cool ambient light, warm rim light 
from behind. Shot on 85mm at f/1.8. Style: Calcalist business-magazine 
portraiture. Leave the right third empty for Hebrew headline overlay 
(right-to-left). 1:1 aspect ratio.
```

### T7 — Mock-tweet / mock-DM social proof (1:1)

```
A photorealistic mockup of an iPhone screen showing a single tweet or 
WhatsApp message that reads "{testimonial_quote}" from "{persona_name}", 
displayed against a soft pastel {accent_color} background. The phone is 
held at a slight angle by a hand entering from the bottom-right. Soft 
studio lighting, shallow depth of field. Style: minimalist product 
photography. 1:1 aspect ratio. Leave 20% top margin empty.
```

### T8 — AI tool "screen + outcome" (4:5)

```
An overhead shot of a wooden desk: a MacBook on the left showing a 
{ai_tool_name} interface mid-prompt, a printed-out result of the AI's 
output on the right (a {output_artifact}), a coffee cup and notebook 
beside them. Warm morning window light from the top-left, shot on 35mm 
at f/4. Style: editorial tech-magazine flat-lay, like The Verge feature 
photography. 4:5 vertical aspect ratio.
```

### T9 — Israeli SaaS dashboard hero (1:1, HE) ✨

```
A clean 3D mockup of a MacBook Pro displaying the {product_name} dashboard 
with Hebrew UI text in right-to-left layout, key metrics visible. The 
laptop sits on a minimalist concrete desk with a single small succulent 
plant. Soft diffused daylight from camera-right. Style: Notion or Linear 
marketing site product hero. Background is warm off-white. Leave the left 
third empty for Hebrew headline. 1:1 aspect ratio.
```

## The negative-prompt clause (always append)

Nano Banana 2 doesn't have a separate `negative_prompt` field, but appending an exclusion clause meaningfully reduces failure modes:

```
Avoid: glowing blue neural network backgrounds, holographic UI floating in 
dark void, robot or android characters, glowing brain imagery, cyan-to-purple 
gradients, lens flares, "Matrix" code rain, hooded hacker silhouettes, 
overly smooth airbrushed skin, three-font typography, drop shadows on text, 
3D chrome lettering, stock-photo smiling, dead-center subject filling the 
whole frame, suit-and-tie corporate look. The image must feel editorial 
and real, not like AI stock art.
```

## Top 7 anti-patterns (skip these to save CPM)

1. **Generic AI-blue glow on a face** — instantly reads as 2022 AI startup. CPM penalty via quality classifier.
2. **Robot or android mascot** — kills trust for paid info products; works only for genuine robotics SaaS.
3. **"AI brain" stock illustration** — Meta's quality model has been observed flagging these as low-quality.
4. **Three-line text overlay covering >40% of image** — still triggers reduced delivery despite the official 20% rule being retired.
5. **Centered-symmetric composition with subject filling the frame** — leaves no room for the headline, forces overlay on the face.
6. **Western blonde "founder" for Hebrew-targeted ads** — fails cultural-relevance signal; Israeli viewers scroll past in <0.2s.
7. **Hyper-real CGI with perfect skin** — reads as fake. Slight imperfection (a stray hair, a mug in frame) raises perceived authenticity and CTR.

## Workflow: from brief to running ad

1. **Brief** — User describes audience, offer, hook angle. Pick one of the 4 hook patterns by goal.
2. **Pick template** — match by goal × audience × placement (T1-T9).
3. **Fill placeholders** — be specific. "AI for accountants" beats "AI for professionals".
4. **Append negative clause** — always.
5. **Generate 3-4 variants** — same prompt, different `seed`. Cost: 4×$0.08 = $0.32 to get options.
6. **Show user, pick winner** — don't auto-pick. Aesthetic judgment is theirs.
7. **Overlay Hebrew copy in Figma/Canva** — never bake Hebrew into the AI generation.
8. **Upload to Meta** as the `image_path` in `create_campaign.py` spec, or upload manually via Ads Manager.
9. **Track performance** — after 48-72h running, use `creative_fatigue.py` to see which variant won.

## Iteration playbook (when the first batch doesn't land)

If the user rejects all 4 variants, diagnose before regenerating:

- **"Looks too AI"** → Drop "shot on 50mm" specificity, add "amateur iPhone selfie", add stronger negative prompt clauses.
- **"Doesn't look Israeli"** → Add explicit Mediterranean/Levantine descriptors + Tel Aviv backdrop. Drop "professional" — the model maps that to LinkedIn-stock.
- **"Subject is too perfect"** → Add: "slight wrinkles, casual posture, hair slightly out of place, candid expression."
- **"No room for the headline"** → Replace the negative-space line with: "the bottom 35% of the image is plain warm beige with no objects."
- **"Doesn't match brand"** → Add the brand's primary color + a reference brand: "in the visual style of {brand the user trusts}".

## Cost budgeting (rough)

For a typical 3-creative A/B test:
- 9 generations (3 angles × 3 variants each) at 1K = **$0.72**
- Add web search context (+$0.015 each) = **$0.86**
- Add high-thinking variants for quality push (+$0.002 each) = **$0.88**

Round to **~$1 per A/B campaign creative pack**. Cheap relative to the $20-50 ad spend per day per ad set those creatives will drive.

## References

- fal.ai Nano Banana 2 model page: https://fal.ai/models/fal-ai/nano-banana-2/edit
- fal.ai docs: https://docs.fal.ai/
- Google Gemini Image guide: https://ai.google.dev/gemini-api/docs/image-generation
- Meta Creative Center (current best practices): https://www.facebook.com/business/inspiration/creative-center
- Meta Ad Library (research what's actually running): https://www.facebook.com/ads/library/ — filter by Country=Israel + keyword "AI" or "בינה מלאכותית" before generating your own.

# Higgsfield Video Production Brief
## Recruitin RPO Campaign - 3 Hero Videos + 5 Carousel Variations

**Platform:** Seedance 2.0 (image-to-video, reference-driven)
**Alt models:** Veo 3.1 / Veo 3.1 Lite / Kling 3.0 / Cinema Studio Video 3.0
**Duration:** 5-15 seconds per shot
**Audio:** ElevenLabs voice clone (Dutch, female, professional)
**Target:** LinkedIn + Meta (Facebook/Instagram/Reels)
**Brand Colors:** Creme #FAF8F3 | Antraciet footer | Orange #E8630A accent

---

## VIDEO 1: "The Problem" (Urgency Hook)
**Seedance / Veo prompt:**
```
Professional tech company office, morning light. HR director at desk,
frustrated, looking at spreadsheet with red X marks (open vacancies).
Camera slowly dollies in to her face, slight frown. Transition: screen
fills with red "OPEN VACANCIES" text spinning. Background fades to dark
blue-gray (tension). Text reveal: "Openstaande vacatures remmen je groei."
Creme background slides in, antraciet footer with Recruitin logo.
Style: cinematic corporate, slight warm-to-cool color grade.
Duration: 8-10 seconds
```

**Reference image (Nano Banana Pro / Leonardo Phoenix):**
```
Prompt: "Professional corporate office, HR director looking frustrated at
computer screen showing open job vacancies spreadsheet. Warm morning light
from window. Professional photography, corporate environment, realistic."
Resolution: 1920x1080, aspect 16:9
```

---

## VIDEO 2: "The Solution" (Confidence Hook)
**Seedance / Veo prompt:**
```
Same HR director, now smiling confidently. Quick montage:
- diverse candidates in interview format (2-3 sec each)
- check marks appearing as candidates are selected
- growth chart rising smoothly from left to right
- team celebrating (high-five, thumbs up)
Background transitions: dark -> creme gradient.
Text reveals: "RPO doet het voor jou." | "Gegarandeerd resultaat."
Style: uplifting, energetic montage, dynamic cuts.
Duration: 10-12 seconds
```

**Reference image:**
```
Prompt: "Diverse professional team in modern office celebrating success.
Smiling faces, confident poses, growth chart visible on screen in background.
Modern corporate environment, natural lighting, positive energy."
Resolution: 1920x1080, aspect 16:9
```

---

## VIDEO 3: "The Partnership" (Positioning Hook)
**Seedance / Veo prompt:**
```
Split screen: left = Recruitin team member shaking hands with client
director. Right = handshake transitions to growing graph and candidate
profiles appearing. Seamless transition to unified screen showing the
workflow: sourcing -> screening -> placement -> success metric.
Timeline animation, each step highlighted with orange #E8630A accent.
Creme background, antraciet footer with: "Een partner in jouw groei."
Style: modern minimalist motion graphics meets cinematic.
Duration: 10-12 seconds
```

**Reference image:**
```
Prompt: "Two professional men shaking hands in modern office. One wearing
subtle Recruitin branding. Growing business metrics on digital screen behind
them. Collaborative, trustworthy, modern corporate environment."
Resolution: 1920x1080, aspect 16:9
```

---

## VIDEO 4-8: CAROUSEL VARIATIONS (LinkedIn 9:16)
5-second loops, captions on-screen.

### V4: HR Director POV
"Close-up of HR director face, nodding confidently. Text: 'Recruitin RPO:
Maanden werk in weken.' Creme bg. Quick cut to growth metric +100%."

### V5: CFO POV (Cost Focus)
"Financial dashboard showing cost reduction. Money bag animation.
Text: 'Vaste kosten. Geen verborgen bureaukosten.' Antraciet footer."

### V6: Operations Manager POV (Scale)
"Scaling animation, small to large. Candidates multiplying on screen.
Text: 'Schaal flexibel. Betaal proportioneel.'"

### V7: Quality Focus
"Quality checkmark animations. Candidate profiles with green check marks.
Text: 'Alleen gekwalificeerde kandidaten. 0% waste.'"

### V8: Speed Focus
"Timeline animation: Vacature -> Interview -> Hire. Days counting down.
Text: '4 weken. Guaranteed.'"

---

## VOICE SCRIPT (ElevenLabs Dutch Female)
Master 30-second background audio for Video 1-3:

```
[0-5 sec]   "Openstaande vacatures remmen je groei. Je weet het."
[5-10 sec]  "Met Recruitin RPO neem je dit probleem uit handen."
[10-18 sec] "We bouwen je recruitment-team. Schaalbaar. Gegarandeerd resultaat."
[18-25 sec] "Geen bureau. Een partner in jouw groei."
[25-30 sec] "Recruitin RPO. Maak nu een afspraak."
```

**Voice Config:**
- Voice ID: Recruitin female clone (warmth + authority)
- Model: eleven_multilingual_v2
- Language: Dutch (nl-NL)
- Stability: 0.45
- Similarity Boost: 0.85
- Style: 0.0
- Speaker Boost: true

---

## PRODUCTION CHECKLIST

- [ ] Generate 3 reference images (Nano Banana Pro or Leonardo Phoenix)
- [ ] Submit Seedance 2.0 / Veo 3.1 prompts with reference images
- [ ] Clone ElevenLabs voice + record master script
- [ ] Apply lipsync via SyncLabs (if presenter shots are used)
- [ ] Export MP4 + add creme background burn
- [ ] Test on mobile, tablet, desktop
- [ ] Create LinkedIn captions per variant
- [ ] A/B test: logo placement (top vs bottom)
- [ ] Configure GA4 video_view events

---

## ESTIMATED COSTS

| Step | Tool | Cost |
|------|------|------|
| 3 reference images | Nano Banana Pro / Leonardo | ~15 credits |
| 3 hero videos (Seedance 2.0 std 720p) | Higgsfield | ~150 credits |
| 5 carousel clips (Veo 3.1 Lite fast) | Higgsfield | ~50 credits |
| ElevenLabs voiceover | ElevenLabs | ~20 EUR |
| SyncLabs lipsync (optional) | SyncLabs | ~30 EUR |
| **Total Higgsfield credits** | | **~215** |
| **Total EUR (external)** | | **~50** |

Available Higgsfield balance: 474.95 credits — sufficient.

---

## DEPLOYMENT
1. Upload MP4s to public storage URL pattern: `https://publieke-storage.recruitin.nl/assets/[video-id].mp4`
2. Configure Meta Ads Manager with the variants
3. Wire each variant to a UTM (see `config/ga4_setup.json`)
4. Track via GA4 + Pixel events

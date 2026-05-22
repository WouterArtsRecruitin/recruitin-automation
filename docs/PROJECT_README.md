# Recruitin Meta Automation Engine — Project Guide

**Version:** 1.0.0  |  **Owner:** Wouter Arts (warts@recruitin.nl, 06-14314593)  |  **Status:** Production Ready

End-to-end automation for Recruitin RPO campaigns: lead capture → CRM → tracking → optimization.

---

## Repo layout (this PR adds)

```
recruitin-automation/
├── config/
│   ├── audience_builder.json       Meta ToFu/MoFu/BoFu audiences
│   ├── ga4_setup.json              GA4 events, audiences, UTM template
│   ├── meta-ad-copy-set.json       20 RPO ad copy variants
│   └── settings.env.example        env var template
├── creative_pipeline/
│   └── orchestrator.py             ElevenLabs + SyncLabs video pipeline
├── webhook_backend/
│   └── server.py                   FastAPI Meta Lead Ads webhook
├── tests/
│   └── test_webhooks.py            6 pytest cases — all green locally
├── docs/
│   ├── API_SPEC.md                 webhook contract + curl examples
│   ├── DEPLOYMENT.md               Render + Meta + Zapier go-live
│   ├── higgsfield-video-briefs.md  3 hero videos + 5 carousel briefs
│   └── PROJECT_README.md           this file
└── requirements.production.txt     pinned Python deps
```

---

## Quickstart

```bash
git clone https://github.com/WouterArtsRecruitin/recruitin-automation.git
cd recruitin-automation
python -m venv venv && source venv/bin/activate
pip install -r requirements.production.txt
cp config/settings.env.example config/settings.env
# Fill in API keys
pytest tests/ -v
cd webhook_backend && uvicorn server:app --reload
```

See `docs/DEPLOYMENT.md` for production deployment via Render.

---

## Campaign assets

- **20 ad copy variants** mapped to HR Director / Operations Manager / CFO personas
- **3 audiences** (ToFu cold, MoFu lookalike, BoFu retargeting) with €1000/wk test budget
- **3 hero videos** + 5 carousel variants — Seedance 2.0 / Veo 3.1 prompts in `docs/higgsfield-video-briefs.md`
- **5 GA4 conversion events** + UTM template for end-to-end attribution

---

## Performance targets

- Video CTR: 0.8–1.2% (benchmark: 0.5%)
- CPC: €45 (target €40–50)
- CPL: €120–150
- Lead → Meeting: 30%
- Meeting → Deal: 25%

Kill rule: CPL > €200 after 5k impressions. Scale rule: CPL < €100 + min 3 leads → 2× budget.

---

## What still needs your hand

1. ElevenLabs + SyncLabs API keys in `config/settings.env` (never commit them).
2. Deploy webhook to Render — see DEPLOYMENT.md.
3. Hook up Meta App Dashboard → webhook URL.
4. Create Zapier zap to forward to Pipedrive.
5. Generate the 3 hero videos via Higgsfield (use the briefs in docs).
6. Import 20 ad variants + 3 audiences into Meta Ads Manager.
7. Launch with €1000/wk test budget. Review at day 14.

---

## Support

Issues / PRs welcome.

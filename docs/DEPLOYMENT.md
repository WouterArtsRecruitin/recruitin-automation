# Deployment Guide — Recruitin Webhook Backend

## 1. Local Development

```bash
git clone https://github.com/WouterArtsRecruitin/recruitin-automation.git
cd recruitin-automation
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.production.txt
cp config/settings.env.example config/settings.env
# Fill in API keys
pytest tests/ -v
cd webhook_backend && uvicorn server:app --reload
```

## 2. Production — Render.com (recommended)

1. Push repo to GitHub (already done).
2. Render dashboard → New → Web Service → connect repo.
3. **Build command:** `pip install -r requirements.production.txt`
4. **Start command:** `uvicorn webhook_backend.server:app --host 0.0.0.0 --port $PORT`
5. Add env vars from `config/settings.env.example` in the Render dashboard.
6. Deploy. You get an HTTPS URL like `https://recruitin-webhook.onrender.com`.

## 3. Meta App Dashboard Setup

1. Go to https://developers.facebook.com → your app → **Webhooks**
2. Subscribe object: **Page**
3. Callback URL: `https://recruitin-webhook.onrender.com/webhook`
4. Verify token: paste `META_VERIFY_TOKEN` value
5. Subscribe to field: `leadgen`
6. Connect the Recruitin FB Page → add `leadgen` subscription
7. Click **Test** in the webhook UI → expect `200 OK`

## 4. Zapier Integration

1. New Zap → trigger: **Webhooks by Zapier → Catch Hook**
2. Copy webhook URL → paste into `PIPEDRIVE_WEBHOOK_URL` env var
3. Action: **Pipedrive → Create Person + Create Deal**
   - Person fields: extract from `raw` payload
   - Deal title: `RPO Lead — {{meta_lead_id}}`
   - Deal value: `€0` (placeholder, updated on Quick Scan)
   - Pipeline: Pipeline 12 (or 14)
   - Owner: `account_owner`
4. Action 2: **Slack → Send Channel Message** → `#leads-meta`

## 5. GA4 + Meta Pixel

1. Place Meta Pixel + GA4 tag on landing page (via GTM container).
2. Fire `lead_form_submit` from the LP thank-you page.
3. GA4 → **Events → Mark as conversion** for the events in `config/ga4_setup.json`.
4. Connect GA4 to Looker Studio → import the dashboard template.

## 6. Smoke Test

```bash
# After deploy
curl https://recruitin-webhook.onrender.com/health
curl -X POST https://recruitin-webhook.onrender.com/test-lead
# Check Pipedrive for the test lead
```

## 7. Go-Live Checklist

- [ ] Webhook deployed and `/health` returns `healthy`
- [ ] Meta verify handshake succeeded
- [ ] `META_APP_SECRET` set → signature verification active
- [ ] Test lead arrives in Pipedrive + Slack
- [ ] GA4 conversion events confirmed in DebugView
- [ ] Looker Studio dashboard live
- [ ] 3 hero videos uploaded to public storage
- [ ] 20 ad variants imported into Meta Ads Manager
- [ ] 3 audiences (ToFu/MoFu/BoFu) built per `audience_builder.json`
- [ ] Daily budget caps verified
- [ ] Kill rule and scale rule documented for the campaign manager

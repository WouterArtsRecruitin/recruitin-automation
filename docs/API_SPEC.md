# API Specification — Recruitin Webhook Backend

**Version:** 1.0.0
**Base URL (local):** `http://localhost:8000`
**Base URL (prod):** `https://webhook.recruitin.nl`

---

## Authentication

Meta webhook requests are verified two ways:

1. **GET `/webhook`** — `hub.verify_token` query param must equal `META_VERIFY_TOKEN`.
2. **POST `/webhook`** — `X-Hub-Signature-256` header must be a valid HMAC-SHA256 over the raw body, signed with `META_APP_SECRET`.

If `META_APP_SECRET` is not configured, signature verification is skipped and a warning is logged. **Always set it in production.**

---

## Endpoints

### `GET /`
Liveness probe. Returns `Recruitin Webhook Backend v1.0.0 - operational`.

### `GET /health`
Detailed health check.

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-22T10:00:00Z",
  "crm_configured": true,
  "signature_verification": true
}
```

### `GET /webhook`
Meta subscription handshake.

Query params:
- `hub.mode` — must be `subscribe`
- `hub.challenge` — random string Meta sends; we echo it back
- `hub.verify_token` — must match `META_VERIFY_TOKEN`

Response: the raw `hub.challenge` string with `200 OK`, or `403` if token mismatches.

### `POST /webhook`
Receive a lead-generation notification from Meta.

Headers:
- `Content-Type: application/json`
- `X-Hub-Signature-256: sha256=<hex digest>` (validated when `META_APP_SECRET` is set)

Body (Meta envelope):
```json
{
  "object": "page",
  "entry": [
    {
      "id": "PAGE_ID",
      "time": 1700000000,
      "changes": [
        {
          "field": "leadgen",
          "value": {
            "leadgen_id": "12345",
            "form_id": "67890",
            "page_id": "PAGE_ID",
            "created_time": 1700000000
          }
        }
      ]
    }
  ]
}
```

Response:
```json
{
  "received": true,
  "lead_id": "12345",
  "crm_forwarded": true,
  "timestamp": "2026-05-22T10:00:00.000Z"
}
```

### `POST /test-lead`
Sends a mock lead through the CRM forwarder. Useful for verifying the Zapier/Pipedrive hook end-to-end without touching Meta.

---

## CRM Forward Payload

When a lead arrives, this normalized payload is POSTed to `PIPEDRIVE_WEBHOOK_URL`:

```json
{
  "platform": "meta",
  "funnel_stage": "MoFu_Qualified_Lead",
  "meta_lead_id": "12345",
  "meta_form_id": "67890",
  "meta_page_id": "PAGE_ID",
  "account_owner": "warts@recruitin.nl",
  "received_at": "2026-05-22T10:00:00.000Z",
  "raw": { "...original Meta envelope..." }
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 400  | Invalid JSON body |
| 403  | Verification token mismatch or invalid HMAC signature |
| 500  | Internal error (logged with stack trace) |

---

## Local Testing

```bash
# Start server
cd webhook_backend
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# Verify webhook handshake
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.challenge=test123&hub.verify_token=RecruitinSecureToken2026!"
# -> test123

# Send mock lead
curl -X POST http://localhost:8000/test-lead

# Run test suite
pytest tests/ -v
```

"""
Recruitin Webhook Backend
Receives Meta Lead Ad webhooks, validates, enriches, forwards to CRM.

Run:
    cd webhook_backend
    uvicorn server:app --host 0.0.0.0 --port 8000 --reload
"""

import os
import hmac
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path

import requests
from fastapi import FastAPI, Request, HTTPException, Query, Header
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config" / "settings.env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("recruitin-webhook")

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "RecruitinSecureToken2026!")
APP_SECRET = os.getenv("META_APP_SECRET", "")
CRM_WEBHOOK_URL = os.getenv("PIPEDRIVE_WEBHOOK_URL", "")
ACCOUNT_OWNER = os.getenv("ACCOUNT_OWNER", "warts@recruitin.nl")

app = FastAPI(
    title="Recruitin Webhook Backend",
    version="1.0.0",
    description="Meta Lead Ad to CRM pipeline for Recruitin RPO campaigns",
)


# ----------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------
class LeadPayload(BaseModel):
    platform: str = "meta"
    funnel_stage: str = "MoFu_Qualified_Lead"
    meta_lead_id: Optional[str] = None
    meta_form_id: Optional[str] = None
    meta_page_id: Optional[str] = None
    account_owner: str = ACCOUNT_OWNER
    received_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    raw: Dict[str, Any] = Field(default_factory=dict)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def verify_signature(body: bytes, signature_header: Optional[str]) -> bool:
    """Verify X-Hub-Signature-256 against the Meta app secret."""
    if not APP_SECRET:
        logger.warning("META_APP_SECRET not set - skipping signature verification")
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(
        APP_SECRET.encode("utf-8"), body, hashlib.sha256
    ).hexdigest()
    received = signature_header.split("=", 1)[1]
    return hmac.compare_digest(expected, received)


def extract_lead_data(meta_payload: Dict[str, Any]) -> LeadPayload:
    """Parse the Meta webhook envelope into a normalized LeadPayload."""
    lead = LeadPayload(raw=meta_payload)

    entries = meta_payload.get("entry", [])
    for entry in entries:
        for change in entry.get("changes", []):
            value = change.get("value", {})
            lead.meta_lead_id = value.get("leadgen_id") or lead.meta_lead_id
            lead.meta_form_id = value.get("form_id") or lead.meta_form_id
            lead.meta_page_id = value.get("page_id") or lead.meta_page_id
    return lead


def forward_to_crm(lead: LeadPayload) -> bool:
    """Push enriched lead to Zapier/Pipedrive webhook."""
    if not CRM_WEBHOOK_URL:
        logger.warning("PIPEDRIVE_WEBHOOK_URL not set - skipping CRM forward")
        return False

    try:
        response = requests.post(
            CRM_WEBHOOK_URL, json=lead.model_dump(), timeout=10
        )
        response.raise_for_status()
        logger.info(f"CRM forward OK: lead={lead.meta_lead_id}")
        return True
    except Exception as exc:
        logger.error(f"CRM forward failed: {exc}")
        return False


# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------
@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Recruitin Webhook Backend v1.0.0 - operational"


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "crm_configured": bool(CRM_WEBHOOK_URL),
        "signature_verification": bool(APP_SECRET),
    }


@app.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
):
    """Meta webhook handshake. Returns hub.challenge on success."""
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        logger.info("Meta webhook verified")
        return hub_challenge
    logger.warning(f"Meta verification failed: mode={hub_mode}")
    raise HTTPException(status_code=403, detail="Verification token mismatch")


@app.post("/webhook")
async def receive_lead(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None),
):
    """Receive a Meta Lead Ad notification, normalize, forward to CRM."""
    body = await request.body()

    if not verify_signature(body, x_hub_signature_256):
        logger.warning("Signature verification failed")
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    logger.info(f"Lead received: {payload}")
    lead = extract_lead_data(payload)
    crm_ok = forward_to_crm(lead)

    return JSONResponse(
        {
            "received": True,
            "lead_id": lead.meta_lead_id,
            "crm_forwarded": crm_ok,
            "timestamp": lead.received_at,
        }
    )


@app.post("/test-lead")
async def test_lead():
    """Send a mock lead to validate the CRM forwarder end-to-end."""
    mock = LeadPayload(
        meta_lead_id="test_lead_123",
        meta_form_id="test_form_456",
        meta_page_id="test_page_789",
        raw={"test": True, "source": "test-lead endpoint"},
    )
    crm_ok = forward_to_crm(mock)
    return {"sent": True, "crm_ok": crm_ok, "payload": mock.model_dump()}

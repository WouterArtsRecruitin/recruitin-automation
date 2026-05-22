"""Tests for the webhook backend."""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "webhook_backend"))
os.environ.setdefault("META_VERIFY_TOKEN", "RecruitinSecureToken2026!")

from server import app  # noqa: E402

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Recruitin" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_webhook_verification_success():
    response = client.get(
        "/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "challenge_12345",
            "hub.verify_token": "RecruitinSecureToken2026!",
        },
    )
    assert response.status_code == 200
    assert response.text == "challenge_12345"


def test_webhook_verification_failure():
    response = client.get(
        "/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "challenge_12345",
            "hub.verify_token": "wrong_token",
        },
    )
    assert response.status_code == 403


def test_webhook_post_invalid_json():
    response = client.post("/webhook", content="not json")
    assert response.status_code == 400


def test_webhook_post_valid():
    payload = {
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
                            "created_time": 1700000000,
                        },
                    }
                ],
            }
        ],
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["received"] is True
    assert data["lead_id"] == "12345"

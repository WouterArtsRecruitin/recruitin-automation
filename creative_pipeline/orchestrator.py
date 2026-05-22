"""
Recruitin Video Production Orchestrator
Generates RPO campaign videos: ElevenLabs voiceover + SyncLabs lipsync.

Usage:
    python orchestrator.py
"""

import os
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config" / "settings.env")


class VideoOrchestrator:
    """Orchestrates AI video production for Recruitin RPO campaigns."""

    def __init__(self):
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID")
        self.synclabs_key = os.getenv("SYNCLABS_API_KEY")
        self.output_path = Path(os.getenv("STORAGE_PATH", "./output_ads/"))
        self.output_path.mkdir(parents=True, exist_ok=True)

        if not self.elevenlabs_key:
            raise EnvironmentError("ELEVENLABS_API_KEY missing in settings.env")

    def generate_voiceover(self, text: str, output_path: str) -> str:
        """Generate Dutch voiceover via ElevenLabs cloned voice."""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
        headers = {
            "xi-api-key": self.elevenlabs_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.85,
                "style": 0.0,
                "use_speaker_boost": True,
            },
        }

        response = requests.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code != 200:
            raise RuntimeError(
                f"ElevenLabs error {response.status_code}: {response.text[:200]}"
            )

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"  Voiceover saved: {output_path}")
        return output_path

    def trigger_lipsync(self, video_url: str, audio_url: str) -> str:
        """Start a SyncLabs lipsync job. Returns job_id."""
        url = "https://api.synclabs.so/lipsync"
        headers = {
            "x-api-key": self.synclabs_key,
            "Content-Type": "application/json",
        }
        payload = {
            "audioUrl": audio_url,
            "videoUrl": video_url,
            "model": "sync-1.6.0",
            "synergize": True,
            "maxCredits": 100,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        job_id = response.json().get("id")
        print(f"  Lipsync job queued: {job_id}")
        return job_id

    def poll_sync_job(self, job_id: str, output_filename: str, max_wait_seconds: int = 1800) -> str:
        """Poll until lipsync job finishes, then download MP4."""
        url = f"https://api.synclabs.so/lipsync/{job_id}"
        headers = {"x-api-key": self.synclabs_key}
        polls = 0
        max_polls = max_wait_seconds // 15

        while polls < max_polls:
            response = requests.get(url, headers=headers, timeout=30)
            data = response.json()
            status = data.get("status", "UNKNOWN")

            if status == "COMPLETED":
                video_url = data.get("videoUrl") or data.get("outputUrl")
                video_response = requests.get(video_url, timeout=60)
                out_path = self.output_path / output_filename
                with open(out_path, "wb") as f:
                    f.write(video_response.content)
                print(f"  Lipsynced video saved: {out_path}")
                return str(out_path)

            if status == "FAILED":
                raise RuntimeError(f"SyncLabs job failed: {data.get('error')}")

            print(f"  Job {job_id} status={status} ({polls+1}/{max_polls})")
            time.sleep(15)
            polls += 1

        raise TimeoutError(f"Lipsync job {job_id} timed out")

    def generate_video_batch(self):
        """Generate the full campaign batch."""
        videos = [
            {
                "id": "rpo_01_problem",
                "title": "The Problem Hook",
                "voice_script": (
                    "Openstaande vacatures remmen je groei. "
                    "Telkens dure bureaus inschakelen lost niets structureels op."
                ),
            },
            {
                "id": "rpo_02_solution",
                "title": "The Solution Hook",
                "voice_script": (
                    "Met Recruitin RPO halen we een schaalbaar recruitment-team in huis "
                    "dat gegarandeerd resultaat levert."
                ),
            },
            {
                "id": "rpo_03_partnership",
                "title": "The Partnership Hook",
                "voice_script": (
                    "Geen bureau. Een partner in jouw groei. "
                    "Klik hieronder voor de gratis Quick Scan."
                ),
            },
        ]

        results = []
        for video in videos:
            print(f"\nProcessing {video['id']}: {video['title']}")
            try:
                audio_path = self.generate_voiceover(
                    video["voice_script"],
                    str(self.output_path / f"{video['id']}_voice.mp3"),
                )
                results.append({
                    "id": video["id"],
                    "title": video["title"],
                    "audio": audio_path,
                    "voice_script": video["voice_script"],
                    "status": "voiceover_ready",
                })
            except Exception as exc:
                print(f"  Failed: {exc}")
                results.append({"id": video["id"], "status": "failed", "error": str(exc)})

        manifest_path = self.output_path / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nManifest written: {manifest_path}")
        return results


if __name__ == "__main__":
    orchestrator = VideoOrchestrator()
    results = orchestrator.generate_video_batch()
    print("\n" + "=" * 60)
    print("BATCH RESULTS")
    print("=" * 60)
    print(json.dumps(results, indent=2))

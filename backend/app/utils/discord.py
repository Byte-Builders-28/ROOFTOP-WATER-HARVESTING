import matplotlib.pyplot as plt
import io
import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise RuntimeError("DISCORD_WEBHOOK_URL not set in .env")

def send_to_discord_from_response(api_response: dict, state: str, city: str):
    # --------- Chart ----------
    values = api_response.get("rain_forecast") or [0, 0, 0, 0, 0]
    days = range(1, len(values) + 1)

    plt.figure(figsize=(6, 4))
    plt.plot(days, values, marker="o", linewidth=2)
    plt.fill_between(days, values, alpha=0.2)
    plt.xlabel("Day")
    plt.ylabel("Rain (mm)")
    plt.title("Rain Forecast")
    plt.grid(True, linestyle="--", alpha=0.4)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # --------- Message ----------
    tips = "\n".join(f"- {t}" for t in api_response.get("storage_tips", [])) or "-"
    storage = {0: "Low", 1: "High"}.get(api_response.get("storage_risk"), "-")
    quality = {0: "Low", 1: "High"}.get(api_response.get("quality_risk"), "-")

    content = (
        "@everyone\n"
        f"**Water Report for {state}, {city}**\n"
        f"pH: {api_response.get('ph', '-')}\n"
        f"TDS: {api_response.get('tds', '-')} ppm\n"
        f"Storage Risk: {storage}\n"
        f"Quality Risk: {quality}\n"
        f"Overall Suggestion: {api_response.get('overall_suggestion', '-')}\n\n"
        f"Tips:\n{tips}"
    )

    payload = {
        "content": content,
        "allowed_mentions": {"parse": ["everyone"]}
    }

    files = {
        "file": ("rain_forecast.png", buf, "image/png")
    }

    resp = requests.post(
        WEBHOOK_URL,
        data={"payload_json": json.dumps(payload)},
        files=files,
        timeout=15
    )

    resp.raise_for_status()
    return resp

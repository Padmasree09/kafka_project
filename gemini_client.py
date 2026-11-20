import json
import time
import uuid
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

def gemini_call_instrumented(prompt: str, model: str = "gemini-2.5-flash", request_id: str = None):
    request_id = request_id or str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    start_time = time.time()

    event = {
        "request_id": request_id,
        "timestamp": timestamp,
        "model": model,
        "status": None,
        "latency_ms": None,
        "prompt_tokens": None,
        "completion_tokens": None,
        "response_text": None,
        "error_message": None,
    }

    try:
        response = client.models.generate_content(
            model=model,
            contents=f"System tracking reference: {request_id}. {prompt}"
        )
        end_time = time.time()
        latency_ms = end_time - start_time

        event["status"] = "success"
        event["latency_ms"] = round(latency_ms * 1000)
        event["prompt_tokens"] = response.usage_metadata.prompt_token_count
        event["completion_tokens"] = response.usage_metadata.candidates_token_count
        event["response_text"] = response.text

    except Exception as e:
        end_time = time.time()
        latency_ms = end_time - start_time

        event["status"] = "error"
        event["latency_ms"] = round(latency_ms * 1000)
        event["error_message"] = str(e)

    return event
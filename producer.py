from confluent_kafka import Producer
from gemini_client import gemini_call_instrumented
import json


producer = Producer({
    "bootstrap.servers": "localhost:9092"
})
topic = "llm.request.completed.v1"
def publish_event(event: dict):
  producer.produce( topic= topic, value = json.dumps(event))
  return "event published succesfully"

event = gemini_call_instrumented("explain artificial intelligence", model="gemini-2.5-flash")
publish_event(event)
producer.flush()
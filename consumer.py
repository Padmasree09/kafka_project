import json

from confluent_kafka import Consumer
import redis
from cost_calculator import calculate_cost 
from storage import store_event, init_db

init_db()

# -----------------------------
# Connect to Redis
# -----------------------------

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


# -----------------------------
# Connect to Kafka
# -----------------------------

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "llm-request-processor",
    "auto.offset.reset": "earliest"
})


# -----------------------------
# Subscribe to the Kafka topic
# -----------------------------

topic = "llm.request.completed.v1"

consumer.subscribe([topic])

print(f"Listening to {topic}...")


# -----------------------------
# Continuously read messages
# -----------------------------

try:
    while True:

        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            print(f"Kafka error: {message.error()}")
            continue


        # Convert Kafka message bytes/string into Python dictionary
        event = json.loads(
            message.value().decode("utf-8")
        )

        # Get request_id
        request_id = event["request_id"]


        # Check Redis
        if redis_client.exists(request_id):

            print(f"skipped duplicate: {request_id}")

        else:

            print(f"processed: {request_id}")

            # Store request_id in Redis
            redis_client.set(request_id, "processed")
            calculate_cost_value = calculate_cost(
                event["prompt_tokens"],
                event["completion_tokens"],
                event["model"]
            )
            event["cost"] = calculate_cost_value
            store_event(event)


except KeyboardInterrupt:

    print("\nStopping consumer...")


finally:

    consumer.close()
import sqlite3
def init_db():
    conn = sqlite3.connect('observability.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS llm_events (
                        request_id TEXT PRIMARY KEY,
                        model TEXT NOT NULL,
                        status TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        latency_ms REAL,
                        prompt_tokens INTEGER,
                        completion_tokens INTEGER,
                        cost REAL
                    )''')
    conn.commit()
    conn.close()

def store_event(event: dict):
    conn = sqlite3.connect('observability.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO llm_events (request_id, model, status, timestamp, latency_ms, prompt_tokens, completion_tokens, cost)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (event["request_id"], event["model"], event["status"], event["timestamp"],
                    event["latency_ms"], event["prompt_tokens"], event["completion_tokens"], event.get("cost")))
    conn.commit()
    conn.close()
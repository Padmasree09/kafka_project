import sqlite3



def cost_per_model():
    conn = sqlite3.connect("observability.db")
    cursor = conn.cursor()
    

    #sql query to return the cost per model from the llm_events table
    query = """
    SELECT model, SUM(cost) as total_cost
    FROM llm_events
    GROUP BY model
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def cost_per_day():
    conn = sqlite3.connect("observability.db")
    cursor = conn.cursor()
    #sql query to return the cost per day from the llm_events table
    query = """
    SELECT DATE(timestamp) as day, SUM(cost) as total_cost
    FROM llm_events
    GROUP BY day
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def average_cost_per_call():
    conn = sqlite3.connect("observability.db")
    cursor = conn.cursor()
    #sql query to return the average cost per call from the llm_events table
    query = """
    SELECT AVG(cost) as average_cost
    FROM llm_events
    """
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result[0]


def calls_per_day():
    conn = sqlite3.connect("observability.db")
    cursor = conn.cursor()
    # sql query to return the number of API calls per day from the llm_events table
    query = """
    SELECT DATE(timestamp) as day, COUNT(*) as total_calls
    FROM llm_events
    GROUP BY day
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def average_latency_per_day():
    conn = sqlite3.connect("observability.db")
    cursor = conn.cursor()
    # sql query to return the average latency per day from the llm_events table
    query = """
    SELECT DATE(timestamp) as day, AVG(latency_ms) as average_latency_ms
    FROM llm_events
    GROUP BY day
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def success_vs_error_count():
    conn = sqlite3.connect("observability.db")
    cursor = conn.cursor()
    # sql query to return the number of calls grouped by status from the llm_events table
    query = """
    SELECT status, COUNT(*) as total_calls
    FROM llm_events
    GROUP BY status
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

print("Cost per model:", cost_per_model())
print("Cost per day:", cost_per_day())
print("Average cost per call:", average_cost_per_call())

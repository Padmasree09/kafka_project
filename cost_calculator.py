PRICING = {
        "gemini-2.5-flash": {
            "input_cost" : 0.30,   # Cost per input token in USD
            "output_cost" : 2.50,  # Cost per output token in USD
        },
        "gemini-2.5-pro": {
            "input_cost" : 1.25,   # Cost per input token in USD
            "output_cost" : 10.00,  # Cost per output token in USD
        }
        
    }
def calculate_cost(prompt_tokens: int, completion_tokens: int, model: str):
    
    if(model not in PRICING):
        raise ValueError(f"Model '{model}' not found in pricing dictionary.")
    input_cost = prompt_tokens / 1000000 * PRICING[model]["input_cost"]
    output_cost = completion_tokens / 1000000 * PRICING[model]["output_cost"]
    total_cost = input_cost + output_cost

    return total_cost


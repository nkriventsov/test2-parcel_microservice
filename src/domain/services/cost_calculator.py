

def calculate_delivery_cost(weight: float, content_value: float, exchange_rate: float) -> float:
    return (weight * 0.5 + content_value * 0.01) * exchange_rate


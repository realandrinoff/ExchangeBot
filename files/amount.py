from decimal import Decimal, InvalidOperation

def convert_amount(amount: str) -> Decimal:
    try:
        result = Decimal(amount)
    except InvalidOperation:
        raise ValueError("Invalid amount")

    if result.is_signed():
        raise ValueError("Amount cannot be negative")

    if not result.is_finite():
        raise ValueError("Amount cannot be infinite or NaN")

    return result

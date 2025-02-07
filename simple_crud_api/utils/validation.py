from typing import Any

def phone_number_validation(num: Any) -> bool:
    if not isinstance(num, int):
        return False
    count = 0
    while num > 0:
        num //= 10
        count+=1
    if count != 10:
        return False
    return True
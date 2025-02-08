from string import ascii_letters, digits
from typing import Any, Tuple

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


def password_validation(raw_password: str) -> Tuple[bool, str]:
    invalid_message = False, (
        "Password must be atleast 8 characters and atmost 20 characters"
        "and should also include alphanumeric, not special chracter are allowed"
    )
    
    if len(raw_password) < 8 or len(raw_password) > 20:
        return invalid_message
    
    if (
        not any(c.isdigit() for c in raw_password) or 
        not any(c.isupper() for c in raw_password) or
        not any(c.islower() for c in raw_password)  
    ):
        return invalid_message
    
    return True, "Successfull password"
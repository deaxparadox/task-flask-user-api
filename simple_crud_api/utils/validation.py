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
        "Password must be atleast 8 characters"
        "and should be alphanumeric, not special chracter are allowed"
    )
    
    if len(raw_password) < 8:
        return invalid_message
    
    # num_collect = []
    # for c in raw_password:
    #     if c not in ascii_letters:
    #         num_collect.append(c)
    #     if c in 
    # for c in digits:
    #     if c not in digits:
    #         return invalid_message
        
    return True, "Successfull password"
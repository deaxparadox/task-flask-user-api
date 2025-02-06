from typing import Optional
from dataclasses import dataclass

@dataclass
class UserLoginSerializer:
    id: int
    username: str
    password: str
    first_name: str
    lastname: str
    
@dataclass
class UserRegisterSerializer:
    username: str
    password: str
    role: int
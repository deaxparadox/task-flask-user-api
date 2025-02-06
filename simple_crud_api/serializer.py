from dataclasses import dataclass

@dataclass
class UserLoginSerializer:
    username: str
    password: str
    
@dataclass
class UserRegisterSerializer:
    username: str
    password: str
    role: int
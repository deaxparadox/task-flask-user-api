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
    

@dataclass
class AddressSerializer:
    line1: str
    city: str
    state: str
    country: str
    pincode: str

@dataclass
class UserProfileSerializer:
    first_name: str
    last_name: str
    email: str
    phone: int
    username: str
    address: AddressSerializer | None = None
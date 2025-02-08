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
    address: AddressSerializer | None = None
    
    


@dataclass
class AddressUpdateSerializer:
    line1: str | None = None
    line2: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    pincode: str | None = None
@dataclass

class UserUpdateSerializer:
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: int | None = None
    username: str | None = None
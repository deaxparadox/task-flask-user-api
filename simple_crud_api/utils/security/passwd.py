import bcrypt
from ...settings import ENCODING


def make_password(byte_password: bytes, /) -> bytes:
    return bcrypt.hashpw(byte_password, bcrypt.gensalt())
    
def check_password(raw_password: str, hashed_password: str, /, encoding: str = ENCODING) -> bool: 
    byte_password = raw_password.encode(encoding)
    byte_hashed_password = hashed_password.encode(encoding)
    return bcrypt.checkpw(byte_password, byte_hashed_password)

def generate_hashed_password(raw_password: str = None, /, encoding: str = ENCODING) -> str:
    byte_password = raw_password.encode(encoding)
    return make_password(byte_password).decode(encoding)
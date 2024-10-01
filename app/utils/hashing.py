from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password_plane:str, password_hash: str) -> bool:
    return pwd_context.verify(password_plane, password_hash)

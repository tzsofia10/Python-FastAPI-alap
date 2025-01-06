import bcrypt

class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password)

    @staticmethod
    def get_password_hash(password):
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        string_password = hashed_password.decode('utf8')
        return string_password
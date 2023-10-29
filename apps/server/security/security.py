import json
import typing

import bcrypt
import cryptography.fernet
from cryptography.fernet import Fernet
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from packages.config.env import env


class Security:
    """
    Security is a class dedicated to data security in a Python application.
    It provides methods for creating secure tokens with an expiration time and encrypting/decrypting
    sensitive information.
    """

    @staticmethod
    def generate_token(email: str) -> str:
        """creates a token to the user"""
        secret_key = env.SECRET_KEY
        if not secret_key:
            raise Exception("SECRET_KEY is not set.")

        token: URLSafeTimedSerializer = URLSafeTimedSerializer(secret_key)
        return token.dumps(email)

    @staticmethod
    def verify_token(
        email: str,
        token: str,
    ) -> bool:
        """checks whether the token entered is valid."""
        secret_key = env.SECRET_KEY
        if not secret_key:
            raise Exception("SECRET_KEY is not set.")

        content = URLSafeTimedSerializer(secret_key)
        try:
            loads = content.loads(token, max_age=86400)
            return loads == email
        except BadSignature as e:
            print("Assing Error:", e)
            return False
        except Exception as e:
            print("Error:", e)
            return False

    @staticmethod
    def hash_password(password_str: str) -> str:
        """Hashes a password string securely.
        Args:
            password_str (str): The password to be hashed.
        Returns:
            str: Hashed password."""
        salt: bytes = bcrypt.gensalt()
        hash: bytes = bcrypt.hashpw(password_str.encode("utf-8"), salt)
        return hash.decode("utf-8")

    @staticmethod
    def verify_password(hashed_password: str, password: str) -> bool:
        """
        Checks if a hashed password matches the provided password.
         Args:
             hashed_password (str): Hashed password to be checked.
             password (str): Password to compare against the hash.
         Returns:
             bool: True if the password matches the hash, else False.
        """
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
        except ValueError:
            return False

    @staticmethod
    def encrypted_traffic(
        package: typing.Dict[str, typing.Any],
    ) -> typing.Any:
        fernet_key = env.FERNET_KEY
        if not fernet_key:
            raise ValueError("FERNET_KEY is not set.")
        fernet: Fernet = Fernet(fernet_key)
        data: str = json.dumps(package)
        encrypted_data = fernet.encrypt(data.encode())
        return {"secure": encrypted_data}

    @staticmethod
    def decrypted_traffic_package(encrypted_data: str) -> typing.Dict[str, typing.Any]:
        fernet_key = env.FERNET_KEY
        if not fernet_key:
            raise ValueError("FERNET_KEY is not set.")
        fernet: Fernet = Fernet(fernet_key)
        try:
            encrypted_data = fernet.decrypt(encrypted_data.encode())
            return json.loads(encrypted_data)
        except Exception as e:
            print(e)
            return {"error": "Something was wrong!", "status": 500}


if __name__ == "__main__":
    # example teste de criptografia do trafego
    data = Security.encrypted_traffic({"OK": 1})
    print(data)
    print(
        Security.decrypted_traffic_package(
            "Z0FBQUFBQmxQYVY0ZWVJdUJHdFJCaHI1ZW1yczg5Zmw5UFdqRHRsOFNGa"
            "VhJWE5yT3NXbDJxTXJzdHc4RGE1WmMtWWdaS3NNcmlsRWNRSml1WUdHb"
            "09lY2tONEJZa1VPclJ5aTV0TnBFbGlYV0hyQUlUTXdMWEl6dnJZVE1TQkZa"
            "THVjZjBSeGJISG80VFhhaWtGYlZQVlBvbHBrN2stX1kzTUgtOVZHNi1BVTdhc"
            "FF5ZEJsdjhPZ2I3REhFZkZ3WTdCQmRLbFgzcXJhWEpjV2x4cHdBcEQtX3p1bEJr"
            "emdXbm52ZWYzVEpJYXlPdGdIRDBPa2Y2MHlrcDQycGpNTldfbE50OUxncWpfRmRP"
            "amdjbEdXRDByUTRaSEdKYW8wX1hrY1F4OWQ5eGpFWG1OUE5LZkE0RnlxVHNUcnlCaXdzS"
            "TdmclZ1UjMx"
            "cVpfUmIxRUtmU0Y5NXV3c3BWWks1UE5xTjFpa1hmOU1tMkZPOUZSSHlhb2R0QUJ1RkJkS"
            "UJXdWQ5dTBIQndLczdr"
            "UlhyczAyVk9pTkE0cWd1ckNEZV9qY3U4VzQw"
            "MGR1eDNOdEVwS0NReGVOdHQ0UWNmMmZIY1daLUJMRG91ZVNqVA=="
        )
    )
    token = Security.generate_token("imaadmin@email.com")
    h = {
        "email": "imaadmin@email.com",
        "token": "ImltYXJvb3RAZW1haWwuY29tIg.ZT1AmQ.uV9iJFUaW3CjDPFMQFk8ac0kzqQ",
    }
    print(Security.verify_token(h["email"], h["token"]))

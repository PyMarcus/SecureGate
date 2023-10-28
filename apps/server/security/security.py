import json
import typing

import bcrypt
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
    def encrypted_traffic_prototype(
        method: typing.Callable,
    ) -> typing.Any:  # criptografa trafego, se der tempo...
        def wrapper(arg: typing.Dict[str, typing.Any]) -> typing.Callable:
            fernet_key = env.FERNET_KEY
            if not fernet_key:
                raise ValueError("FERNET_KEY is not set.")

            fernet: Fernet = Fernet(fernet_key)
            data: str = json.dumps(arg)
            encrypted_data = fernet.encrypt(data.encode())
            return method({"secure": encrypted_data})

        return wrapper

    @staticmethod
    def decrypted_traffic_package(encrypted_data: bytes) -> typing.Dict[str, typing.Any]:
        fernet_key = env.FERNET_KEY
        if not fernet_key:
            raise ValueError("FERNET_KEY is not set.")

        fernet: Fernet = Fernet(fernet_key)
        encrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(encrypted_data)

    @staticmethod
    @encrypted_traffic_prototype
    def prototype_encrypted_traffic_example(
        data: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        return data


if __name__ == "__main__":
    # example teste de criptografia do trafego
    # data = Security.prototype_encrypted_traffic_example({"OK": 1})
    # print(data)
    # print(Security.decrypted_traffic_package(data["secure"]))
    token = Security.generate_token("imaadmin@email.com")
    h = {
        "email": "imaadmin@email.com",
        "token": "ImltYXJvb3RAZW1haWwuY29tIg.ZT1AmQ.uV9iJFUaW3CjDPFMQFk8ac0kzqQ",
    }
    print(Security.verify_token(h["email"], h["token"]))

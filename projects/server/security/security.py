import typing
import bcrypt
import json
from libs import ReadEnv
from cryptography.fernet import Fernet
from itsdangerous import URLSafeTimedSerializer


class Security:
    """
    Security is a class dedicated to data security in a Python application.
    It provides methods for creating secure tokens with an expiration time and encrypting/decrypting
    sensitive information.
    """

    @staticmethod
    def generate_token(user_id: str) -> str:
        """creates a 24-hour token to the user"""
        token_from_env: ReadEnv = ReadEnv(path_to_env="../../../.env.example")
        SECRET: str = token_from_env.secret_key
        token: URLSafeTimedSerializer = URLSafeTimedSerializer(SECRET)
        return token.dumps(user_id)

    @staticmethod
    def verify_token(user_id: str, token: str, ) -> bool:
        """checks whether the token entered is valid."""
        token_from_env: ReadEnv = ReadEnv(path_to_env="../../../.env.example")
        SECRET: str = token_from_env.secret_key
        content = URLSafeTimedSerializer(SECRET)
        return content.loads(token) == user_id

    @staticmethod
    def hash_password(password_str: str) -> str:
        """Hashes a password string securely.
        Args:
            password_str (str): The password to be hashed.
        Returns:
            str: Hashed password."""
        salt: bytes = bcrypt.gensalt()
        hash: bytes = bcrypt.hashpw(password_str.encode('utf-8'), salt)
        return hash.decode('utf-8')

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
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except ValueError:
            return False

    @staticmethod
    def encrypted_traffic_prototype(method: typing.Callable) -> typing.Any:  # criptografa trafego, se der tempo...
        def wrapper(arg: typing.Dict[str, typing.Any]) -> typing.Callable:
            key: ReadEnv = ReadEnv(path_to_env="../../../.env.example")
            secret: bytes = key.fernet_key
            fernet: Fernet = Fernet(secret)

            data: str = json.dumps(arg)
            encrypted_data = fernet.encrypt(data.encode())
            return method({"secure": encrypted_data})
        return wrapper

    @staticmethod
    def decrypted_traffic_package(encrypted_data: bytes) -> typing.Dict[str, typing.Any]:
        key: ReadEnv = ReadEnv(path_to_env="../../../.env.example")
        secret: bytes = key.fernet_key
        fernet: Fernet = Fernet(secret)

        encrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(encrypted_data)


    @staticmethod
    @encrypted_traffic_prototype
    def prototype_encrypted_traffic_example(data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return data


if __name__ == '__main__':
    # example teste de criptografia do trafego
    data = Security.prototype_encrypted_traffic_example({"OK": 1})
    print(data)
    print(Security.decrypted_traffic_package(data["secure"]))

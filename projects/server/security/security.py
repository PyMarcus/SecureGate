import bcrypt
from libs import ReadEnv
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

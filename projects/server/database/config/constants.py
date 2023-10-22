from libs import ReadEnv


re: ReadEnv = ReadEnv("../../../.env.example")
POSTGRES_DIALECT: str = f"postgresql://{re.database_password}:{re.database_password}" \
                        f"@{re.database_host}:{re.database_port}/{re.database_name}"

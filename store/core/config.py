from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"

    """
        Uso de barra-inverttida duplo para não gerar o erro 404 Not Found ao
        inicializar o uvicorn, mais detalhes do erro no link abaixo:
        https://github.com/tiangolo/fastapi/discussions/9018
    """
    ROOT_PATH: str = "//"

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

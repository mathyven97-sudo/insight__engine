from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Social Media Insight Engine"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_PATH: str = "social_media.duckdb"
    
    class Config:
        case_sensitive = True

settings = Settings()

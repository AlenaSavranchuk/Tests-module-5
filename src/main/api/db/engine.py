from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.api.configs.config_mentor import Config

engine = create_engine(Config.fetch('dataBaseUrl'), echo = False)
SessionLocal = sessionmaker(bind=engine)


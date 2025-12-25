from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

class Annotation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    transcript: str
    model_used: str

class DBManager:
    def __init__(self, config):
        url = config['database']['postgres_url'] if config['database']['use_postgres'] else "sqlite:///dst.db"
        self.engine = create_engine(url)
        SQLModel.metadata.create_all(self.engine)

    def save(self, filename, text, model):
        with Session(self.engine) as session:
            entry = Annotation(filename=filename, transcript=text, model_used=model)
            session.add(entry)
            session.commit()
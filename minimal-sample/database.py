from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker , DeclarativeBase , Mapped , mapped_column
from config import settings

engine = create_engine(settings.DATABASE_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)   
    age: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, age={self.age})"



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

Base = declarative_base()
factory = None


def global_init(db_file: str):
    global factory

    if factory:
        return

    if not db_file or not db_file.split():
        raise Exception("Укажите файл бд.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = create_engine(conn_str, echo=False)
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    from . import __all_models

    Base.metadata.create_all(bind=engine)


def create_session() -> Session:
    global factory
    return factory()

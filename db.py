from sqlalchemy import create_engine
from sqlmodel import Session


engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},
    echo=True
)

def get_session():
    """
    This could be a single line function -
    ```
    def get_session():
        return Session(engine)
    ```
    However, I prefer returning the session wrapped inside the with block,
    because it would provide protection against data corruption by faicilitating rollback
    in case of exceptions.

    """
    with Session(engine) as session:
        yield session
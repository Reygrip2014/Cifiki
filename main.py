from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base
from engine import check_tables
from rtbf import rtbfScraper

def main():
    engine = create_engine(
        'sqlite:///test.db',
        echo=True
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    #check_tables(session)
    rtbfScraper(session).main()


if __name__ == "__main__":
    main()
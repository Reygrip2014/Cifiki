from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from rtbf import rtbfScraper

def main():
    engine = create_engine(
        'sqlite:///test.db',
        echo=True
    )
    session = Session(engine)
    rtbfScraper(session).main()


if __name__ == "__main__":
    main()
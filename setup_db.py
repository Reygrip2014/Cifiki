from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Site


SITES = [
        {
            "url":"http://rtbf.be/",
            "name": "rtbf"
        }
]


def create_tables():
    engine = create_engine(
        'sqlite:///test.db',
        echo=True
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    for site in SITES:
        s = Site(
                url = site["url"],
                name = site["name"]
        )
        session.add(s)
        session.flush()
    session.commit()

if __name__ == "__main__":
    create_tables()
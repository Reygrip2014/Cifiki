from hashlib import new
from bs4 import BeautifulSoup
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import requests

from models import Site, News

class rtbfScraper():
    def __init__(self, session) -> None:
        self.name = "rtbf"
        self.url = "http://rtbf.be/"
        self.session = session

    def scrape(self) ->None:
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "lxml")
        main_news_url = soup.find("div", class_="w-full lg:w-2/3").a["href"]
        site = self.session.execute(select(Site).filter_by(name=self.name)).first()
        news = News(
                url = main_news_url, 
                start = datetime.now()
        )
        if site:
            site = site[0]
            main_news = self.session.get(News,site.main_news_id)
            if main_news.url != news.url:
                main_news.stop = datetime.now()
                main_news.is_main = False
        else:
            site = Site(
                url = self.url,
                name = self.name
            )
            site.news.append(
                news
           )
            self.session.add(site)
            self.session.flush()
        news.site_id = site.id
        self.session.add(news)
        self.session.flush()
        site.main_news_id = news.id
        self.session.flush()
        print(site.main_news_id)
        self.session.commit()

    def main(self):
        self.scrape()

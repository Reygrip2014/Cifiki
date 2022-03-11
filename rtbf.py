from bs4 import BeautifulSoup
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import requests
from Cifiki.main import main

from models import Site, MainNews, CoureselNews

class rtbfScraper():
    def __init__(self, session) -> None:
        self.name = "rtbf"
        self.url = "http://rtbf.be"
        self.session = session

    def scrape(self) ->None:
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "lxml")
        site = self.session.execute(select(Site).filter_by(name=self.name)).scalar_one()
        #self.scrape_main_news(soup, site)  
        self.scrape_carousel_news(soup, site)      
        self.session.flush()
       
    def scrape_main_news(self, soup, site):
        main_news_url = soup.find("div", class_="w-full lg:w-2/3").a["href"]
        news = MainNews(
                url = self.url+main_news_url, 
                start = datetime.now(),
                site_id = site.id
        )
        main_news = self.session.get(MainNews,site.main_news_id)
        if main_news:
            if main_news.url != news.url:
                main_news.stop = datetime.now()
                main_news.is_main = False
            else:
                return
        self.session.add(news)
        self.session.flush()
        site.news.append(
            news
        )
        self.session.add(site)
        site.main_news_id = news.id

    def scrape_carousel_news(self, soup, site):
        lis = soup.select("div[id=slider_react-aria-3]>ul[class=swiper-wrapper]>li")
        for li in lis:
            url = self.url+li.div.a["href"]
            couresels_news = self.session.execute(select(CoureselNews).filter_by(url=url)).scalar_one_or_none()
            if not couresels_news:
                news = CoureselNews(
                    url = url, 
                    start = datetime.now(),
                    site_id = site.id,
                    is_carousel = True
                )

    def main(self):
        self.scrape()
        self.session.commit()
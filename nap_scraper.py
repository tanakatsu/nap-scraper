# coding: utf-8

from bs4 import BeautifulSoup
from util import getPage
import requests
from tqdm import tqdm


class NapScraper(object):
    SITE_URL = 'https://www.nap-camp.com'

    def keyword_search(self, keyword):
        endpoint = '{}/list'.format(self.SITE_URL)
        params = {
            'KEYWORDS': keyword,
        }
        res = requests.post(endpoint, data=params)
        res.encoding = res.apparent_encoding
        html = res.text

        soup = BeautifulSoup(html, "html.parser")
        lists = soup.select("div.block_campsite_list")
        lists = [l for l in lists if 'advertising' not in l.get('class')]

        result = []
        for l in lists:
            camp_lst = l.select("div.camp_list")
            url = camp_lst[0].a.get("href")
            name = camp_lst[0].h2.span.string
            area = url.split('/')[-3]
            campsite_id = url.split('/')[-2]
            result.append({'name': name, 'url': self.SITE_URL + url, 'area': area, 'campsite_id': campsite_id})
        return result


    def get_reviews(self, area, campsite_id, max_count=None, per_page=10):
        review_cnt = self.__get_total_review_count(area, campsite_id)
        if max_count:
            fetch_cnt = min(review_cnt, max_count)
        else:
            fetch_cnt = review_cnt

        review_urls = []
        for i in tqdm(range(0, fetch_cnt, per_page), desc="collecting review urls"):
            review_urls.extend(self.__get_review_urls(area, campsite_id, i, per_page))

        reviews = []
        for url in tqdm(review_urls, desc="getting reviews"):
            review = self.__get_review(url)
            reviews.append(review)

        return reviews


    def __get_total_review_count(self, area, campsite_id):
        html = getPage("{}/{}/{}/review".format(self.SITE_URL, area, campsite_id))
        soup = BeautifulSoup(html, "html.parser")
        return int(soup.select("div.review_num span[itemprop='votes']")[0].string)


    def __get_review_urls(self, area, campsite_id, index, per_page):
        html = getPage("{}/{}/{}/review/?01={}&L1={}".format(self.SITE_URL, area, campsite_id, index, per_page))
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select("p.review_sentence a.more_info")
        paths = [link.get("href") for link in links]
        return [self.SITE_URL + path for path in paths]


    def __get_review(self, url):
        html = getPage(url)
        soup = BeautifulSoup(html, "html.parser")
        dds = soup.select("div.review_text dl dd")
        return [d.text.replace('\r\n', '').replace('\n', '') for d in dds]


if __name__ == "__main__":
    scraper = NapScraper()
    # print(scraper.keyword_search('バウアーハウス'))
    print(scraper.get_reviews("kanagawa", 11677, max_count=10))

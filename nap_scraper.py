# coding: utf-8

from bs4 import BeautifulSoup
from util import getPage
import requests
from tqdm import tqdm
from time import sleep


class NapScraper(object):
    SITE_URL = 'https://www.nap-camp.com'

    def __init__(self, interval=1):
        self.interval = interval

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

    def get_reviews(self, area, campsite_id, max_cnt=None, per_page=10):
        review_cnt = self.__get_total_review_count(area, campsite_id)
        if max_cnt:
            fetch_cnt = min(review_cnt, max_cnt)
        else:
            fetch_cnt = review_cnt

        review_urls = []
        for i in tqdm(range(0, fetch_cnt, per_page), desc="collecting review urls"):
            review_urls.extend(self.__get_review_urls(area, campsite_id, i, per_page))
            sleep(self.interval)

        review_urls = review_urls[:fetch_cnt]
        reviews = []
        for url in tqdm(review_urls, desc="getting reviews"):
            review = self.__get_review(url)
            review_id = int(url.split('=')[1])
            reviews.append({'id': review_id, 'review': review})
            sleep(self.interval)

        return reviews

    def get_area_list(self):
        area_list = []

        html = getPage("{}".format(self.SITE_URL))
        soup = BeautifulSoup(html, "html.parser")
        search_prefecture_elm = soup.find('div', id='main_search_prefecture')
        elms = search_prefecture_elm.find_all('dd')
        for elm in elms:
            links = elm.find_all('a')
            for link in links:
                area = link['href'].split('/')[1]
                area_list.append(area)
        # print(len(area_list))
        return area_list

    def get_campsite_list(self, area, max_cnt=None, per_page=10):
        start_no = 0
        campsite_list = []

        while True:
            result = self.__get_campsite_list_from_page(area, start_no, per_page)
            start_no += per_page

            if len(result) == 0:
                break
            campsite_list.extend(result)

            if max_cnt and len(campsite_list) >= max_cnt:
                campsite_list = campsite_list[:max_cnt]
                break
            sleep(self.interval)

        return campsite_list

    def __get_campsite_list_from_page(self, area, start_no, per_page):
        html = getPage("{}/{}/list?OFFSET={}&LIMIT={}&display_order=21&".format(self.SITE_URL, area, start_no, per_page))
        soup = BeautifulSoup(html, "html.parser")
        campsite_elms = soup.select("div.block_campsite_list div.camp_list a")

        campsite_list = []
        for elm in campsite_elms:
            campsite_id = elm.get("href").split('/')[-2]
            campsite_name = elm.select("h2 span.name")[0].string
            campsite_name = campsite_name.replace('\u3000', '')
            campsite_list.append({'id': campsite_id, 'name': campsite_name, 'area': area})
        return campsite_list

    def __get_total_review_count(self, area, campsite_id):
        html = getPage("{}/{}/{}/review".format(self.SITE_URL, area, campsite_id))
        soup = BeautifulSoup(html, "html.parser")
        return int(soup.select("div.review_num span[itemprop='votes']")[0].string)

    def __get_review_urls(self, area, campsite_id, index, per_page):
        html = getPage("{}/{}/{}/review/?O1={}&L1={}&".format(self.SITE_URL, area, campsite_id, index, per_page))
        soup = BeautifulSoup(html, "html.parser")
        links = soup.select("p.review_sentence a.more_info")
        paths = [link.get("href") for link in links]
        return [self.SITE_URL + path for path in paths]

    def __get_review(self, url):
        html = getPage(url)
        soup = BeautifulSoup(html, "html.parser")
        dds = soup.select("div.review_text dl dd")
        if len(dds) > 0:
            review = ''.join([d.text.replace('\r\n', '').replace('\n', '') for d in dds])
        else:
            sentences = soup.select("p.review_sentence")[0]
            review = sentences.text.strip().replace('\r', '').replace('\n', '')
        return review



if __name__ == "__main__":
    scraper = NapScraper()
    # print(scraper.keyword_search('バウアーハウス'))
    # print(scraper.get_reviews("kanagawa", 11677, max_cnt=10))
    print(scraper.get_campsite_list("kanagawa"))
    # print(scraper.get_area_list())

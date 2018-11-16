# coding: utf-8

from nap_scraper import NapScraper
import pickle
import pandas as pd
import os
import argparse


def get_reviews(area, campsite_id, output_file, fmt='csv', max_cnt=None, interval=1):
    scraper = NapScraper(interval=interval)
    reviews = scraper.get_reviews(area, campsite_id, max_cnt=max_cnt)

    if fmt == 'pkl':
        pickle.dump(reviews, open(output_file, "wb"))
    elif fmt == 'csv':
        data = []
        for review in reviews:
            id = review['id']
            comments = review['review']
            data.append([id, comments])
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, header=False)
    else:
        raise ValueError("unknown output format")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('area', type=str, action='store', help='area code')
    parser.add_argument('campsite_id', type=str, action='store', help='campsite id')
    parser.add_argument('--output', '-o', type=str, action='store', help='output filename')
    parser.add_argument('--max_cnt', type=int, action='store', help='max reviews to fetch')
    parser.add_argument('--interval', type=int, default=1, action='store', help='page access interval')

    args = parser.parse_args()

    area = args.area
    campsite_id = args.campsite_id
    max_cnt = args.max_cnt
    interval = args.interval

    if args.output:
        output_filename = args.output
    else:
        output_filename = "{area}_{campsite_id}_reviews.csv".format(area=area, campsite_id=campsite_id)

    fmt = os.path.splitext(output_filename)[-1].replace('.', '')

    get_reviews(area, campsite_id, output_filename,
                fmt=fmt, max_cnt=max_cnt, interval=interval)

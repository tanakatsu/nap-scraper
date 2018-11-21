# coding: utf-8

from nap_scraper import NapScraper
import pandas as pd
import os
import argparse


def get_reviews_from_csv(campsite_list_csv, output_dir=".", interval=1):
    df = pd.read_csv(campsite_list_csv)
    for i, row in df.iterrows():
        area = row['area']
        campsite_id = row['id']
        output_filename = "{area}_{campsite_id}_reviews.csv".format(area=area, campsite_id=campsite_id)
        output_filename = os.path.join(output_dir, output_filename)

        if os.path.exists(output_filename):
            print("{}: File exists. Skipped.".format(output_filename))
            continue

        print(output_filename)
        get_reviews(area, campsite_id, output_filename, interval=interval)


def get_reviews(area, campsite_id, output_file, interval=1):
    scraper = NapScraper(interval=interval)
    reviews = scraper.get_reviews(area, campsite_id)

    data = []
    for review in reviews:
        id = review['id']
        comments = review['review']
        data.append([id, comments])
    df = pd.DataFrame(data, columns=['review_id', 'text'])
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('campsite_list_csv', type=str, action='store', help='campsite list csv')
    parser.add_argument('--output_dir', type=str, action='store', help='output directory')
    parser.add_argument('--interval', type=int, default=1, action='store', help='page access interval')

    args = parser.parse_args()

    campsite_list_csv = args.campsite_list_csv
    interval = args.interval

    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = "."

    get_reviews_from_csv(campsite_list_csv,
                         output_dir=output_dir, interval=interval)

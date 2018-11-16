# coding: utf-8

from nap_scraper import NapScraper
import pandas as pd
import argparse
from tqdm import tqdm


def get_campsite_list(output_file, interval=1):
    scraper = NapScraper(interval=interval)
    areas = scraper.get_area_list()

    campsite_list = []
    for area in tqdm(areas):
        result = scraper.get_campsite_list(area)
        campsite_list.extend(result)

    data = []
    for campsite in campsite_list:
        area = campsite['area']
        id = campsite['id']
        name = campsite['name']
        data.append([area, name, id])

    df = pd.DataFrame(data, columns=["area", "id", "name"])
    df.to_csv(output_file, index=False, header=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', type=str, action='store', help='output filename')
    parser.add_argument('--interval', type=int, default=1, action='store', help='page access interval')

    args = parser.parse_args()
    interval = args.interval

    if args.output:
        output_filename = args.output
    else:
        output_filename = "campsite.csv"

    get_campsite_list(output_filename, interval=interval)

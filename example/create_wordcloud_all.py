# coding:utf-8

import MeCab
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from glob import glob
import os


STOP_WORDS = ['あり', 'ある', 'いる', 'する', 'こと', 'それ', 'ない', 'の', 'し', 'さ', 'れ', 'い', 'サイト', 'キャンプ場', '思い', 'キャンプ', 'でき', 'よう', 'とても', 'ところ', '出来', 'なり', 'あっ', 'おり', 'なっ', 'テント', 'キャビン', 'さん', 'なく', 'られ', 'オートキャンプ', 'トイレ', '利用']
# with open("stopwords.txt") as f:
#     STOP_WORDS = [x.rstrip() for x in f.readlines()]


def extract_words(text, target_types=[]):
    output = []

    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')  # https://teratail.com/questions/88592
    node = tagger.parseToNode(text)

    while(node):
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            if target_types:
                if word_type in target_types:
                    output.append(node.surface)
            else:
                output.append(node.surface)
        node = node.next
        if node is None:
            break
    return output


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_dir', type=str, action='store', required=True)
    parser.add_argument('--output_dir', '-o', type=str, action='store', required=True)
    parser.add_argument('--width', type=int, action='store', default=1200)
    parser.add_argument('--height', type=int, action='store', default=800)
    parser.add_argument('--background_color', type=str, action='store', default='white')
    parser.add_argument('--font_path', type=str, action='store')
    parser.add_argument('--min_words', type=int, action='store', default=1)
    args = parser.parse_args()

    kwargs = {
        'width': args.width,
        'height': args.height,
        'background_color': args.background_color,
        'stopwords': STOP_WORDS,
    }
    if args.font_path:
        kwargs['font_path'] = args.font_path

    csvfiles = glob(os.path.join(args.input_dir, "*.csv"))
    for csvfile in csvfiles:
        print(csvfile)
        df = pd.read_csv(csvfile, encoding='utf-8')
        df = df.dropna()  # remove empty line

        data = list(df.iloc[:, 1].values)

        whole_words = []
        for review in data:
            words = extract_words(review, target_types=["形容詞", "動詞", "名詞", "副詞"])
            whole_words.extend(words)
        print("{} words".format(len(whole_words)))

        if len(whole_words) < args.min_words:
            continue

        print("generating...")
        wordcloud = WordCloud(**kwargs).generate(' '.join(whole_words))

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        # plt.show()

        output_file = os.path.join(args.output_dir, os.path.basename(csvfile).replace(".csv", ".png"))
        plt.savefig(output_file)
        print("created {}".format(output_file))
        # break


if __name__ == "__main__":
    main()

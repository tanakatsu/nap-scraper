# coding:utf-8

import MeCab
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from argparse import ArgumentParser


STOP_WORDS = ['あり', 'ある', 'いる', 'する', 'こと', 'それ', 'ない', 'の', 'し', 'さ', 'れ', 'い', 'サイト', 'キャンプ場']


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
    parser.add_argument('--output', '-o', type=str, action='store', default='result.png')
    parser.add_argument('--width', type=int, action='store', default=1200)
    parser.add_argument('--height', type=int, action='store', default=800)
    parser.add_argument('--background_color', type=str, action='store', default='white')
    parser.add_argument('--font_path', type=str, action='store')
    parser.add_argument('csvfile', type=str, action='store')
    args = parser.parse_args()

    review_csvfile = args.csvfile
    df = pd.read_csv(review_csvfile, header=None, encoding='utf-8')
    df = df.dropna()  # remove empty line

    data = list(df[0].values)

    whole_words = []
    for review in data:
        words = extract_words(review, target_types=["形容詞", "動詞", "名詞", "副詞"])
        whole_words.extend(words)
    print("{} words".format(len(whole_words)))

    kwargs = {
        'width': args.width,
        'height': args.height,
        'background_color': args.background_color,
        'stopwords': STOP_WORDS,
    }
    if args.font_path:
        kwargs['font_path'] = args.font_path

    print("generating...")
    wordcloud = WordCloud(**kwargs).generate(' '.join(whole_words))

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    # plt.show()
    plt.savefig(args.output)
    print("created {}".format(args.output))


if __name__ == "__main__":
    main()

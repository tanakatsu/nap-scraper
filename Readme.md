## Nap web scraper

This is a scaper for Nap (www.nap-camp.com) - camping portal site -.

### Functions

##### keyword search

```
from nap_scaper import NapScraper

scraper = NapScraper()
result = scraper.keyword_search('バウアーハウス')
print(result)
```
Output
```
[{'name': 'バウアーハウスジャパン', 'url': 'https://www.nap-camp.com/kanagawa/11678/', 'area': 'kanagawa', 'campsite_id': '11678'}]
```

##### get reviews

```
from nap_scaper import NapScraper

scraper = NapScraper()
result = scraper.get_reviews("kanagawa", 11677, max_cnt=3)
print(result)
```

Output
```
[['森の中でした。晴れたら木の間から見える星が綺麗なんだろうなと思います。川も7、8月なら泳いで 楽しめますね。', '都内から約2時間なので、多少、渋滞しますが行きやすいです。狭い道が多く、すれ 違いするのが大変ですが、まあ、行けます。', 'ゴミ出しに時間かるので、チェックアウトの11時近くは避けて行くことをお勧めします', 'インディアンゾーンは坂道が辛かったです。トイレや洗い物など。', '普通のトイレと洗い場です。トイレ脇のサイトの場合、衝立が老朽化により壊れ丸見えでした。', '施設近くに温泉があります。道の駅もありますがすごく混んでます。', '広大な敷地で、ゾーンごとに、楽しみ方が変わるので、よく調べてからお好みのゾーンを選ぶと良いです。'], ['川が近くにあり子どもたちが遊べる環境です。釣りも楽しめます。木々も適度にあり、木陰も確保でき、サイトによってはハンモックも吊るせます。', '大井松田インターから1時間程度でしょうか、道を迷うことはありませんが途中 での渋滞スポットと、山道ですれ違い出来ないポイントがあるので要注意です。', 'フロントの対応はまずまずですが、とにかく客が多いので、さばくのに大変といった感じです。コールセンターがしっかりしているので、なにかあれば親身になって対応する姿勢があるのはポイント高いです。', 'D2ゾーンに泊まりましたが、炊事とトイレにメインの受付まで戻らなければならず、不便さを感じました。Bゾーンのと きは便利でしたので、サイトのゾーンによるのだと思います。', '最低限の管理はされている感じです。トイレの個室の床が常に濡れているのが掃除のものなのか、なんなのか分からず不快な感じでした。', '周辺には釣り施設もあり、帰りには温泉にも立ち寄れます。ただし、キャンプ場が多いのでシーズンはそれなりに混雑することを覚悟する必要があると思います。', 'さすがにオオバコなので、ギリギリに申込しても何とかなるところはさすがです。今は何度かかよってどのゾーンが一番楽しめるかを体験してますが、今のところBゾーンかなという感じです。'], ['川は透き通るきれいさで、雨の後なので水かさはあ ったけど、本当にきれいな川で最高でした。', 'あの細い？すれ違えない道はこりごり。信号とかつけてくれなくては繁忙期は間違いなく到着できない', 'スタッフの方はすごく多く、説明も丁寧。決められた場所があまりにひどいところで、コールセンターに場所のチェンジを依頼したら、混んでいるにもかかわらず良心的に対応してくれて、一度はダメだったのに、お電話いただいて、変更できました。すごくありがたかった。', 'スタッフも多いし、そんなに安くもないサイトで、詰めるだけ詰め込んでいて、お湯は出ないし、トイレは簡易。しかも夕方になったら水が出なくなって、簡易トイレが流れなく、その上にみんなしていくから最悪な状況。朝になってもかわらず、遠い水が出るトイレに行くことに。もうちょっと人数確保よりも設備を整えて欲しい。', '汚いわけじゃないけど、そのままな感じ。サイトの仕切りも消えててどこまでかあまりわからなかった。', '渋滞はあっても御殿場も近く、温泉もあったりで、環境は良かった。', '敷地が大きいので、多くのキャンパーが入っていて、ギューギューに思えても1サイトの 大きさは十分あり、広々と過ごせました。トイレさえ改善されたらまた行きたいけど、今のところリピーターにはなれません。']]
```

### Example Application

`example` directory has some simple application scripts.

##### Get reviews

```
usage: get_reviews.py [-h] [--output OUTPUT] [--max_cnt MAX_CNT]
                      [--interval INTERVAL]
                      area campsite_id
```

```
$ python get_reviews.py --output reviews.csv kanagawa 11677
```

##### Generate Wordcloud image

Prerequisite
- MeCab ([mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd) is preferred)

Install required packages
```
$ pip install -r requirements
```

```
usage: create_wordcloud.py [-h] [--output OUTPUT] [--width WIDTH]
                           [--height HEIGHT]
                           [--background_color BACKGROUND_COLOR]
                           [--font_path FONT_PATH]
                           csvfile
```

```
$ python create_wordcloud.py --font_path ~/Library/Fonts/ipag.ttf -o wordcloud.png reviews.csv
```


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
[{'id': 21155, 'review': '標高が高いため夏でも涼しく目の前で川遊びが出来てとても気持ちよく過ごせました。途中道が狭く車が１台しか通れず交互に通過しなければならない所が数カ所あります。信号があればいいのですが。分別したゴミを所定の場所に持っていくと係の人がテキパキと片付けていて常に綺麗な状態でした。またリピーターにやさしい割引も魅力です。トイレや炊事場は綺麗で大きめのお風呂もありとても快適でした。いつも綺麗に整備されており気持ちよく利用させていただきました。道の駅を過ぎると店がないため早めに買い物はすませてから行かれたほうがよいでしょう。'}, {'id': 16237, 'review': '川が近く、そして水がとても綺麗。砂地で水はけ がよく、水たまりがない。インターから近く、分かりやすい場所にあるが、何ヶ所か道が狭い場所がある。説明がとても分かりやすく、いろいろと丁寧に対応してもらえる。また、すぐに対応してもらえる。場内はとても整備されている。お湯が出るので、寒い時期も非常に助かります。お風呂も大きくて、良い。場内はとても整備されている。トイレもとても綺麗。夜も灯りが適度にあり、トイレに行くときも安心。行く途中に温泉、道の駅がある。また、釣堀やダムも近くにあり、アクティビティには困らない。とても落ち着いていて、夜も静かに過ごすことができました。'}, {'id': 16093, 'review': '川もあり、木陰もあります。グルキャンはできませんが二世帯で参加。周 りはきれいに整備されていますゴミも分別されておりヤギやアヒルの餌になっているよう手前に有名キャンプ場があり、いっしゅんまちがえますが道のりはわかりやすく迷いはしないとおもぃすインター降りて1時間かからないくらい。反対にはなるけとスーパーがあり大体のものは揃いますゴ ミの分別、水場の温水、お風呂の清掃、トイレはとにかくきれいです！！！売店も品揃えはそんなでもないけど最低限のものはありました。アウトドアグッズのレンタルもあります有料ではありましたがお風呂があります。広くはないけどきれいに使えました。どらいやーもありました水場はおんすいがでます。トイレがとにかくきれいで広い。虫が入らぬよう入り口に網戸があります下水をきれい？にするためトイレットペーパーはゴミ箱へ、となってますサイトも、きれいに整備されてました周辺にはなにもないです。麓まで行くとスーパーがありますがサッといくには時間がかかりました連泊のときは仕方がないかなぁとは思いますが買い出ししてから行くことをおすすめします高規格ではありますがきれいに整備されてます秋と雨のときにしか行ったことないけど、砂利のため水はけがよく、良かった。今度は夏に来てみたいです'}]
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


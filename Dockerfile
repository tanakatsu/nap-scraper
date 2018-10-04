FROM ubuntu:16.04

RUN apt-get update \
  && apt-get install -y python3 python3-pip git curl wget make xz-utils file sudo unzip \
  && apt-get install -y mecab libmecab-dev mecab-ipadic-utf8 \
  && apt-get install -y language-pack-ja \
  && apt clean \
  && update-locale LANG=ja_JP.UTF-8

# Set locale
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8

# Install mecab-ipadic-NEologd (Docker memory should be more than 3GB)
WORKDIR /opt
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
  && cd mecab-ipadic-neologd \
  && ./bin/install-mecab-ipadic-neologd -n -y \
  && cd .. \
  && rm -rf mecab-ipadic-neologd

# Set mecab-ipadic-NEologd as default
RUN sed -i 's/dicdir = \/var\/lib\/mecab\/dic\/debian/dicdir = \/usr\/lib\/mecab\/dic\/mecab-ipadic-neologd/' /etc/mecabrc

# Install python packages
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Install fonts
RUN wget -O IPAfont00303.zip https://ipafont.ipa.go.jp/old/ipafont/IPAfont00303.php \
  && unzip IPAfont00303.zip \
  && mv IPAfont00303 fonts \
  && rm IPAfont00303.zip

# Add scripts
ENV PYTHONPATH /opt
ADD . .

CMD ["bash"]

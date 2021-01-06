#!/usr/bin/python3

import tweepy
import requests
from bs4 import BeautifulSoup

import environ
import logging


######################################
## 環境変数の.envファイルを読み込み ##
######################################
BASE_DIR = environ.Path(__file__) - 1
env = environ.Env()
env_file = str(BASE_DIR.path('.env'))
env.read_env(env_file)


######################################
## 環境変数の.envファイルを読み込み ##
######################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

h = logging.FileHandler('weatherBot.log')
logger.addHandler(h)


######################################
## Twitter API                      ##
## Consumerキー、アクセストークン設定    ##
######################################
Consumer_key = env('CONSUMER_KEY')
Consumer_secret = env('CONSUMER_SECRET')
Access_token = env('ACCESS_TOKEN')
Access_secret = env('ACCESS_SECRET')


# ツイートテンプレート
content = """
おはようございます！
今日もまた、一歩前進しましょう。

今日の天気予報は...? 
※自作Bot by CentOS8 + Python3 + Twitter API + cronで実行
"""


### URLを指定
urls = {
        '札幌市　': 'https://weather.yahoo.co.jp/weather/jp/1b/1400.html',
        '東京　　': 'https://weather.yahoo.co.jp/weather/jp/13/4410.html',
        '名古屋市': 'https://weather.yahoo.co.jp/weather/jp/23/5110.html',
        '大阪市　': 'https://weather.yahoo.co.jp/weather/jp/27/6200.html',
        '福岡市　': 'https://weather.yahoo.co.jp/weather/jp/40/8210.html',
      }


def twitter_auth():
    """Twitter 認証"""
    auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
    auth.set_access_token(Access_token, Access_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    logger.debug('Twitter 認証が成功しました。')
    
    return api


def tweet(api):
    """ツイートする"""
    str = ''
    for city, url in urls.items():
        
        # HTTPリクエスト
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # 今日の天気
        tenki_today = soup.select_one('#main > div.forecastCity > table > tr > td > div > p.pict')
        
        str += f'{city}：' + tenki_today.text.replace('\n', '') + '\n'
    
    # ツイート
    print(content + '\n' + str)
    api.update_status(content + '\n' + str)
    logger.debug('ツイートが成功しました。')


################################
##         処理を行う         ##
################################
if __name__ == '__main__':
    
    api = twitter_auth()
    
    tweet(api)



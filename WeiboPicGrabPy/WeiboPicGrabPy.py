import requests
import argparse
import os
import urllib.parse

WEIBO_API = 'https://api.weibo.com/2/statuses/show.json'

def parse_args():
    parser = argparse.ArgumentParser(description='Grab Weibo Picture')
    parser.add_argument('-t', '--access-token', help='OAuth\'s access token', required=True)
    parser.add_argument('-i', '--id', action='append', help='weibo id', required=True)
    return parser.parse_args()

def save_pic(id, url):
    r = requests.get(url, stream=True)
    filename = os.path.basename(urllib.parse.urlparse(url).path)
    if r.status_code == 200:
        with open(os.path.join(id, filename), 'wb') as f:
            for chunk in r:
                f.write(chunk)

def parse_weibo_json(id, data):
    if not os.path.exists(id):
        os.mkdir(id)
    pic_urls = []
    for url in data['pic_urls'] + data['retweeted_status']['pic_urls']:
        pic_large_url = url['thumbnail_pic'].replace('thumbnail', 'large')
        pic_urls.append(pic_large_url)
    return pic_urls


def main():
    args = parse_args()
    if not os.path.exists('pic'):
        os.mkdir('pic')
    os.chdir('pic')
    for id in args.id:
        payload = {
            'access_token': args.access_token,
            'id': id
            }
        r = requests.get(WEIBO_API, params=payload)
        data = parse_weibo_json(id, r.json())
        for url in data:
            save_pic(id, url)


if __name__ == '__main__':
    main()

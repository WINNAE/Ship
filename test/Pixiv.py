# -*- coding:utf-8 -*-
# Author: 李华
# Date: 2021/09/26

import re
import requests
import json
from lxml import etree
from requests.packages import urllib3
from fake_useragent import FakeUserAgent
urllib3.disable_warnings()


def getPicInformation():
    url = 'https://www.pixiv.net/bookmark_new_illust.php'
    proxies = {
        'http': 'http://127.0.0.1:10801',
        'https': 'http://127.0.0.1:10801',
    }
    headers = {
        'cookie': 'first_visit_datetime_pc=2021-09-26+14%3A25%3A57; p_ab_id=1; p_ab_id_2=6; p_ab_d_id=616938512; yuid_b=NFOAIXA; __cf_bm=RJZGn6zqkV580Nhp7nDFN4Up6FzKfosm5oi_f6wSjQI-1632633979-0-AYm9VxINlHdUi9W6HOp9zL7VOZ++NEK2/NlmNdSgyf+XEAYUugMPM/hRIHYv13p5XhIRBoLJGoUQF9e7vjmWvj4bjj+i37KJnQ9BmOImJJt449T7A3INmAE+rFX3/6LPgJ11SmBg4bNZxfW192cWOyg47O0/qSkedCWQGbO2I4KRkCPlDcaBi8RrHO6ksLtV/w==; PHPSESSID=32944579_VR2RhA1DPbKMPa0Eh2gTlJlx3dE1QiK2; device_token=a5d8343aeb1b49b5a83f6a07a111fd08; privacy_policy_agreement=3; c_type=22; privacy_policy_notification=0; a_type=0; b_type=1; login_ever=yes',
        'referer': 'https://www.pixiv.net/',
        'user-agent': str(FakeUserAgent().random),
    }
    params = {
        'p': '2'
    }
    resp = requests.get(url, proxies=proxies, headers=headers, params=params, timeout=8)
    resp.encoding = 'utf-8'
    html = etree.HTML(resp.text)
    data = html.xpath('//div[@id="js-mount-point-latest-following"]//@data-items')
    information = re.findall('{.+?}', str(data[0]))
    listInformation = list()
    for i in information:
        picInformation = json.loads(i)
        picInformation['url'] = 'https://www.pixiv.net/artworks/' + picInformation['illustId']
        listInformation.append(picInformation)
    return listInformation


def analyzePic(picInformation):
    url = picInformation['url']
    proxies = {
        'http': 'http://127.0.0.1:10801',
        'https': 'http://127.0.0.1:10801',
    }
    headers = {
        'referer': 'https://www.pixiv.net/',
        'user-agent': str(FakeUserAgent().random),
    }
    resp = requests.get(url, proxies=proxies, headers=headers, timeout=8, verify=False)
    resp.encoding = 'utf-8'
    original = re.findall('"original":"(.+?)"', resp.text)
    picInformation['url'] = original[0]
    return picInformation


def save(originalImage):
    url = originalImage['url']
    proxies = {
        'http': 'http://127.0.0.1:10801',
        'https': 'http://127.0.0.1:10801',
    }
    headers = {
        'cookie': 'first_visit_datetime_pc=2021-09-26+14%3A25%3A57; p_ab_id=1; p_ab_id_2=6; p_ab_d_id=616938512; yuid_b=NFOAIXA; __cf_bm=RJZGn6zqkV580Nhp7nDFN4Up6FzKfosm5oi_f6wSjQI-1632633979-0-AYm9VxINlHdUi9W6HOp9zL7VOZ++NEK2/NlmNdSgyf+XEAYUugMPM/hRIHYv13p5XhIRBoLJGoUQF9e7vjmWvj4bjj+i37KJnQ9BmOImJJt449T7A3INmAE+rFX3/6LPgJ11SmBg4bNZxfW192cWOyg47O0/qSkedCWQGbO2I4KRkCPlDcaBi8RrHO6ksLtV/w==; PHPSESSID=32944579_VR2RhA1DPbKMPa0Eh2gTlJlx3dE1QiK2; device_token=a5d8343aeb1b49b5a83f6a07a111fd08; privacy_policy_agreement=3; c_type=22; privacy_policy_notification=0; a_type=0; b_type=1; login_ever=yes',
        'referer': 'https://www.pixiv.net/',
        'user-agent': str(FakeUserAgent().random),
    }
    resp = requests.get(url, proxies=proxies, headers = headers, timeout=8, verify=False)
    with open('E:\Pixiv\%s.jpg' % (originalImage['illustId']), 'wb') as fp:
        fp.write(resp.content)
    return


def main():
    picPool = getPicInformation()
    imagePool = list()
    for i in picPool:
        imagePool.append(analyzePic(i))
    for j in imagePool:
        print(j)
        save(j)
    return


if __name__ == '__main__':
    main()

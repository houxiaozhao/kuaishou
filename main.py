# -*- coding: utf-8 -*-
import re
import requests
import json
from fontTools.ttLib import TTFont

headers = {
    'accept-encoding': 'deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}


def getuserinfo(url):
    if url.find('v.kuaishou.com') < 0:
        return url
    res = requests.get(url, headers=headers)
    print(res.text)
    text = re.search("window.pageData=([\s\S]*?)<\/script>", res.text, re.S).group(1).strip()
    userinfo = json.loads(text)
    ttf_url = userinfo["obfuseData"]["fontCdnUrl"]
    ttf_resp = requests.get(ttf_url)
    try:
        with open('ks.ttf', 'wb') as f:
            f.write(ttf_resp.content)
    except Exception as e:
        print(e)
    font = TTFont('ks.ttf')
    font.saveXML('ks.xml')
    uni_list = font.getGlyphOrder()[1:]
    first_map = {}
    for i, uni in enumerate(uni_list):
        if i == 10:
            first_map[uni] = '.'
        elif i == 11:
            first_map[uni] = 'w'
        elif i == 12:
            first_map[uni] = 'k'
        elif i == 13:
            first_map[uni] = 'm'
        elif i == 14:
            first_map[uni] = '+'
        else:
            first_map[uni] = i
    print(uni_list)
    print(first_map)
    bestcmap = font['cmap'].getBestCmap()
    newmap = dict()
    for key, value in bestcmap.items():
        key = hex(key)
        newmap[key] = value
    print(newmap)
    real_map = {}
    for k, v in newmap.items():
        for x, y in first_map.items():
            if x == v:
                key = re.sub('0x', '&#x', k)
                real_map[key] = y
    print(real_map)
    for key, value in real_map.items():
        if key in text:
            text = text.replace(key+';', str(real_map[key]))
    print(text)
    return text


if __name__ == '__main__':
    userInfo = getuserinfo("https://v.kuaishou.com/8TJLFL")
    print(json.dumps(userInfo))

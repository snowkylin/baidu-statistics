# coding: utf-8
# MIT License
#
# Copyright (c) 2019 Snowkylin Lazarus
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urllib3
import re
import time
import json


def query(word_list, print_html=False):
    res = []
    http = urllib3.PoolManager()
    for word in word_list:
        try:
            r = http.request('GET', 'http://www.baidu.com/s', fields={'wd': word}, timeout=10.0)
        except:
            print('Query timeout, retrying...')
            r = http.request('GET', 'http://www.baidu.com/s', fields={'wd': word}, timeout=20.0)
        html = r.data.decode('utf-8')
        if print_html:
            print(html)
        count = len(re.findall('style="text-decoration:none;">(|http://|https://)baijiahao.baidu.com', html))
        print(word + '\t' + str(count))
        res.append((word, count))
        time.sleep(5)
    print('平均%.2f个百家号' % (sum([count for word, count in res]) / len(res)))
    return res


if __name__ == '__main__':
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b1_c513')
    html = r.data.decode('gbk')
    baidu_words = re.findall('<a class="list-title" target="_blank" href="http://www.baidu.com/baidu\?cl=.*">(.*)</a>', html)
    r = http.request('GET', 'https://top.sogou.com/')
    html = r.data.decode('utf-8')
    sogou_words = re.findall('target="_blank">(.*)</a>(<span class="hot-num">|</p>)', html)
    sogou_words = [i[0] for i in sogou_words]
    print('百度热门关键词：%d个，搜狗热门关键词：%d个' % (len(baidu_words), len(sogou_words)))
    sogou_words_splited = [sogou_words[i * 10: (i + 1) * 10] for i in range(9)]
    sogou_category = ['搜狗热门电影', '搜狗热门电视剧', '搜狗热门综艺', '搜狗热门动漫', '搜狗热门小说', '搜狗热门游戏', '搜狗热门音乐', '搜狗热门汽车', '搜狗热门人物']
    print('搜狗关键词：')
    res = {}
    for i, category in enumerate(sogou_category):
        print(category + '：')
        res[category] = query(sogou_words_splited[i])
    print('百度关键词：')
    res['baidu'] = query(baidu_words)
    print(res)
    with open(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()) + '.json', 'w') as f:
        json.dump(res, f)





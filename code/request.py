import json
import os
import re
import traceback
from time import sleep
from urllib.parse import quote

import numpy as np
import pandas as pd
from pyquery import PyQuery as pq
import requests
import csv
from code.analyse import frequency_text
from code.analyse import hot_band

# with open("test.csv","w") as csvfile:
#     writer = csv.writer(csvfile)
#
#     #先写入columns_name
#     writer.writerow(["index","a_name","b_name"])
#     #写入多行用writerows
#     writer.writerows([[0,1,3],[1,2,3],[2,3,4]])
from code.analyse import emotion_text


#200条
def content_text_(key):
    'https://m.weibo.cn/search?containerid=100103type=1&q=迪丽热巴'
    # key="原神"
    i = 0
    k = 0
    File = open("../other/data/key.csv", "w")
    writer = csv.writer(File)
    writer.writerow(["user_id", "date", "text"])
    File.close()
    File = open("../other/data/key.csv", 'a+', encoding='utf-8')
    writer = csv.writer(File)
    for j in range(1000):
        if i > 200:
            break
        # print(str(j),'j')
        try:
            r = requests.get('https://m.weibo.cn/api/container/getIndex?container''id=100103type%3D1%26q%3D' + quote(
                key) + '&page_type=searchall&page=' + str(j))
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            js = json.loads(r.text)
            web_lists = js['data']['cards']
            print(len(web_lists))
            for web_list in web_lists:
                try:
                    k = k + 1
                    # print('k',str(k))
                    if web_list.get('card_type') == 9:
                        # print(str(j),'type9')
                        pass
                    elif web_list.get('card_type') == 11:
                        web_list = web_list.get('card_group')[0]

                    # print(web_list.get('mblog').get('bid'))
                    web_url = 'https://m.weibo.cn/statuses/show?id=' + web_list.get('mblog').get('bid')
                    sleep(0.1)
                    text_got = requests.get(web_url)
                    text_got.raise_for_status()
                    text_got.encoding = text_got.apparent_encoding
                    text_js = json.loads((text_got.text))
                    user_id = text_js['data']['user']['id']
                    text = text_js['data']['text']
                    date = text_js['data']['created_at']
                    pattern = re.compile(r'<[^>]+>', re.S)
                    result_text = pattern.sub('', text)
                    result_date = pattern.sub('', date)
                    print(str(i), user_id, result_text, result_date)
                    # File.write(str(i)+'*'+str(user_id)+'*'+result_date+'*'+result_text+'\n')
                    # File.flush()
                    writer.writerow([str(user_id), result_date, result_text])
                    i = i + 1
                    if i > 200:
                        break
                except:
                    # print("except")
                    # print(traceback.print_exc())
                    pass
            if j<10:
                sleep(0.5)
            else:
                sleep(3)
            print('k', str(k), 'j', str(j))
        except:
            sleep(1.5)
            # print(traceback.print_exc())
    File.close()


def get_hot_():
    # data = pd.read_csv('../other/test_data/hot.csv')
    # col_1 = data.values[1:51, 0:1]  # 获取一列，用一维数据
    # lines_1 = np.array(col_1)
    # lines_1 = list(lines_1)
    # print(type(lines_1))
    # col_2 = data.values[1:51, 1:2]
    # lines_2 = np.array(col_2)
    # lines_2 = list(lines_2)
    # print(lines_2)
    os.remove('../other/test_data/hot1.csv')
    os.rename('../other/test_data/hot2.csv', '../other/test_data/hot1.csv')
    os.rename('../other/test_data/hot3.csv', '../other/test_data/hot2.csv')
    os.rename('../other/test_data/hot4.csv', '../other/test_data/hot3.csv')
    os.rename('../other/test_data/hot5.csv', '../other/test_data/hot4.csv')

    r = requests.get('https://weibo.com/ajax/statuses/hot_band')
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    js = json.loads(r.text)
    band_lists = js['data']['band_list']
    i = 1
    hot_title_1 = ['hot_title_1']
    hot_degree_1 = ['hot_degree_1']
    with open("../other/test_data/hot5.csv", "w+", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['hot_degree', 'hot_title'])
        # if 1==1:
        for band_list in band_lists:
            print(str(i), band_list['word'], '\t\t\t热度值:', band_list['num'])
            i = i + 1
            hot_title_1.append(band_list['word'])
            hot_degree_1.append(band_list['num'])
            writer.writerow([band_list['num'], band_list['word']])
    #
    # with open("../other/test_data/hot.csv", "w+",encoding='utf-8') as csvfile:
    #     rows=csv.reader(csvfile)
    #     with open("../other/test_data/hot1.csv", "w+",encoding='utf-8') as newfile:
    #         writer=csv.writer(newfile)
    #         i=0
    #         for row in rows:
    #             row.append(hot_title_1[i])
    #             row.append(hot_degree_1[i])
    #             print(row)
    #             i = i + 1
    #             writer.writerow(row)

    # writer = csv.writer(csvfile)
    # writer.writerow(["hot_degree_1", "hot_title_1","hot_degree_2","hot_title_2"])
    # writer.writerow(["hot_degree_1", "hot_title_1"])


#100条左右
def get_user(user_id):
    k = 0
    i = 0
    File = open("../other/test_data/user.csv", "w")
    writer = csv.writer(File)
    writer.writerow(["user_id",  'up', 'comment',"date", "text"])
    File.close()
    File = open("../other/test_data/user.csv", 'a+', encoding='utf-8')
    writer = csv.writer(File)
    for j in range(1, 20):
        # if j==0:
        #     url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413' + str(
        #         user_id) + '_-_WEIBO_SECOND_PROFILE_WEIBO'
        # else:
        sleep(1.5)
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413' + str(
            user_id) + '_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=' + str(j)
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        js = json.loads(r.text)
        web_lists = js['data']['cards']
        for web_list in web_lists:
            sleep(0.5)
            try:
                k = k + 1
                # print('k',str(k))
                if web_list.get('card_type') == 9:
                    # print(str(j),'type9')
                    pass
                elif web_list.get('card_type') == 11:
                    web_list = web_list.get('card_group')[0]

                # print(web_list.get('mblog').get('bid'))
                web_url = 'https://m.weibo.cn/statuses/show?id=' + web_list.get('mblog').get('bid')
                # print(web_url)
                text_got = requests.get(web_url)
                text_got.raise_for_status()
                text_got.encoding = text_got.apparent_encoding
                text_js = json.loads((text_got.text))
                # print(text_js)
                user_id = text_js['data']['user']['id']
                text = text_js['data']['text']
                date = text_js['data']['created_at']
                comment = text_js['data']['comments_count']
                up = text_js['data']['attitudes_count']
                pattern = re.compile(r'<[^>]+>', re.S)
                result_text = pattern.sub('', text)
                result_date = pattern.sub('', date)
                print(str(i), user_id, up,comment ,result_text, result_date)
                # File.write(str(i)+'*'+str(user_id)+'*'+result_date+'*'+result_text+'\n')
                # File.flush()
                writer.writerow([str(user_id),up,comment, result_date, result_text])
                i = i + 1
                if i > 100:
                    break
            except:
                pass
        if i > 100:
            break
        print('j',str(j))
    print('k', str(k), 'i', str(i))
    File.close()


if __name__ == '__main__':
    # content_text_("端午")
    # frequency_text('../other/test_data/key.csv')
    # emotion_text("../other/test_data/key.csv")
    # get_hot_()
    # hot_band()
    # try_()
    # 对用户
    get_user(1686546714)
    # frequency_text('../other/test_data/user.csv')
    # emotion_text("../other/test_data/user.csv")

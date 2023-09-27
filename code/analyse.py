# encoding=utf-8
import csv
import re
from datetime import datetime

import jieba
import pandas as pd
import platform
from snownlp import sentiment
from snownlp import SnowNLP
import numpy as np
import time
import matplotlib.pyplot as plt  # 导入模块
import random


# 生成屏蔽词list
def ignore_lists_gen():
    with open('../other/data/ignore_lists.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return_lines = []
        for line in lines:
            line = line.rstrip("\n")
            return_lines.append(line)
    # print("ignore list",list)
    return return_lines


# 读入文件，打印出现词频前20：关键字：词频
def frequency_text(file_name):
    TOTAL = 10000
    # print("total:" + str(TOTAL))
    # print("test函数开始")
    jieba.enable_paddle()
    if 1 == 1:
        data = pd.read_csv(file_name)
        print("文本打开成功")
        number = 0
        word_key = {}  # 格式为 关键字：词频
        col_1 = data['text']  # 获取一列，用一维数据
        text = np.array(col_1)
        for line in text:
            # 处理一下
            line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）{}]+▓", "", line)
            seg_list0_gen = jieba.cut(line, cut_all=False)  # 精确模式
            seg_list1_gen = jieba.cut(line, use_paddle=True)  # 使用paddle模式，生成器
            seg_list1 = list(seg_list1_gen)

            # 计算每个词的词频，在word_key里
            for seg in seg_list1:
                if seg in word_key:
                    word_key[seg] = word_key[seg] + 1  # 词频加1
                else:
                    word_key[seg] = 1

            number = number + 1

            # 好看进度
            if number > TOTAL:
                break
            if number % (TOTAL / 100) == 0:
                i = int(number / (TOTAL / 100))
                print('\r' + '▇' * (i // 2) + str(i) + '%', end='')

        ############以下为词频排行部分
        result_list = []  # 输出用的list
        empty_list = [" ", "  ", "   ", "   ", "    "]  # 因为空格处理不掉，所以在这里处理一下
        ignore_list = ignore_lists_gen()  # 用屏蔽词生成器生成屏蔽词列表
        for key, value in word_key.items():
            if key not in ignore_list and key not in empty_list:
                result_list.append([key, value])  # 不在屏蔽词里的加入结果list
        result_list.sort(key=lambda x: x[1], reverse=True)  # 结果list排序一下
        print("result_list:", result_list[:10])  # 输出前20个
        print("result_list:", result_list[10:20])
        print("result_list:", result_list[20:30])
        return result_list
        # print("result_list:", result_list[30:40])


# 读入文件，查看情感走向趋势
def emotion_text(file_name):
    if 1 == 1:
        data = pd.read_csv(file_name)
        col_1 = data['text']  # 获取一列，用一维数据
        lines = np.array(col_1)
        file_pos = open('_emotion_pos.csv', 'w', encoding='utf-8')
        file_neg = open('_emotion_neg.csv', 'w', encoding='utf-8')
        file_mid = open('_emotion_mid.csv', 'w', encoding='utf-8')
        writer_pos = csv.writer(file_pos)
        writer_pos.writerow(["text"])
        writer_neg = csv.writer(file_neg)
        writer_neg.writerow(["text"])
        writer_mid = csv.writer(file_mid)
        writer_mid.writerow(['text'])
        print("情感分析开始")
        total = len(lines)
        per = int(total / 100)
        # print("total:",str(total))
        count = 0
        count_neg = 0
        count_pos = 0
        count_mid = 0
        for line in lines:
            emotion = SnowNLP(line).sentiments
            if emotion < 0.4:
                count_neg = count_neg + 1
                writer_neg.writerow([line])
            elif emotion > 0.6:
                count_pos = count_pos + 1
                writer_pos.writerow([line])
            else:
                count_mid = count_mid + 1
                writer_mid.writerow([line])
            count = count + 1
            # print(str(count))
            if count > total:
                break
            # if count%per==0:
            #     i=int(count/per)
            #     print('\r' + '|' * (i // 2) + str(i) + '%', end='')
        print("\n")
        print("总共词条数为：", str(total))
        print("负面词条数为：", str(count_neg), "占总数的", str(count_neg / total))
        print("中性词条数为：", str(count_mid), "占总数的", str(count_mid / total))
        print("正面词条数为：", str(count_pos), "占总数的", str(count_pos / total))
        file_neg.close()
        file_mid.close()
        file_pos.close()
    list = emotion_frequency()
    return [[count_neg / total, count_mid / total, count_pos / total], list]


# 查看负面和正面的情绪分别的词频
def emotion_frequency():
    print("负面词频为：")
    list_neg = frequency_text("_emotion_neg.csv")
    print("正面词频为：")
    list_pos = frequency_text("_emotion_pos.csv")
    return [list_neg, list_pos]


# 训练模型，老天爷给我个好的训练集吧
def train_emotion():
    #####snownlp训练模型
    # 重新训练模型
    sentiment.train('other/nlp/neg.txt', 'other/nlp/pos.txt')
    # 保存好新训练的模型
    sentiment.save('web_sentiment.marshal')


# 查看训练出来的模型准确率
def test_emotion():
    with open('other/nlp/test.txt', "r", encoding='utf-8') as file:
        lines = file.readlines()
        totle = len(lines)
        print("total:", str(totle))
        count = 0
        is_neg = 0
        test_neg = 0
        count_correct = 0
        for line in lines:
            elements = line.split(",")
            if elements[1] == "0":
                is_neg = 1
            elif elements[1] == "1":
                is_neg = 0
            emotion = SnowNLP(elements[2]).sentiments
            if emotion < 0.5:
                if is_neg == 1:
                    count_correct = count_correct + 1
            elif emotion >= 0.5:
                if is_neg == 0:
                    count_correct = count_correct + 1
            count = count + 1
            if count % (totle / 10) == 0:
                print("已完成", str(count / (totle / 10)), "/10")
        print("准确率", str(count_correct / totle))


# 分析热搜变化情况
def hot_band():
    hot_list = []  # 热搜格式的列表，应该共5个,内容是hot_dic
    for i in range(1, 6):
        data = pd.read_csv('../other/test_data/hot' + str(i) + '.csv')
        print(str(i) + "号文件打开成功")
        hot_list_s = []  # 格式为 里面也是列表，关键字，词频，排序
        hot_degree = data['hot_degree']  # 获取一列，用一维数据
        hot_title = data['hot_title']
        hot_degree = np.array(hot_degree)
        hot_title = np.array(hot_title)
        # print(type(hot_degree))
        # print(hot_degree)
        # print(type(hot_title))
        # print(hot_title)
        num = 0
        for title in hot_title:
            list_a = [title, hot_degree[num], num + 1]
            num = num + 1
            hot_list_s.append(list_a)
        # print(hot_dic)
        hot_list.append(hot_list_s)
    # print(hot_list[0])
    # print(hot_list[1])
    # print(hot_list[2])
    # print(hot_list[3])
    # print(hot_list[4])
    per_list = [[], [], [], []]
    for i in range(0, 4):
        old_title = []  # 格式为，标题，排行
        new_title = []
        j = 0
        for list in hot_list[i]:
            old_title.append(list[0])
        for list in hot_list[i + 1]:
            new_title.append(list[0])
            if list[0] in old_title:
                x = old_title.index(list[0]) - new_title.index(list[0])
                # print('-1',end=' ')
            else:
                x = -99
                # print('1', end=' ')
            list.append(x)
            per = list
            # print(per)
            per_list[i].append(per)
            j = j + 1
    print(per_list[0])
    print(per_list[1])
    print(per_list[2])
    print(per_list[3])
    return per_list


# AC算法，多字符串匹配
import ahocorasick
import pandas as pd
import numpy as np


def build_actree(wordlist):
    actree = ahocorasick.Automaton()
    for index, word in enumerate(wordlist):
        actree.add_word(word, (index, word))
        # flag[index]=1
        # print(index)
    # print('flag',flag)
    actree.make_automaton()
    # print('success')
    return actree


def AC_(wordlist):
    # wordlist = ['中学', '石弓中学','情况']
    # print(len(wordlist))
    flag = np.zeros(len(wordlist), int)
    flag2 = 1
    File = open('../other/data/key.csv', 'r', encoding='utf-8')
    sent = pd.read_csv(File)
    col_1 = sent['text']
    # print(col_1)
    lines = np.array(col_1)
    return_list=[]
    for line in lines:
        # print(line)
        actree = build_actree(wordlist=wordlist)
        for i in actree.iter(line):
            # print(i)
            index = i[1][0]
            # print('index',index)
            flag[index] = 1
            # print('flag',flag)
        for j in range(len(wordlist)):
            # print(flag[j])
            if flag[j] == 1:
                # print('con')
                continue
            else:
                flag2 = 0
        # print('flag2',flag2)
        if flag2 == 1:
            print(line)
            return_list.append(line)

        flag2 = 1
        flag = np.zeros(len(wordlist), int)
        # print('re')
    # actree = build_actree(wordlist=wordlist)
    # # print(actree)
    # for i in actree.iter(col_1):
    #     print(i)
    return return_list


# 分析用户发微博频率，点赞评论
def user_analyse():
    print("user_analyse begin")
    GMT_FORMAT = '%a %b %d  %H:%M:%S +0800 %Y'
    MY_FORMAT = '%Y-%b-%d'
    data = pd.read_csv('../other/test_data/user.csv')
    print("用户文本打开成功")
    up = data['up']  # 格式为 里面也是列表，关键字，词频，排序
    print(type(up))
    comment = data['comment']  # 获取一列，用一维数据
    date_s = data['date']

    num = 0
    temp_date = ''
    # 格式为[日期，微博数,总点赞数，总评论数]
    list = []
    temp_list = ['', 0, 0, 0]
    # print(len(date_s))
    for line in date_s:
        if num == 0 or num == 1:  # 去掉置顶微博
            num = num + 1
        else:
            print(num, end='')
            date = datetime.strptime(line, GMT_FORMAT)
            date = date.strftime(MY_FORMAT)
            date = datetime.strptime(date, MY_FORMAT)
            if date == temp_date:
                temp_list = [date,
                             temp_list[1] + 1,
                             temp_list[2] + up[num],
                             temp_list[3] + comment[num]]
            else:
                list.append(temp_list)
                temp_list = [date, 1, up[num], comment[num]]
                temp_date = temp_list[0]

            num = num + 1
    list.remove(list[0])
    print('')
    print(list)
    return list


if __name__ == '__main__':
    # test_emotion()
    # frequency_text("other/data/test_file.txt")
    # emotion_text("other/data/哈尔滨大学.txt")
    # frequency_text("../other/test_data/key.csv")
    # emotion_text("../other/test_data/key.csv")
    hot_band()
    # user_analyse()

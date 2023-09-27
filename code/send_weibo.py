import json
import random
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.edge import webdriver
from selenium import webdriver


def get_cookie():
    driver = webdriver.Edge()
    driver.get("https://weibo.com")
    sleep(50)
    with open('cookies.txt','w',encoding='utf-8') as file:
        print("开始存储cookie")
        dictCookies=driver.get_cookies()
        jsonCookies=json.dumps(dictCookies)
        file.write(jsonCookies)
        print("存储完成")
    driver.close()

def set_cookies(driver):
    driver.delete_all_cookies()
    print("删除所有cookie")
    with open('cookies.txt', 'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        for cookie in cookies_list:
            driver.add_cookie(cookie)

def login_(driver):
    driver.get("https://weibo.com/")
    sleep(5)
    set_cookies(driver)
    sleep(1)
    driver.refresh()
    sleep(1)

goodword=['真是太好了','我觉得不错','喜大普奔','你下凡玉帝同意了吗','羡慕了','这也太好看了吧','前无古人，后无来者']
badword=['地狱空荡荡，恶魔在人间','真是醉了','怎么这样啊，太过分了','无语住了','一整个大无语','真的是人干得出来的事吗']
def send_weibo(key,emo,times):
    driver = webdriver.Edge()
    driver.maximize_window()
    login_(driver)
    sleep(5)
    word=''
    for i in range(times):
        if emo == 1:
            x = random.randint(0, len(goodword) - 1)
            print(x, len(goodword))
            word = goodword[x]
        elif emo == -1:
            x = random.randint(0, len(badword) - 1)
            word = badword[x]
        driver.find_element(By.XPATH, '//*[@id="homeWrap"]/div[1]/div/div[1]/div/textarea').send_keys('#'+key+'#'+word+str(i))
        sleep(2)
        driver.find_element(By.XPATH,'//*[@id="homeWrap"]/div[1]/div/div[4]/div/button').click()
        sleep(2)
    sleep(2)
    driver.close()
if __name__ == '__main__':

    send_weibo('哈工大',-1,3)

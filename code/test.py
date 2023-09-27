import json
import random
from re import I
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.edge import webdriver
from selenium import webdriver


def get_cookie():
    driver = webdriver.Edge()

    for i in range(9):
        for j in range(67,93):
            x=str(i)+chr(j)
            url1="https://kaoyandaka.mikecrm.com/8j"+x+"H5K"
            driver.get(url1)

            sleep(5)

    driver.close()

if __name__ == '__main__':

    get_cookie()

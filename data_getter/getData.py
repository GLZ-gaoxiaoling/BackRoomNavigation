import json

from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
import re
import time


class LevelGetter:
    def __init__(self):
        # 初始化selenum
        self.browser = webdriver.Edge()
        self.browser.implicitly_wait(3)
        self.browser.maximize_window()

    def get_exit(self, url):
        self.browser.get(url)

        time.sleep(1)
        elements = self.browser.find_elements(By.XPATH,
                                              "//*[contains(., '出口')][2]/following-sibling::*[not(self::div) and preceding-sibling::*[contains(., '出口')][2]]")

        text = ""
        # 打印所有找到的元素
        for element in elements:
            text += element.text
        # 去除text中多余空格
        text.split()
        # 通过正则匹配text中符合level 一到三位数字 格式的内容
        levels = re.findall(r'Level \d{1,3}', text)
        return levels

    # url是‘self.url = 'http://backrooms-wiki-cn.wikidot.com/level-n'’n的数值为0到999的整数
    def get_level_from_url(self, base_url):
        exits_dist = {}
        for i in range(0, 1000):
            datas = []
            url = f"{base_url}/level-{str(i)}"
            # 清洗数据
            for data in self.get_exit(url):
                if data == f"Level {i}":
                    continue
                else:
                    datas.append(data)
            exits_dist[f"level{i}"] = list(set(datas))
        return exits_dist

    def save_to_sqllite(self, dist):
        conn = sqlite3.connect('level_exit.db')
        cursor = conn.cursor()
        # 创建表
        cursor.execute('CREATE TABLE IF NOT EXISTS levels_table (key TEXT, value TEXT)')
        # 插入数据
        for key, value in dist.items():
            json_value = json.dumps(value)
            cursor.execute('INSERT INTO levels_table (key, value) VALUES (?, ?)', (key, json_value))
        # 提交事务并关闭连接
        conn.commit()
        conn.close()


if __name__ == '__main__':
    level_getter = LevelGetter()
    exit_dist = level_getter.get_level_from_url('http://backrooms-wiki-cn.wikidot.com')
    level_getter.save_to_sqllite(exit_dist)
    level_getter.browser.close()
    level_getter.browser.quit()

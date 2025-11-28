import json
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import re
import time


class LevelGetter:
    def __init__(self):
        # 配置浏览器选项，禁用不必要的功能
        options = webdriver.EdgeOptions()
        # 禁用图片加载
        options.add_argument("--blink-settings=imagesEnabled=false")
        # 禁用JavaScript（根据需要调整，有些网站可能需要JavaScript）
        # options.add_argument("--disable-javascript")
        # 禁用CSS（根据需要调整）
        # options.add_argument("--disable-css")
        # 禁用扩展
        options.add_argument("--disable-extensions")
        # 禁用插件
        options.add_argument("--disable-plugins")
        # 禁用GPU加速
        options.add_argument("--disable-gpu")
        # 禁用沙盒
        options.add_argument("--no-sandbox")
        # 禁用弹窗拦截
        options.add_argument("--disable-popup-blocking")
        # 使用无头模式（根据需要调整）
        # options.add_argument("--headless")
        
        self.browser = webdriver.Edge(options=options)
        self.browser.implicitly_wait(2)  # 减少隐式等待时间
        self.browser.maximize_window()

    def get_exit(self, url, max_retries=3):
        """
        获取楼层出口信息，支持重试
        :param url: 楼层URL
        :param max_retries: 最大重试次数
        :return: 出口楼层列表
        """
        for retry in range(max_retries):
            try:
                self.browser.get(url)
                # 使用显式等待，等待页面内容加载完成
                try:
                    WebDriverWait(self.browser, 5).until(
                        EC.presence_of_element_located((By.ID, "page-content"))
                    )
                except:
                    pass
                
                # 使用更准确的XPath定位出口信息
                elements = self.browser.find_elements(By.XPATH,
                                                  "//div[@id='page-content']//*[contains(., '出口')]/following-sibling::*[not(self::div)][position()<=10]")

                text = ""
                for element in elements:
                    text += element.text
                # 优化正则表达式，支持更多格式的楼层引用
                levels = re.findall(r'Level\s*\d{1,3}', text, re.IGNORECASE)
                # 标准化楼层格式
                levels = [level.title() for level in levels]
                return levels
            except Exception as e:
                print(f"获取出口信息失败，重试 {retry+1}/{max_retries}: {e}")
                time.sleep(1)
        # 重试多次失败后返回空列表
        return []

    def get_level_info(self, url, max_retries=3):
        """
        获取楼层详细信息，支持重试
        :param url: 楼层URL
        :param max_retries: 最大重试次数
        :return: 楼层信息字典
        """
        for retry in range(max_retries):
            try:
                self.browser.get(url)
                # 使用显式等待，等待页面内容加载完成
                try:
                    WebDriverWait(self.browser, 5).until(
                        EC.presence_of_element_located((By.ID, "page-content"))
                    )
                except:
                    pass
                
                # 获取楼层介绍
                try:
                    # 使用更准确的XPath定位楼层介绍
                    description_element = self.browser.find_element(By.XPATH, "//div[@id='page-content']/div[@class='lang-cn sd-container']/p[1]")
                    description = description_element.text.strip()
                except:
                    # 备用定位方式
                    try:
                        description_element = self.browser.find_element(By.XPATH, "//div[@id='page-content']/p[1]")
                        description = description_element.text.strip()
                    except:
                        description = "暂无介绍"
                
                # 获取楼层等级（生存难度）
                try:
                    # 根据网页源码，生存难度信息在top-box中
                    difficulty_element = self.browser.find_element(By.XPATH, "//div[@class='top-box']//div[@class='bottom-text']")
                    difficulty_text = difficulty_element.text.strip()
                    # 提取数字部分
                    difficulty_match = re.search(r'\d+', difficulty_text)
                    difficulty = int(difficulty_match.group()) if difficulty_match else 0
                except:
                    # 备用定位方式
                    try:
                        difficulty_element = self.browser.find_element(By.XPATH, "//*[contains(., '生存难度') or contains(., '生产难度')]/following-sibling::*[1]")
                        difficulty_text = difficulty_element.text.strip()
                        difficulty_match = re.search(r'\d+', difficulty_text)
                        difficulty = int(difficulty_match.group()) if difficulty_match else 0
                    except:
                        difficulty = 0
                
                return {
                    'description': description,
                    'difficulty': difficulty
                }
            except Exception as e:
                print(f"获取楼层信息失败，重试 {retry+1}/{max_retries}: {e}")
                time.sleep(1)
        # 重试多次失败后返回默认信息
        return {
            'description': "暂无介绍",
            'difficulty': 0
        }

    def get_level_range_from_url(self, base_url, start, end):
        """爬取指定范围内的楼层数据"""
        exits_dist = {}
        level_info_dist = {}
        
        for i in range(start, end + 1):
            print(f"正在爬取 Level {i}...")
            datas = []
            url = f"{base_url}/level-{str(i)}"
            
            # 获取出口数据
            for data in self.get_exit(url):
                if data == f"Level {i}":
                    continue
                else:
                    datas.append(data)
            exits_dist[f"level{i}"] = list(set(datas))
            
            # 获取楼层详细信息
            level_info = self.get_level_info(url)
            level_info_dist[f"level{i}"] = level_info
        
        return exits_dist, level_info_dist

    def close(self):
        """关闭浏览器"""
        self.browser.close()
        self.browser.quit()

    def save_to_sqllite(self, exits_dist, level_info_dist):
        conn = sqlite3.connect('level_exit.db')
        cursor = conn.cursor()
        
        # 创建出口表
        cursor.execute('CREATE TABLE IF NOT EXISTS levels_table (key TEXT PRIMARY KEY, value TEXT)')
        
        # 创建楼层信息表
        cursor.execute('CREATE TABLE IF NOT EXISTS level_info (level_id TEXT PRIMARY KEY, description TEXT, difficulty INTEGER)')
        
        # 清空现有数据
        cursor.execute('DELETE FROM levels_table')
        cursor.execute('DELETE FROM level_info')
        
        # 插入出口数据
        for key, value in exits_dist.items():
            json_value = json.dumps(value)
            cursor.execute('INSERT OR REPLACE INTO levels_table (key, value) VALUES (?, ?)', (key, json_value))
        
        # 插入楼层信息数据
        for level_id, info in level_info_dist.items():
            cursor.execute('INSERT OR REPLACE INTO level_info (level_id, description, difficulty) VALUES (?, ?, ?)', 
                          (level_id, info['description'], info['difficulty']))
        
        # 提交事务并关闭连接
        conn.commit()
        conn.close()


def crawl_level_range(base_url, start, end):
    """爬取指定范围的楼层数据，用于多线程"""
    getter = LevelGetter()
    try:
        exits_dist, level_info_dist = getter.get_level_range_from_url(base_url, start, end)
        return exits_dist, level_info_dist
    finally:
        getter.close()


if __name__ == '__main__':
    base_url = 'http://backrooms-wiki-cn.wikidot.com'
    
    # 优化分区策略，使用更灵活的区间划分
    total_levels = 999
    interval = 200  # 每个线程处理200个楼层
    ranges = [(i+1, min(i+interval, total_levels)) for i in range(0, total_levels, interval)]
    
    all_exits_dist = {}
    all_level_info_dist = {}
    
    # 优化线程池配置，根据系统资源调整并发数
    max_workers = min(5, len(ranges))  # 最多使用5个线程
    print(f"使用 {max_workers} 个线程进行并发爬取")
    
    # 使用线程池执行并发爬取
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务
        future_to_range = {
            executor.submit(crawl_level_range, base_url, start, end): (start, end)
            for start, end in ranges
        }
        
        # 获取结果
        completed = 0
        total = len(future_to_range)
        for future in concurrent.futures.as_completed(future_to_range):
            start, end = future_to_range[future]
            try:
                exits_dist, level_info_dist = future.result()
                # 合并结果
                all_exits_dist.update(exits_dist)
                all_level_info_dist.update(level_info_dist)
                completed += 1
                print(f"区间 {start}-{end} 爬取完成，进度: {completed}/{total}")
            except Exception as exc:
                print(f"区间 {start}-{end} 爬取失败: {exc}")
                completed += 1
    
    # 保存到数据库
    print("正在保存数据到数据库...")
    getter = LevelGetter()
    getter.save_to_sqllite(all_exits_dist, all_level_info_dist)
    getter.close()
    print(f"所有数据爬取完成并保存到数据库！共爬取 {len(all_exits_dist)} 个楼层")

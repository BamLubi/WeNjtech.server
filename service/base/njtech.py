import requests
import json
import redis
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .config import Config

# 设置日志属性
logging.basicConfig(level=logging.INFO, filename='/www/wwwroot/develop/weNjtech/logs/python.log', filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

class Njtech:
    def __init__(self, username, password):
        # 设置 selenium 浏览器
        # self.browser = webdriver.Chrome(options=chrome_options)
        # self.wait = WebDriverWait(self.browser, 5)
        # 设置用户名和密码
        self.username = username
        self.password = password
        # 是否登录
        self.isLogin = False
        # 尝试登录次数
        self.tryTimes = 0
        # 网络请求参数
        self.cookies = None
        self.config = Config(self.username)
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.130 Safari/537.36 "
        }
        # 跳转登录
        self.login()

    def check_login(self):
        return self.isLogin

    def login(self):
        # 如果已经登录，就返回
        if self.check_login():
            return
        # 查询redis
        cookie = r.get(self.username)
        if cookie != None:
            logging.info("Redis已存在cookie:"+cookie)
            self.cookies = json.loads(cookie)
            self.isLogin = True
            return
        logging.info("Redis不存在cookie,登录中...")
        # 初始化浏览器
        self.browser = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 5)
        # 登录
        try:
            # 1. 进入教务处页面
            self.browser.get(self.config.login_url)
            # 2. 获取组件，并填写相应信息
            yhm = self.browser.find_element_by_id('yhm')
            yhm.send_keys(self.username)
            mm = self.browser.find_element_by_id('mm')
            mm.send_keys(self.password)
            # 点击按钮
            button = self.browser.find_element_by_id('dl')
            button.click()
            self.wait.until(EC.presence_of_element_located((By.ID, 'area_five')))
            self.cookies = {
                'JSESSIONID': self.browser.get_cookies()[0].get('value')
            }
            self.isLogin = True
            r.set(self.username, json.dumps(self.cookies), ex=600*2)
            logging.info("登录成功,写入Redis: "+json.dumps(self.cookies))
        except Exception as e:
            if self.tryTimes < 1:
                self.tryTimes += 1
                logging.info("第一次登录失败,尝试重新登录")
                return self.login()
            print("登录失败")
        finally:
            self.browser.close()

    def get_kebiao(self):
        # 判断是否登录
        if not self.check_login():
            logging.info("查询课表:未登录")
            self.login()
        # 获取课表
        try:
            data = {
                'xnm': '2018',
                'xqm': '3',
                'kzlx': 'ck'
            }
            response = self.get_request('POST', self.config.kebiao_url, data)
            return response
        except Exception as e:
            print("获取课表失败", e)
    
    def get_classroom(self, year, term, term_week, week, time):
        # 判断是否登录
        if not self.check_login():
            logging.info("查询空教室:未登录")
            self.login()
        # 获取课表
        try:
            data = {
                'fwzt': 'cx',
                'xqh_id': 1,
                'xnm': year,
                'xqm': term,
                'jyfs': 0,
                'zcd': term_week,
                'xqj': week,
                'jcd': time,
                'queryModel.showCount': 1,
                'queryModel.currentPage': 1
            }
            ## 获取总共有多少数据,再次请求
            response = self.get_request('POST', self.config.classroom_url, data)
            total_count = response["totalCount"]
            if not isinstance(total_count, int):
                total_count = 15
            ## 再次请求
            data["queryModel.showCount"] = total_count
            response = self.get_request('POST', self.config.classroom_url, data)
            return response
        except Exception as e:
            logging.error("获取空教室失败",e)

    def get_request(self, method, url, data):
        """
        发起网络请求
        :param method: 请求方式 'GET'或'POST'
        :param url: 地址
        :param data: 附带参数
        :return:
        """
        response = requests.request(method, url, data=data, headers=self.header, cookies=self.cookies)
        return json.loads(response.content.decode('utf-8'))


if __name__ == '__main__':
    njtech = Njtech("1405170121", "1999819lyy")
    # print(njtech.check_login())
    # njtech.get_kebiao()
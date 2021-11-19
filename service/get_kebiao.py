import json
from requests.models import Response
from base.njtech import Njtech
from base.wechatApp import WechatApp
from base import R
import sys
import logging
import re
import time

# 设置日志属性
logging.basicConfig(level=logging.INFO, filename='/www/wwwroot/develop/weNjtech/logs/python.log', filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# 云端存储数据的集合名
collection_name = 'weNjtech-kebiao'

class Kebiao:
    def __init__(self, username, password, year, term):
        # 查询学年、学期
        self.year = year
        self.term = term
        # 课表列表
        self.kebiaoList = []
        # 完整的存储数据
        self.post_data = None
        # 连接器
        self.njtech = Njtech(username, password)

    def get_kebiao(self):
        response = self.njtech.get_kebiao(self.year, self.term)
        response = response["kbList"]
        # 只取必要的字段
        for item in response:
            kebiao = {
                'id': item["kch"],
                'course_name': item["kcmc"],
                'address': item["cdmc"],
                'time': item["jcs"],
                'teacher': item["xm"],
                'week': item["xqjmc"],
                'campus': item["xqmc"],
                'term_week': item["zcd"],
                'require': item["kcxszc"],
                'type': item["kcxz"],
                'kclb': item["kclb"]
            }
            ## 追加进数组
            self.kebiaoList.append(kebiao)
    
    def clean_data(self):
        # 遍历数据
        for item in self.kebiaoList:
            ## 解析week为数字
            item["week"] = self.week2int(item["week"])
            ## 正则拆分上课时间
            pattern = "([0-9]+)-([0-9]+)"
            res = re.compile(pattern).findall(item["time"])
            item["time"] = [int(res[0][0]),int(res[0][1])]
            ## 正则拆分教学周
            item["term_week_str"] = item["term_week"]
            pattern = "([0-9]+)-([0-9]+)周"
            res = re.compile(pattern).findall(item["term_week"])
            item["term_week"] = []
            for _item in res:
                for i in range(int(_item[0]), int(_item[1])+1):
                    item["term_week"].append(i)
        # 测试用输出
        # logging.info(self.kebiaoList)
    
    @staticmethod
    def week2int(target):
        week = {"星期一": 1, "星期二": 2, "星期三": 3, "星期四": 4, "星期五": 5, "星期六": 6, "星期日": 7}
        ans = week.get(target)
        return ans if ans != None else 0
    
    def write_kebiao(self, file):
        """
        写入文件
        """
        try:
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(self.post_data, ensure_ascii=False) + '\n')
        except IOError as e:
            logging.error("Write Kebiao File FAILURE!"+str(e))
            return False
        else:
            logging.info("Write Kebiao File SUCCESS!")
            return True

    def make_post_data(self, openid):
        _post_data = {
            "_id": str(openid),
            "_openid": str(openid),
            "year": int(self.year),
            "term": int(self.term),
            "data": self.kebiaoList,
            "update_time": int(time.time())
        }
        self.post_data = _post_data

if __name__ == '__main__':
    try:
        # 1. 获取传入参数
        username = sys.argv[1]
        password = sys.argv[2]
        openid = sys.argv[3]
        query_year = sys.argv[4]
        query_term = sys.argv[5]
        # query_year = '2018'
        # query_term = '3'
        file_name = str(username) + '-' + str(query_year) + '-' + str(query_term) + '.json'
        file_path = '/www/wwwroot/develop/weNjtech/static/kebiao/' + file_name
        logging.info("username: "+username+", password: "+password+", query_year: "+query_year+", query_term: "+query_term)
        # 2. 初始化查询课表对象
        kebiao = Kebiao(username, password, query_year, query_term)
        # 3. 获取课表信息
        logging.info("Getting "+str(username)+" kebiao...")
        kebiao.get_kebiao()
        # 4. 数据清洗
        logging.info("Cleaning Data...")
        kebiao.clean_data()
        # 5. 构造请求数据
        logging.info("Making post data...")
        kebiao.make_post_data(openid)
        # 6. 保存至文件
        logging.info("Saving to local storage...")
        kebiao.write_kebiao(file_path)
        # 7. 保存至小程序云数据库
        logging.info("Saving to wechat miniprogram cloud database...")
        if not WechatApp(file_path, collection_name).upload_kebiao(file_name):
            raise Exception("保存至小程序云数据库错误")
        print(R.OK(kebiao.post_data, '查询课表成功'))
    except Exception as e:
        logging.info("查询课表失败"+str(e))
        print(R.FAIL(str(e), '查询课表失败'))
import json
from base.njtech import Njtech
from base import R
from base.wechatApp import WechatApp
import sys
import re
import logging
import datetime
import subprocess
import time

# 设置日志属性
logging.basicConfig(level=logging.INFO, filename='/www/wwwroot/develop/weNjtech/logs/python.log', filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# 定义当前日期 如'20200504'
now_date = str(datetime.datetime.now().strftime('%Y%m%d'))
# 处理后的数据
file_name = now_date + '.json'
file_path = '/www/wwwroot/develop/weNjtech/static/classroom/' + file_name
# 云端存储数据的集合名
collection_name = 'weNjtech-classroom'

class Classroom:
    def __init__(self, username, password, year, term, term_week, week):
        # 查询节次，需要遍历查询，然后组合
        self.time = [3, 12, 48, 192, 768]
        # 查询学年、学期、周次、星期
        self.year = year
        self.term = term
        self.term_week = term_week
        self.week = week
        # 空教室列表
        self.classroomList = []
        # 场地类别
        self.cdlb = {
            '004': '阶梯教室',
            '005': '阶梯教室',
            '007': '中教室',
            '009': '小教室',
            '011': '阶梯教室'
        }
        # 连接器
        self.njtech = Njtech(username, password)
    
    def get_classroom(self):
        for item in self.time:
            logging.info("获取节次" + str(item))
            response = self.njtech.get_classroom(self.year, self.term, self.term_week, self.week, item)
            ## 返回类型未<list>且这个数据很大在200多个
            response = response["items"]
            ## 只取必要的字段
            for _item in response:
                classroom = {
                    '_id': _item["cd_id"],
                    'cdlb_id': _item["cdlb_id"],
                    'lh': _item["lh"],
                    'name': _item["cdmc"],
                    'emptyTime': item
                }
                ### 追加进数组
                self.classroomList.append(classroom)
    
    def clean_data(self):
        _classroomList = []
        # 对数据排序
        self.classroomList.sort(key=self.sort_by_id)
        # 遍历数据
        for item in self.classroomList:
            ## 对不符合要求的数据剔除
            if item["lh"] == None or item["lh"] == "" or item["lh"] == " ":
                continue
            if item["cdlb_id"] not in self.cdlb:
                continue
            target = list(filter(lambda x: x["_id"]==item["_id"], _classroomList))
            # 判断是否已经存在
            if len(target):
                # 教室已经存在，将空时间加上去
                target[0]['emptyTime'] += self.emptytime2list(item['emptyTime'])
            else:
                # 教室不存在
                _classroomList.append(self.make_classroom(item))
        # 覆写全局数据
        self.classroomList = _classroomList
        ## 测试用logging
        # logging.info(_classroomList)
    
    @staticmethod
    def sort_by_id(elem):
        """
        排序算法
        :param elem: list元素
        :return:
        """
        return elem['_id']
    
    @staticmethod
    def emptytime2list(empty_time):
        """
        将获取的空闲时间转换成列表
        :param empty_time: 空闲时间
        :return:
        """
        if empty_time == 3:
            return [1, 2]
        elif empty_time == 12:
            return [3, 4]
        elif empty_time == 48:
            return [5, 6]
        elif empty_time == 192:
            return [7, 8]
        elif empty_time == 768:
            return [9, 10]
        else:
            return []
    
    def make_classroom(self, empty_classroom):
        """
        将空教室插入资源列表
        1. 重新处理楼号、教室名、空闲时间
        :param empty_classroom: 原始空教室对象
        """
        # 1. 正则拆分教室
        pattern = "(.*?)([0-9][0-9][0-9])"
        res = re.compile(pattern).findall(empty_classroom["name"])
        empty_classroom["name"] = res[0][1]  # 修改教室名为门牌号
        empty_classroom["lh"] = res[0][0]  # 修改lh为具体楼
        # 如果教室名称前两位为“笃学”，则改为“浦江”
        empty_classroom["lh"] = empty_classroom["lh"].replace("笃学", "浦江")
        # 2. 修改场地类别为具体内容
        empty_classroom["cdlb_id"] = self.cdlb[empty_classroom["cdlb_id"]]
        # 3. 修改空闲时间为列表
        empty_classroom["emptyTime"] = self.emptytime2list(empty_classroom["emptyTime"])
        # 4. 修改楼层为教室名的第一个字段
        empty_classroom["lc"] = int(empty_classroom["name"][0])
        # 5. 返回空教室对象
        return empty_classroom
    
    def write_classroom(self):
        """
        空教室写入文件
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for item in self.classroomList:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
        except IOError as e:
            logging.error("Write Classroom File FAILURE!"+str(e))
            return False
        else:
            logging.info("Write Classroom File SUCCESS!")
            return True

if __name__ == '__main__':
    try:
        # 1. 获取传入参数
        username = sys.argv[1]
        password = sys.argv[2]
        year = sys.argv[3]
        term = sys.argv[4]
        term_week = sys.argv[5]
        week = sys.argv[6]
        logging.info("username: "+username+", password: "+password+", year: "+year+", term: "+term+", term_week: "+term_week+", week: "+week)
        # 2. 初始化查询教室对象
        classroom = Classroom(username, password, year, term, term_week, week)
        # 3. 获取所有空教室信息
        logging.info("Getting classroom...")
        classroom.get_classroom()
        # 4. 清洗数据
        logging.info("Cleaning data...")
        classroom.clean_data()
        # 5. 保存至文件
        logging.info("Saving to local storage...")
        classroom.write_classroom()
        # 6. 判断是否数据长度为0，若为0，则重新执行程序
        if len(classroom.classroomList) == 0:
            logging.info("数据长度为0! 休眠后重新执行...")
            time.sleep(300)
            subprocess.call("/www/wwwroot/develop/weNjtech/shell/autorun_classroom.sh", shell=True)
            exit()
        # 7. 保存至小程序云数据库
        logging.info("Saving to wechat miniprogram cloud database...")
        if not WechatApp(file_path, collection_name).upload_classroom(file_name, len(classroom.classroomList)):
            raise Exception("保存至小程序云数据库错误")
        # 8. 返回信息
        print(R.OK('success', '查询课表成功'))
    except Exception as e:
        logging.info("查询课表失败"+str(e))
        print(R.FAIL(str(e), '查询课表失败'))
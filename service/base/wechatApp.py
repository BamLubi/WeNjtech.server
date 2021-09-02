import json
import requests
import datetime
import logging

# 设置日志属性
logging.basicConfig(level=logging.INFO, filename='日志文件路径', filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class WechatApp:
    def __init__(self, filename, collectionname):
        # 初始化变量
        self.grant_type = 'client_credential'
        self.appid = '小程序APPID'
        self.secret = '小程序SECRET'
        self.env = '小程序云环境ID'
        self.src_file = filename
        self.collectionname = collectionname
        self.access_token = ''
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.130 Safari/537.36 "
        }
        self.wxAPI_url = {
            'access_token': ['GET', 'https://api.weixin.qq.com/cgi-bin/token?grant_type={}&appid={}&secret={}'],
            'upload_file': ['POST', 'https://api.weixin.qq.com/tcb/uploadfile?access_token={}'],
            'db_import': ['POST', 'https://api.weixin.qq.com/tcb/databasemigrateimport?access_token={}'],
            'del_collection': ['POST', 'https://api.weixin.qq.com/tcb/databasecollectiondelete?access_token={}'],
            'add_collection': ['POST', 'https://api.weixin.qq.com/tcb/databasecollectionadd?access_token={}'],
            'update_database': ['POST', 'https://api.weixin.qq.com/tcb/databaseupdate?access_token={}'],
        }
        self.finish_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_request(self, method, url, data):
        """
        发起网络请求
        :param method: 请求方式 'GET'或'POST'
        :param url: 地址
        :param data: 附带参数
        :return:
        """
        response = requests.request(method, url, json=data, headers=self.header)
        return json.loads(response.content.decode('utf-8'))

    def get_access_token(self):
        """
        获取access_token
        :return:
        """
        option = self.wxAPI_url['access_token']
        # 1. 构造url
        url = option[1].format(self.grant_type, self.appid, self.secret)
        # 2. 发送请求
        content = self.get_request(option[0], url, '')
        # 3. 赋值
        self.access_token = content['access_token']

    def upload_file(self, filepath, savepath):
        """
        上传文件
        :param filepath: 本地源文件路径
        :param savepath: 云端保存文件路径
        :return:
        """
        # 输出日志
        logging.info("Uploading File ......")
        logging.info("Local File Path: " + filepath)
        logging.info("Cloud File Path: " + savepath)
        # 1. 构造url
        option = self.wxAPI_url['upload_file']
        url = option[1].format(self.access_token)
        # 2. 构造请求参数
        data = {'env': self.env, 'path': savepath}
        # 3. 发送请求
        content = self.get_request(option[0], url, data)
        # 4. 判断结果
        if content['errcode'] == 0:
            # 成功
            logging.info("Upload File Part 1 SUCCESS!")
            file = {"file": open(filepath, "rb")}
            # 二次请求
            url = content["url"]
            data = {
                'key': savepath,
                'Signature': content["authorization"],
                'x-cos-security-token': content["token"],
                'x-cos-meta-fileid': content["cos_file_id"]
            }
            response = requests.post(url, data=data, headers=self.header, files=file)
            if response.status_code == 204:
                logging.info("Upload File Part 2 SUCCESS!")
                return True
            else:
                logging.error("Upload File Part 2 FAILURE!")
                return False
        else:
            logging.error("Upload File Part 1 FAILURE!")
            return False

    def db_import(self, cloud_fileid):
        """
        数据库导入
        :return:
        """
        # 输出日志
        logging.info("Importing Database ......")
        # 1. 构造url
        option = self.wxAPI_url['db_import']
        url = option[1].format(self.access_token)
        # 2. 构造请求参数
        data = {
            "env": self.env,
            "collection_name": self.collectionname,
            "file_path": cloud_fileid,
            "file_type": 1,
            "stop_on_error": False,
            "conflict_mode": 2
        }
        # 3. 发送请求
        content = self.get_request(option[0], url, data)
        # 4. 判断结果
        if content['errcode'] == 0:
            # 成功
            logging.info("Importing Database SUCCESS!")
            return True
        else:
            logging.error("Importing Database FAILURE!")
            return False

    def del_collection(self):
        """
        删除集合
        :return:
        """
        # 输出日志
        logging.info("Deleting Collection ......")
        # 1. 构造url
        option = self.wxAPI_url['del_collection']
        url = option[1].format(self.access_token)
        # 2. 构造请求参数
        data = {
            "env": self.env,
            "collection_name": self.collectionname,
        }
        # 3. 发送请求
        content = self.get_request(option[0], url, data)
        # 4. 判断结果
        if content['errcode'] == 0:
            logging.info("Delete Collection SUCCESS!")
            return True
        else:
            logging.error("Delete Collection FAILURE!")
            return False

    def add_collection(self):
        """
        新增集合
        :return:
        """
        # 输出日志
        logging.info("Adding Collection ......")
        # 1. 构造url
        option = self.wxAPI_url['add_collection']
        url = option[1].format(self.access_token)
        # 2. 构造请求参数
        data = {
            "env": self.env,
            "collection_name": self.collectionname,
        }
        # 3. 发送请求
        content = self.get_request(option[0], url, data)
        # 4. 判断结果
        if content['errcode'] == 0:
            # 成功
            logging.info("Add Collection SUCCESS!")
            return True
        else:
            logging.error("Add Collection FAILURE!")
            return False

    def update_database(self, query):
        """
        更新记录
        :return:
        """
        # 输出日志
        logging.info("Updating Database ......")
        # 1. 构造url
        option = self.wxAPI_url['update_database']
        url = option[1].format(self.access_token)
        # 2. 构造请求参数
        data = {
            "env": self.env,
            "query": query,
        }
        # 3. 发送请求
        content = self.get_request(option[0], url, data)
        # 4. 判断结果
        if content['errcode'] == 0:
            # 成功
            logging.info("Update Database SUCCESS!")
            return True
        else:
            logging.error("Update Database FAILURE!")
            return False

    def check_environment(self):
        # 若本地access_token为空，则获取
        if self.access_token == '':
            return self.get_access_token()

    def upload_classroom(self, file_name, count):
        """
        上传空教室
        :param file_name: 文件名
        :return:
        """
        # 1. 确保有access_token，时效2小时
        self.check_environment()
        # 2. 上传文件，获取cloudid
        file_path = 'weNjtech/classroom/' + file_name
        if not self.upload_file(self.src_file, file_path):
            return False
        # 3. 删除云端集合
        if not self.del_collection():
            return False
        # 4. 修改公共字典，锁，根据情况自己设计
        query_str = "db.collection(\"publicDict\").doc(\"dict003\").update({data: {isAvailable: false, notice: \"数据维护中\"}})"
        if not self.update_database(query_str):
            return False
        # 5. 新增云端集合
        if not self.add_collection():
            return False
        # 6. 数据导入集合
        if not self.db_import(file_path):
            return False
        # 7. 修改公共字典，释放锁，根据情况自己设计
        query_str = "db.collection(\"publicDict\").doc(\"dict003\").update({data: {isAvailable: true, count:" + str(
            count) + ",time:\"" + self.finish_time + "\"}})"
        if not self.update_database(query_str):
            return False
        # 8. 处理成功,返回
        return True
    
    def upload_kebiao(self, file_name):
        """
        上传课表
        :param date: 当前的日期
        :return:
        """
        # 1. 确保有access_token，时效2小时
        self.check_environment()
        # 2. 上传文件，获取cloudid
        file_path = 'weNjtech/kebiao/' + file_name
        if not self.upload_file(self.src_file, file_path):
            return False
        # 6. 数据导入集合
        if not self.db_import(file_path):
            return False
        # 8. 处理成功,返回
        return True
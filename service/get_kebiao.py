import json
from base.njtech import Njtech
from base import R
import sys
import logging

# 设置日志属性
logging.basicConfig(level=logging.INFO, filename='/www/wwwroot/develop/weNjtech/logs/python.log', filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

try:
    # 1. 获取传入参数
    username = sys.argv[1]
    password = sys.argv[2]
    logging.info("username: "+username+", password: "+password)
    # 2. 初始化连接器
    njtech = Njtech(username, password)
    # 3. 查询课表
    logging.info("查询课表中...")
    response = njtech.get_kebiao()
    # 4. 数据清洗
    ## 获取所有课程
    response = response["kbList"]
    ## 根据课程号归类
    logging.info("查询课表成功")
    print(R.OK(response, '查询课表成功'))

except Exception as e:
    logging.info("查询课表失败")
    print(R.FAIL(str(e), '查询课表失败'))
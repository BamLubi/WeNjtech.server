from base.njtech import Njtech
from base import R
import sys
import logging

# 设置日志属性
logging.basicConfig(level=logging.INFO, filename='../logs/python.log', filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

try:
    # 1. 获取传入参数
    username = sys.argv[1]
    password = sys.argv[2]
    logging.info("username: "+username+", password: "+password)
    logging.info("登录中...")
    # 2. 初始化连接器
    njtech = Njtech(username, password)
    # 3. 判断是否登录
    if njtech.check_login():
        logging.info("登录成功")
        print(R.OK('', '登陆成功'))
    else:
        raise Exception("账号密码错误")
except Exception as e:
    logging.info("登录失败")
    print(R.FAIL(str(e), '登录失败'))


class Config:
    def __init__(self, username='username'):
        self.login_url = 'https://jwgl.njtech.edu.cn/xtgl/login_slogin.html'
        self.kebiao_url = 'https://jwgl.njtech.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151&su=' + username
        self.classroom_url = 'https://jwgl.njtech.edu.cn/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'
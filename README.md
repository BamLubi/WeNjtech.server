# “微南工”小程序后端解决方案

> 后端主要功能包括：
>
> - 自动爬取教务处空闲教室信息
> - 爬取指定用户当前学年课表信息
>
> 主要思路：使用selenium模拟登录教务处获得关键的Cookies并存入Redis，后续的网络请求使用该Cookies获得空教室信息和课表信息。
>
> 不同学校的教务处网站设计不同，爬取方案也不用。因此本项目只提供了一种解决方案，完全照搬将无法运行。本项目只适用于南京工业大学的教务处系统。

## 目录结构

```shell
├─logs # 日志
├─service # 爬虫服务
├─shell # 自动运行脚本
├─static # 静态资源存储
└─*.php # 对外调用服务
```

## 环境

请确保已经配置好如下开发环境：

- python、php
- 安装``chromedriver.exe`放置到`/service/base`目录下
- 安装python相关环境，`pip install -r requirement.txt`

## 使用指南

> 代码中已经注释教务处账号密码，微信小程序密钥等信息，需要开发者自行添加

1. 修改`/get_classroom.php line5-6`，填写教务处账号和密码。
2. 修改`/service/get_classroom.py line21`，填写微信小程序云开发数据库中存储**空教室**信息的表名。
3. 修改`/service/get_kebiao.py line15`，填写微信小程序云开发数据库中存储**课表**信息的表名。
4. 修改`/service/base/wechatApp.py line15-17`，填写微信小程序云开发**APPID**、**APPSECRET**、**CLOOUD-ENV**。

## 版权信息

该项目签署了[MIT 授权许可](http://www.opensource.org/licenses/mit-license.php)，详情请参阅 [LICENSE](./LICENSE)
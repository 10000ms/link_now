# link_now 聊天室
tornado框架的聊天网站

# 启动
1.根据需求配置config.py文件

2.启动
```
python server.py
```
# 需要数据库
- Redis （记录当前用户登陆信息）
- MongoDB （记录注册用户信息）

# 部分界面截图

![主页](https://note.youdao.com/yws/api/personal/file/C4C3ADB9863340A7ACB52AB2D24CDF86?method=download&shareKey=6918c133f42203868e1ab05680ffb775)

![注册](https://note.youdao.com/yws/api/personal/file/22E53721DA8C4181B66EDC0C78890FC0?method=download&shareKey=ad1dbc4108f3705092d871a60f394cba)

![登陆](https://note.youdao.com/yws/api/personal/file/55B4CB6D6C2F4907AA9422F5A80191EF?method=download&shareKey=f758b3f69bcfac6ae0aaf7569371a8db)

![聊天室](https://note.youdao.com/yws/api/personal/file/152F03DC22F749B5A52FF7E6A07F1E97?method=download&shareKey=4ee9ffb44d59d09b01da9818f54d54b9)

# requirements
pymongo==3.6.1
redis==2.10.6
tornado==5.0.2


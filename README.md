## 简介

这个项目根据cnblog的url`http://www.cnblogs.com/[ID]/articles/[文章ID].html`来爬取单个用户的每个文章  
实际速度并不快，建议指定好`文章ID`范围  
本项目会把得到的文章链接/标题输出到当前目录下的`ResLog.log`文件内。

## 代码示例

### 作为模块调用

```python
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import CNBlogSpider

# 建立对象，设置用户名为'testusername'，从文章ID 1000000开始到1000100结束，同时运行100个线程
cnbs = CNBlogSpider.cnBLogSpider("testusername", 1000000,1000100,100)
# 开始爬行
cnbs.run()
```

### 作为程序执行

```shell
python3 main.py 'testusername' 1000000 1000100 100
```



## 安装

需要注意的是本项目需要requests模块的支持，在运行前请不要忘记安装下列模块 

```shell
# 尝试 
pip install requests
# 或尝试
python -m pip install requests
```

`命令执行失败大多数情况都是环境变量没有配置好`

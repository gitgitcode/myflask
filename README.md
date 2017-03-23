# myflask
python-flask

## Flask + WSGI + Nginx 配置

### pip
- apt-get install pip

### VirtualEnv
    (VirtualEnv)[https://virtualenv.readthedocs.org/en/latest/]  可以为每个Python应用创建独立的开发环境

    - pip install virtualenv

    安装VirtualEnv 后只需要在项目目录内运行 virtualenv 目录名 就可以建立一个虚拟环境文件夹，然后启用 activate 指令即可启用该python虚拟环境，具体操作如下：

    假定我的项目目录叫 /home/www/my_flask，首先安装虚拟环境 (我习惯使用的虚拟环境目录叫 venv )

    ```
    my_flask root$ virtualenv venv

    >> New python executable in venv/bin/python
    >> Installing setuptools, pip...done.
    ```

    在项目目录下就会建立一个新的 venv 目录，里面就是运行python 的基本环境的工具与指令，和包。 然后启用该环境，使用当前命令行状态进入虚拟环境，进入虚拟环境后，一切安装python的操作都会将包和引用装在虚拟环境内，而不会影响到全局的python 环境。

    -  my_flask root$ source venv/bin/activate 

    (venv)my_flask root$ 
    调用 ``` activate ```  指令后命令符前就会出现 (venv) 字样。 可通过 ``` deactivate ```退出虚拟环境

    ### uWSGI
安装 Flask
我是用清单文件一次性安装Flask和他的相关依赖的，这样会更快。我的引用清单是这样的：
requirements.txt

Flask==0.10.1
Flask-Login==0.2.11
Flask-Mail==0.9.1
Flask-Moment==0.4.0
Flask-PageDown==0.1.5
Flask-SQLAlchemy==2.0
Flask-Script==2.0.5
Flask-WTF==0.10.2
Flask-Cache==0.13.1
Flask-Restless==0.15.0
Flask-Uploads==0.1.3
Jinja2==2.7.3
Mako==1.0.0
Markdown==2.5.1
MarkupSafe==0.23
SQLAlchemy==0.9.8
WTForms==2.0.1
Werkzeug==0.9.6
html5lib==1.0b3
itsdangerous==0.24
six==1.8.0
awesome-slugify==1.6
可以想像，如果一个一个装非疯了不可。
安装清单文件：

(venv)my_flask root$ pip install -r requirements.txt
在此还是重重地提一下：一定要注意在运行这个安装之前启用了python 虚拟环境，否则会直接安装到全局去的！

项目文件

接下来就是上传 Flask的项目文件，之前我在各大的“转载专业户”里找了好多的资料，在这一步中大多只是在上面加个标准的Flask运行文件，虽说做个范例可以但说实在的这很让人迷惑，为什么？先看看代码吧：

from flask import Flask
 
app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"
生产环境内，谁会用这样的代码呢，这只是Flask 的最简入门范，我的Flask项目中 app 是被做在包内的，相信很多人都是这样做的，在包外我们采用 Flask Script 写一个 manage.py 文件 作为启动文件，这更方便于支持各种的项目，包括可以安装到 window下的 FastCGI 中。

那么我的 这个 manage.py 是这个样子的：

#!/usr/bin/env python
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from flask.ext.script import Manager, Shell

# 通过配置创建 app 
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def deploy():
    """Run deployment tasks."""
    pass


if __name__ == '__main__':
    manager.run()
这样做我地开发环境可以这样运行 Flask:

python manage.py runserver
更详细的做法请参考 [Flask Script|http://flask-script.readthedocs.org/en/latest/] 扩展

好吧，我们可以用 支持SSH的FTP工具将Flask项目文件上传到服务器上，下面是整个项目文件结构：

www/
└── my_flask  
│   ├── logs
│   └── venv  //虚拟目录
│   │   ├── bin
│   │   │         ├── activate
│   │   │         ├── easy_install
│   │   │         ├── gunicorn
│   │   │         ├── pip
│   │   │         └── python
│   │   ├── include
│   │   │          └── python2.7 -> /usr/include/python2.7
│   │   ├── lib
│   │   │         └── python2.7
│   │   ├── local
│   │   │         ├── bin -> /home/shenye/shenyefuli/bin
│   │   │         ├── include -> /home/shenye/shenyefuli/include
│   │   │         └── lib -> /home/shenye/shenyefuli/lib
│   └── app  //Flask 程序目录
│   │           └──  __init__.py //这是程序包文件。这个目录下还有其它的文件此处略过
│   ├── manage.py   
│   ├── requirements.txt                
配置 uwsgi

好了，项目的准备工作已经做完了，是时候回过头去配置 uwsgi 了，它的具体指令可以去看它的官方文档，我们在这里采用其中的一种指令方式：配置起动。我采用 .ini文件作为配置，在项目目录下创建一个 confg.ini （具体见下文）写好后可以这样执行

(venv)my_flask root$ uwsgi config.ini
我认为是最简单的方式，也容易更改。好了重要部分来了，config.ini 是这样写的：

[uwsgi]

# uwsgi 启动时所使用的地址与端口
socket = 127.0.0.1:8001 

# 指向网站目录
chdir = /home/www/ 

# python 启动程序文件
wsgi-file = manage.py 

# python 程序内用以启动的 application 变量名
callable = app 

# 处理器数
processes = 4

# 线程数
threads = 2

#状态检测地址
stats = 127.0.0.1:9191
注意 ： callable=app 这个 app 是 manage.py 程序文件内的一个变量，这个变量的类型是 Flask的 application 类 。

运行 uwsgi

```
(venv)my_flask root$ uwsgi config.ini

[uWSGI] getting INI configuration from config.ini

*** Starting uWSGI 2.0.8 (64bit) on [Fri Dec 19 14:34:11 2014] 
// 此处略去那些无用的启动信息
Stats server enabled on 127.0.0.1:9191 fd: 15 ***
```

OK， 此时已经正常启动 uwsgi 并将 Flask 项目载入其中了，ctrl+c 关闭程序。但这只是命令启动形式，要使其随同服务器启动并作为后台服务运行才是运营环境的实际所需要。因此接下来我们需要安装另一个工具来引导 uwsgi 。

安装 Supervisor

[Supervisor|http://supervisord.org/configuration.html]可以同时启动多个应用，最重要的是，当某个应用Crash的时候，他可以自动重启该应用，保证可用性。

sudo apt-get install supervisor
Supervisor 的全局的配置文件位置在：

/etc/supervisor/supervisor.conf
正常情况下我们并不需要去对其作出任何的改动，只需要添加一个新的 *.conf 文件放在

/etc/supervisor/conf.d/
下就可以，那么我们就新建立一个用于启动 my_flask 项目的 uwsgi 的 supervisor 配置 (命名为：my_flask_supervisor.conf)：
```

    [program:myflask]
    # 启动入口
    command=/home/wwwroot/myflask/venv/bin/uwsgi /home/wwwroot/myflask/config.ini

    # 命令程序所在目录
    directory=/home/wwwroot/myflask/
    #运行命令的用户名
    user=root
            
    autostart=true
    autorestart=true
    #日志地址
    stdout_logfile=/home/wwwroot/myflask/logs/uwsgi_supervisor.log    
```
    
启动服务

sudo service supervisor start
终止服务

sudo service supervisor stop
安装 Nginx
[Nginx|http://nginx.com/]是轻量级、性能强、占用资源少，能很好的处理高并发的反向代理软件。

sudo apt-get install nginx
配置 Nginx

Ubuntu 上配置 Nginx 也是很简单，不要去改动默认的 nginx.conf 只需要将

/ext/nginx/sites-available/default
文件替换掉就可以了。

新建一个 default 文件:

    server {
      listen  80;
      server_name XXX.XXX.XXX; #公网地址
    
      location / {
        include      uwsgi_params;
        uwsgi_pass   127.0.0.1:8001;  # 指向uwsgi 所应用的内部地址,所有请求将转发给uwsgi 处理
        uwsgi_param UWSGI_PYHOME /home/www/my_flask/venv; # 指向虚拟环境目录
        uwsgi_param UWSGI_CHDIR  /home/www/my_flask; # 指向网站根目录
        uwsgi_param UWSGI_SCRIPT manage:app; # 指定启动程序
      }
    }
将default配置文件替换掉就大功告成了！
还有，更改配置还需要记得重启一下nginx:

sudo service nginx restart
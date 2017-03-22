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

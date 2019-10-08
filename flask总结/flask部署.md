## 1.安装python3

1.安装python依赖包

```shell
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make -y
```

2.下载python3安装包

```sehll
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
```

3.解压安装包

```shell
tar -xvJf Python-3.5.2.tar.xz
```

4.进入目录，进行编译安装

```shell
 cd Python-3.5.2/
 ./configure prefix=/usr/local/python3
 make && make install
```

5.配置环境变量

```shell
# 建立python3的软连接
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
# 建立pip3的软件链接
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3

```

6.输入python3 查看效果

## 2.安装配置uwsgi

```
pip3 install uwsgi
```

创建软链接

```
ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi
```

创建uwsgi配置文件

```
mkdir script
cd script/
touch uwsgi.ini
```

编写uwsgi配置文件

```
vim  uwsgi.ini
[uwsgi]
socket=10.10.14.80:8000
pythonpath=/opt/FlaskOA
module=manage
wsgi-file=/opt/FlaskOA/manage.py
callable=app
processes=4
threads=2
daemonize=/opt/script/uwsgi.1og
```

启动uwsgi

```
uwsgi --ini uwsgi.ini
```

可以查看到配置文件目录下，多出uwsgi.1og文件，目前无法通过访问网站判断启动成功。继续配置nginx

## 3.配置NGINX

1.下载nginx

```
wget -c  https://nginx.org/download/nginx-1.8.1.tar.gz
```

2.解压安装

```
#解压
tar -zxvf nginx-1.8.1.tar.gz
#编译配置
./configure \ 
#编译安装
make && make install
```

3.创建软链接

```
ln -s /usr/local/nginx/sbin/nginx /usr/bin/nginx
```

4.启动nginx，访问ip，如果出现welcom to nginx，则安装成功

```
# 启动nginx
nginx 
```

## 4.部署项目

1.上传项目

2.配置nginx服务器执行flask的uwsgi

```
server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;
        access_log  /opt/script/host.access.log;
        error_log  /opt/script/error.log;
        
        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8000;
        
            uwsgi_param UWSGI_CHDIR /opt/FlaskOA;
            uwsgi_param UWSGI_SCRIPT manage:app;
        }

```

说明

- listen — 表示监听的端口
- server_name — 表示服务名称(有域名可以换成域名)
- access_log   —服务器接收的请求日志
- error_log   — nginx失败了的错误日志文件地址
- location — 接收请求
- include uwsgi_params —   #确定为同uwsgi通讯 ，固定写法
- uwsgi_param UWSGI_SCRIPT manage:app;   # 启动flask的文件:Flask的实例
- uwsgi_param UWSGI_CHDIR 项目的目录

2.修改uwsgi.ini配置文件

```
[uwsgi]
socket=127.0.0.1:8000
pythonpath=/opt/FlaskOA
module=manage
wsgi-file=/opt/FlaskOA/manage.py
callable=app
processes=4
threads=2
daemonize=/opt/script/uwsgi.1og
```

说明

```
#添加配置选择
[uwsgi]  必须有 , 不然会报错
#配置和nginx连接的socket连接
socket=127.0.0.1:8000
# 项目路径设置  到项目主目录
pythonpath=/opt/FlaskOA
#配置项目启动文件
wsgi-file=/opt/FlaskOA/manage.py
#配置启动的进程数
processes=4
#配置每个进程的线程数
threads=2
#配置启动管理主进程
master=True
#配置存放主进程的进程号文件
pidfile=uwsgi.pid
#配置dump日志记录
daemonize=/opt/script/uwsgi.1og
```



3.先启动uwsgi，后启动nginx，访问服务器ip，如果项目页面展示出来，即为成功

```
# 杀死 uwsgi 和nginx进程
pkill -9 uwsgi
pkill -9 nginx
#启动uwsgi
uwsgi --ini uwsgi.ini
#启动nginx
nginx

```

访问逻辑

浏览器通过服务器ip的80端口访问，nginx监听80端口，转发给127.0.0.1:8000,uwsgi处理请求，访问用户



### 5.Flask 项目使用docker的mysql数据库

#### 1. 安装Mariadb数据库

安装命令. 同时安装mariadb的数据库和客户端程序

```
yum -y install mariadb mariadb-server    # mariadb的客户端和服务端
```

安装完成后我们要启动mariadb数据库[有如下常用的命令]

```shell
# 启动数据库
systemctl start mariadb
# 重启数据库
systemctl restart mariadb
# 停止数据库
systemctl stop mariadb
# 查看数据库的运行状态
systemctl status mariadb
# 设置数据库开机自动启动
systemctl enable mariadb
```

启动好数据库后.由于我们是首次使用数据库我们需要配置数据库的初始密码(**ps:以下步骤可以不用做，我们使用的是docker的数据库**)

设置密码的命令是:

```
mysql_secure_installation
```

这样就会进入到如下的页面,按照要求进行设置.

```
Enter current password for root:<–初次运行直接回车

设置密码

Set root password? [Y/n] <– 是否设置root用户密码，输入y并回车或直接回车

New password: <– 设置root用户的密码
Re-enter new password: <– 再输入一次你设置的密码

其他配置

Remove anonymous users? [Y/n] <– 是否删除匿名用户，回车

Disallow root login remotely? [Y/n] <–是否禁止root远程登录,回车,

Remove test database and access to it? [Y/n] <– 是否删除test数据库，回车

Reload privilege tables now? [Y/n] <– 是否重新加载权限表，回车
```

初始化MariaDB完成，接下来测试登录的命令:

```
mysql -u root -p
```

会提示我们数据密码,这个时候我们输入刚才设置的密码就可以登录到数据库中了.

因为项目需要远程连接数据库,数据库默认是没有开启的所以我们需要开启远程连接.在mysql数据库中的user表中可以看到默认是只能本地连接的，所有可以添加一个新的用户，该用户可以远程访问

1. 创建用户

   ```
   # 先使用数据库
   
   use mysql;
   
   # 针对ip
   create user 'root'@'192.168.10.10' identified by 'password';
   
   #全部
    create user 'root'@'%' identified by 'password';  [本项目选择的这条命令,password要替换成自己需要设置的root密码]
   ```

2. 授权

   ```
   # 给用户最大权限  [本项目选择这条命令,password要替换成自己需要设置的root密码]
   grant all privileges on *.* to 'root'@'%' identified by 'password';
   
   # 给部分权限(test 数据库)
   
   grant all privileges on test.* to 'root'@'%' identified by 'password' with grant option;
   
   # 刷新权限表
   flush privileges;
   
   # 查看
   show grants for 'root'@'localhost';
   ```

   接下来就可以在远程的数据库可视化工具中直接访问该服务器中的mysql了。

#### 2.安装使用docker

```shell
yum install docker -y  #安装docker
systemctl enable docker  #开机自启动docker
systemctl start docker  #启动docker
```

docker 常用命令

```shell
docker images   # 查看本机的镜像
docker search mysql # 搜索镜像 
docker pull mysql:5.7 # 下载镜像
docker rmi 镜像id   #删除镜像
docker run -di --name docker_mysql -p 33306:3306 -e MYSQL_ROOT_PASSWORD=123 383867b75fd2
run 创建并启动	
	-i 交互式
    -d 指定容器是前台还是后台运行，默认是False，后台运行
    -t 分配一个终端
    -u 指定运行用户
    -e 指定环境变量，比如MYSQL_ROOT_PASSWORD
    -p 端口映射 宿主机端口:虚拟机端口
docker ps -a   #查看所有的容器
docker exec -it 容器id /bin/bash #进入虚拟容器

docker container stop 容器id或者容器名字关闭镜像
docker container start 容器id或者容器名字启动容器
docker container rm 容器ID或者容器名字删除容器
docker container kil1 容器ID或者容器名字。杀死容器
```

```shell
docker commit mypython3 mypython3_centos  #制作镜像
    # mypython3容器名字
    # mypython3_centos 镜像名字
docker save -o mypython3_centos.tar mypython3_centos #打包镜像
	# -o mypython3_centos.tar 打包的压缩包名字
	# mypython3_centos 镜像名字
docker load</root/demo/mypython3_centos.tar  # 使用镜像
```

创建mysql容器

```shell
docker pull mysql:5.7 # 下载镜像
docker run -di --name docker_mysql -p 33306:3306 -e MYSQL_ROOT_PASSWORD=1234 383867b75fd2 # 创建并启动容器
```

本机连接docker数据库

```shell
mysql -uroot -p123 -h 10.10.14.180 -P 33306 #连接docker 数据库
```

#### 3.修改flask 配置文件

settings.py

```shell
class Config:
    
    SQLALCHEMY_DATABASE_URI = "mysql://root:1234@主机ip:33306/数据库名"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = '123456'
```

重启uwsgi和nginx即可
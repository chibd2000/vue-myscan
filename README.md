
# 环境搭建

默认账号密码 admin / admin

```
docker volume create --name=myscan_db
docker-compose up -d
./run_mysql.sh
```

![img.png](img/12.png)

数据库初始化

```
docker exec -it myscan_web bash
export PATH=$PATH:/usr/local/python3/bin
flask create
```

##注意事项

- 如果想要支持ksubdomain信息搜集，请在vue-myscan的目录下运行如下命令

```
wget https://github.com/boy-hack/ksubdomain/releases/download/v1.9.5/KSubdomain-v1.9.5-linux.tar
tar -xvf KSubdomain-v1.9.5-linux.tar
mv ./ksubdomain ./client/ksubdomain/ksubdomain
chmod +x ./client/ksubdomain/ksubdomain
rm KSubdomain-v1.9.5-linux.tar
```

- 为了安全jwt记得自己更换一次，密钥文件位于settings.py

![img.png](img/14.png)

## 配置文件

- config/conf.yaml

![img.png](img/1.png)

- client/conf/myscan.yaml

![img.png](img/2.png)

登陆口

![img.png](img/13.png)

页面布局如下所示

![img.png](img/9.png)

# 扫描

## 信息搜集

![img.png](img/5.png)

![img.png](img/8.png)

![img.png](img/6.png)

## 漏洞验证

![img.png](img/3.png)

![img.png](img/4.png)

# github commit & pr & issue 监控

![img.png](img/11.png)

![img.png](img/10.png)





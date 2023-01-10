FROM centos:7

#  yum 更新
RUN set -ex \
	&& yum -y install zlib-devel bzip2-devel libffi-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make wget gcc-c++ \
	&& yum clean all \
	&& mkdir /usr/local/python3 \
	&& mkdir /home/data \
	&& mkdir /app \

# 复制所有文件到/home/data/ 目录
COPY . /home/data

RUN set -ex \
	&& cd /home/data \
	&& tar -zxvf openssl-1.1.1.tar.gz \
	&& cd openssl-1.1.1 \
	&& ./config --prefix=/usr/local/openssl shared zlib \
	&& make && make install \
	&& cd .. \
	&& tar -xvJf  Python-3.10.6.tar.xz \
	&& cd Python-3.10.6 \
	&& ./configure --prefix=/usr/local/python3 --with-openssl=/usr/local/openssl \
	&& make && make install \
    && cd .. \
	&& yum install -y epel-release \
    && yum install -y python-pip \
	&& rm -f /usr/bin/python \
	&& rm -f /usr/bin/pip \
	&& ln -s /usr/local/python3/bin/python3 /usr/bin/python \
	&& ln -s /usr/local/python3/bin/pip3 /usr/bin/pip \

# 修复因修改python版本导致yum失效问题
RUN set -ex \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/bin/yum \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/libexec/urlgrabber-ext-down \
    && yum install -y deltarpm

# 安装python/更新pip
RUN set -ex \
	&& python -V \
	&& python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

# 安装yum 工具
RUN set -ex \
 	&& yum  install -y lrzsz \
	&& yum  install -y net-tools \
 	&& yum  install -y zip unzip \
	&& yum  install -y nginx \

# 启动配置
RUN set -ex \
	&& cd /home \
 	&& pip list \
	&& echo "build success - zpchcbd"


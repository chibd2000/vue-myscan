#!/bin/bash
export PATH=$PATH:/usr/local/python3/bin
flask create;
nginx;
gunicorn app:myscan_app -c gunicorn_config.py;
ln -s /app/client/exploit /app/exploit;
ln -s /app/client/core /app/core;
if [ ! -f "./client/ksubdomain/ksubdomain" ];then
	wget https://github.com/boy-hack/ksubdomain/releases/download/v1.9.5/KSubdomain-v1.9.5-linux.tar --no-check-certificate
	tar -xvf KSubdomain-v1.9.5-linux.tar
  mv ./ksubdomain ./client/ksubdomain/ksubdomain
  chmod +x ./client/ksubdomain/ksubdomain
  rm KSubdomain-v1.9.5-linux.tar
else
	echo "文件存在"
fi


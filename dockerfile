FROM python:3.11

RUN mkdir /app
WORKDIR /app
# 安装net rpc命令
RUN apt update && apt install -y samba && rm -rf /var/lib/apt/lists/*  

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 12345
CMD gunicorn -b 127.0.0.1:12345 --access-logfile '-' --error-logfile '-' aligenie.wsgi
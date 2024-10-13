# 使用官方 Python 镜像
FROM python:slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件和应用程序代码
COPY requirements.txt ./
COPY cors_proxy.py ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 暴露 Flask 应用程序的端口
EXPOSE 5000

# 启动应用程序
CMD ["gunicorn", "-b", "0.0.0.0:5000", "cors_proxy:app"]

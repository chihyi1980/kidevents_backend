# 使用官方 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    libgirepository1.0-dev \
    gobject-introspection \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip, setuptools 和 wheel
RUN pip install --upgrade pip setuptools wheel

# 复制当前目录的内容到容器中的 /app 目录
COPY . /app

# 将 Config.py.prod 替换为 Config.py
RUN cp /app/config.py.prod /app/config.py

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将容器的端口5000暴露出来
EXPOSE 5000

# 运行应用程序
CMD ["python", "app.py"]

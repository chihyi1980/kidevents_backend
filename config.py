import os

class Config:
    # JWT 秘钥
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'e04xup6qj3j4')

    # MongoDB 连接字符串
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://kidevents:kidevents123@localhost:27017/')

# 在app.py中可以通过 Config 进行全局配置

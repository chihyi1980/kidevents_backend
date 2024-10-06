import os

class Config:
    # JWT 秘钥
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'e04xup6qj3j4')

    # MongoDB 连接字符串
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://kidevents:kidevents123@localhost:27017/')

    #OPEN AI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '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')
    OPENAI_ORG = os.getenv('OPENAI_ORG','org-HwNugKJzMNuyw5ouTr7xHARY')
    OPENAI_PROJECT = os.getenv('OPENAI_PROJECT','proj_BBu2qRK5fvki1gZjA7jrqiry')

# 在app.py中可以通过 Config 进行全局配置

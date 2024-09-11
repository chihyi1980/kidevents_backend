from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.user_routes import user_bp
from routes.events_routes import events_bp
from routes.loc_routes import loc_bp
from routes.tag_routes import tag_bp
from config import Config

app = Flask(__name__)
CORS(app)  # 允许所有域访问所有路由
app.config.from_object(Config)  # 加载配置

jwt = JWTManager(app)

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(events_bp, url_prefix='/api')
app.register_blueprint(loc_bp, url_prefix='/api')
app.register_blueprint(tag_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

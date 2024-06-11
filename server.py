# coding:utf-8
from flask import Flask
from flask import jsonify
from flask import request

# 创建对象
import zhilian
import extract_keywords

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# 编写路由，构建url与函数的映射关系（将函数与url绑定）
# 构造post请求
@app.route("/crawl", methods=["POST"])
def crawl():
    # request.form.get：获取post请求的参数，
    city = request.form.get("city")
    if city:
        return jsonify({"code": 1000, "message": zhilian.main(city)})
    else:
        return jsonify({"code": 10001, "message": "failure"})


@app.route("/getKeyWords", methods=["GET"])
def getKeyWords():
    return jsonify({"code": 10000, "message": extract_keywords.main()})


if __name__ == '__main__':
    # 默认方式启动
    # app.run()
    # 解决jsonify中文乱码问题
    app.config['JSON_AS_ASCII'] = False
    # 以调试模式启动,host=0.0.0.0 ,则可以使用127.0.0.1、localhost以及本机ip来访问
    app.run(host="0.0.0.0", port=8008)

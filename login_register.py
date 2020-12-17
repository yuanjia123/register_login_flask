from flask import Flask, url_for, render_template
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy
import config
'''
（输入） Flask_restful01 有一个验证、类似于wtf的验证   （输入验证）
 通过 postman 进行输入
'''
app = Flask(__name__)
api = Api(app)
app.config.from_object(config)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))



#这是一个接受ajax数据的api
class RegisterView(Resource):
    '''
    注册
    '''

    def post(self):
        # 获取解析对象
        parser = reqparse.RequestParser()

        parser.add_argument("password",  required=True)
        parser.add_argument("username",  required=True)


        # 拿到这个传来的参数
        args = parser.parse_args()

        # 打印ajax传递来的参数
        print("获取全部传来的值:",args)

        # 获取username的字段
        print("打印前端传来的值：",args.get("username"))
        print("打印前端传来的值：",args.get("password"))
        u = args.get("username")
        p = args.get("password")

        u1 = User.query.filter(User.username == u).first()

        if u1:
            return {"kk":":  用户名存在"}
        else:
            new_u = User(username = u,password = p)
            db.session.add(new_u)
            db.session.commit()

            return {"kk": ":   注册成功"}

api.add_resource(RegisterView, "/data_register/")




#这是一个接受ajax数据的api
class Send_ajax(Resource):
    '''
    登录
    '''

    def post(self):
        # 获取解析对象
        parser = reqparse.RequestParser()

        parser.add_argument("password",  required=True)
        parser.add_argument("username",  required=True)


        # 拿到这个传来的参数
        args = parser.parse_args()

        # 打印ajax传递来的参数
        print("获取全部传来的值:",args)

        # 获取username的字段
        print("打印前端传来的值：",args.get("username"))
        print("打印前端传来的值：",args.get("password"))

        u = args.get("username")
        p = args.get("password")

        k_u = User.query.filter(User.username == u,User.password == p).first()

        if k_u:
            return {"wakaka":"登录成功"}
        else:
            return {"wakaka":"登陆失败"}


api.add_resource(Send_ajax, "/data_login/")




@app.route('/login/')
def login():
    print("主页")
    return render_template("login.html")


@app.route('/')
def register():
    return render_template("register.html")

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)
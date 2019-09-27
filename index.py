from flask import request,Flask,render_template,redirect,url_for
from flask import session
import random,os,json
import register
import SQL


app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def index():
    """加载网页模板"""
    um = session.get('uname')
    if um:
        return redirect('/index/')
    else:
        return render_template("index.html")

@app.route("/logout")
def logout():
    if 'uname' in session:
        session.pop('uname')
        rsp = redirect("/")
        return rsp
    else:
        return redirect("/login/")

@app.route("/login/",methods=["POST","GET"])
def log():
    if 'uname' in session:
            return redirect("/index/")
    else:
        if request.method == "POST":
            name = request.form.get('username')
            pwd = request.form.get('password')
            if register.check_user(name,pwd): 
                session["uname"] = name
                return redirect(url_for("page1"))
            else:
                return render_template("index.html",log_err="用户名密码错误")
        else:
            return redirect(url_for("index"))
    

@app.route("/index/")
def page1():
    um = session.get('uname')
    if um:
        return render_template("page1.html")
    else:
        return redirect(url_for("log"))


@app.route('/check_name')
def check_name():
    uname = request.args.get("name")
    msg = register.check_user_name(uname)
    if msg == 0:
        return json.dumps({"code":0})
    elif msg == 2:
        return json.dumps({"code":2})

@app.route('/register/',methods=["POST","GET"])
def reg():
    if request.method == "GET":
        return render_template("reg.html")
    else:
        print(request.form)
        name = request.form.get("uname")
        pwd = request.form.get("passwd")
        msg1 = register.check_user_name(name)
        if msg1 == 2:
             return render_template("reg.html",reg_err="账户已存在")
        
        phone = request.form.get("phone")
        email = request.form.get("email")
        print(name,pwd,phone,email)
        msg2 = register.user_reg(name, pwd, phone, email)
        if msg2 == True:
             return render_template("reg.html",reg_err="注册成功")
        else:
             return render_template("reg.html",reg_err="注册失败")

@app.route("/view/",methods=["POST","GET"])
def page2():
    um = session.get('uname')
    if not um:
        return redirect('/login/')
    else:
        if request.method =='GET':
            return render_template("page2.html")
        elif request.method =="POST":
            op = request.form.get("term")
            if "编号" in op:
                data0 = SQL.show("id")
            elif "数量" in op:
                data0 = SQL.show("number")
            elif "价格" in op:
                data0 = SQL.show('price')
            if data0 == 0:
                return render_template("page2.html",err="仓库空空如也")
            else:
                return render_template("page2.html",res=data0)

@app.route("/page3/",methods=["POST","GET"])
def page3():
    um = session.get('uname')
    if not um:
        return redirect('/login/')
    else:
        if request.method == "GET":
            return render_template("page3.html")
        else:
            op = request.form.get("term")
            if "编号" in op:
                op = "id"
            elif "数量" in op:
                op = "number"
            elif "价格" in op:
                op = 'price'
            elif "名称" in op:
                op = "name"
            info = request.form.get("find_term")
            res = SQL.find(op,info)
            if res == 1:
                return render_template("page3.html",err="查无此商品")
            elif res == 2:
                return render_template("page3.html",err="数据库查询失败")
            else:
                return render_template("page3.html",res=res,err="查询成功")

@app.route("/page4/",methods=["POST","GET"])
def page4():
    um = session.get('uname')
    if not um:
        return redirect('/login/')
    else:
        if request.method == "GET":
            return render_template("page4.html")
        else:
            id = request.form.get("id")
            name = request.form.get("name")
            num = request.form.get("num")
            size = request.form.get("size")
            price = request.form.get("price")
            msg = SQL.insert(id,name,num,size,price)
            if msg == 1:
                return render_template("page4.html",err="插入成功")
            elif msg == 0:
                return render_template("page4.html",err="插入失败")
            elif msg == 2:
                return render_template("page4.html",err="商品已存在")


@app.route("/page5/")
def page5():
    um = session.get('uname')
    if um:
        return render_template("page5.html")
    else:
        return redirect(url_for("log"))


@app.route("/page5/op",methods=["POST","GET"])
def page5_op():
    um = session.get('uname')
    if not um:
        return redirect('/login/')
    else:
        if request.method == "GET":
            op = request.args.get("term")
            if "编号" in op:
                op = "id"
            elif "数量" in op:
                op = "number"
            elif "价格" in op:
                op = 'price'
            elif "名称" in op:
                op = "name"
            info = request.args.get("find_term")
            res = SQL.find(op,info)
            if res == 1:
                return render_template("page5.html",err="查无此商品")
            elif res == 2:
                return render_template("page5.html",err="数据库查询失败")
            else:
                return render_template("page5.html",res=res,err="查询成功")
        else:
            id = request.form.get("id")
            name = request.form.get("name")
            mm = SQL.delete(id,name)
            # print(mm)
            if mm == 1:
                return json.dumps({"flag":1})
            elif mm == 0:
                return json.dumps({"flag":0})

@app.route("/page6/")
def page6():
    um = session.get('uname')
    if um:
        return render_template("page6.html")
    else:
        return redirect(url_for("log"))

@app.route("/page6/op",methods=["POST","GET"])
def page6_op():
    um = session.get('uname')
    if not um:
        return redirect('/login/')
    else:
        if request.method == "GET":
            op = request.args.get("term")
            if "编号" in op:
                op = "id"
            elif "数量" in op:
                op = "number"
            elif "价格" in op:
                op = 'price'
            elif "名称" in op:
                op = "name"
            info = request.args.get("find_term")
            res = SQL.find(op,info)
            if res == 1:
                return render_template("page6.html",err="查无此商品")
            elif res == 2:
                return render_template("page6.html",err="数据库查询失败")
            else:
                return render_template("page6.html",res=res,err="查询成功")
        else:
            id = request.form.get("id")
            name = request.form.get("name")
            num = request.form.get("num")
            size = request.form.get("size")
            price = request.form.get("price")
            mm = SQL.updata(id,name,num,size,price)
            print(mm)
            if mm == 1:
                return json.dumps({"flag":1})
            elif mm == 0:
                return json.dumps({"flag":0})

if __name__ == "__main__":
    app.run("127.0.0.1",port=80,debug=True)
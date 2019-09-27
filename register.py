#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import re,os
import urllib.parse
import urllib.request
import random, json
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header



conf = json.load(open(os.path.join(os.path.split(os.path.realpath(__file__))[0],'config.json'))) #配置信息数据


def send_sms_code(phone):
    '''
    函数功能：发送短信验证码（6位随机数字）
    函数参数：
    phone 接收短信验证码的手机号
    返回值：发送成功返回验证码，失败返回False
    '''
    verify_code = str(random.randint(100000, 999999))

    try:
        url = "http://v.juhe.cn/sms/send"
        params = {
            "mobile": phone,  # 接受短信的用户手机号码
            "tpl_id": "162901",  # 您申请的短信模板ID，根据实际情况修改
            "tpl_value": "#code#=%s" % verify_code,  # 您设置的模板变量，根据实际情况修改
            "key": "ab75e2e54bf3044898459cb209b195e4",  # 应用APPKEY(应用详细页查询)
        }
        params = urllib.parse.urlencode(params).encode()

        f = urllib.request.urlopen(url, params)
        content = f.read()
        res = json.loads(content)

        if res and res['error_code'] == 0:
            return verify_code
        else:
            return False
    except:
        return False

def check_password(password):
    '''
    函数功能：校验用户密码是否合法
    函数参数：
    password 待校验的密码
    返回值：校验通过返回0，校验错误返回非零（密码太长或太短返回1，密码安全强度太低返回2）
    '''
    #验证密码格式
    if len(password) < 6 or len(password) > 15:
        return 1
    #验证密码难度
    if re.match("[0-9]{6,15}$|[a-z]{6,15}$|[A-Z]{6,15}$", password):
        return 2
    return 0

def check_phone(phone):
    '''
    函数功能：校验手机号格式是否合法
    函数参数：
    phone 待校验的手机号
    返回值：校验通过返回0，校验错误返回1
    '''

    if re.match("^1\d{10}$", phone):
        return 0

    return 1

def check_email(email):
    if re.match("^[a-z,A-Z,0-9]+@[a-z,A-Z]+.[a-z,A-Z]+$", email):
        return 0
    else:
        return 1

def check_user_name(user_name):
    '''
    函数功能：校验用户名是否合法
    函数参数：
    user_name 待校验的用户名
    返回值：校验通过返回0，校验失败返回非零（格式错误返回1，用户名已存在返回2）
    '''
    # [a-zA-Z0-9_]{6, 15}
    if not re.match("^[a-zA-Z0-9_]{3,15}$", user_name):
        return 1

    # 连接数据库，conn为Connection对象
    
    conn = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])

    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("select uname from user where uname=%s", (user_name, ))
            # 通过游标获取执行结果
            rows = cur.fetchone()
    finally:
        # 关闭数据库连接
        conn.close()  

    if rows:
        return 2

    return 0

def send_email_code(email):
    '''
    函数功能：发送邮箱验证码（6位随机数字）
    函数参数：
    email 接收验证码的邮箱
    返回值：发送成功返回验证码，失败返回False
    '''
    mail_host = 'smtp.qq.com'
    port = 465
    send_by = "675248896@qq.com"
    password = 'gpmarcovgajsbcia'
    send_to = email

    verify_code = str(random.randint(100000, 999999))

    message = MIMEText(verify_code, 'plain', 'utf-8')
    message["From"] = Header(send_by)
    message["To"] = Header(send_to)
    message["Subject"] = Header('新用户注册验证码')

    try:
        print('发送开始。。')
        smpt = smtplib.SMTP_SSL(mail_host, port)
        print('开始登录')
        smpt.login(send_by, password)
        print('登录成功')
        smpt.sendmail(send_by, send_to, message.as_string())
    except Exception as e:
        return False

    return verify_code

def user_reg(uname, password, phone, email):
    '''
    函数功能：将用户注册信息写入数据库
    函数描述：
    uname 用户名
    password 密码
    phone 手机号
    email 邮箱
    返回值：成功返回True，失败返回False
    '''
    # 连接数据库，conn为Connection对象
    conn = pymysql.connect(conf["db_server"], conf["db_user"],conf["db_password"], conf["db_name"])

    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("insert into user (uname, password, phone, email) values (%s, password(%s), %s, %s)", (uname, password, phone, email))
            r = cur.rowcount
            conn.commit()
    finally:
        # 关闭数据库连接
        conn.close()      

    return bool(r)

def check_user(name,pswd):
    '''
    函数功能：校验用户名,密码是否存在
    函数参数：
    user_name，pswd 待校验的用户名和密码
    返回值：校验通过返回True，校验失败返回非零
    '''

    # 连接数据库，conn为Connection对象
    conn = pymysql.connect(conf["db_server"], conf["db_user"],conf["db_password"], conf["db_name"])

    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("select * from user where uname=%s and password=password(%s)", (name,pswd))
            # 通过游标获取执行结果
            rows = cur.fetchone()
    finally:
        # 关闭数据库连接
        conn.close()  

    if rows:
        return True

    return False

def reg_main():
    '''
    函数功能：实现用户注册
    参数：无
    返回值：无
    '''
    #用户名验证
    while True:
        user_name = input("请输入用户名（只能包含英文字母、数字或下划线，最短6位，最长15位）：")

        ret = check_user_name(user_name)

        if ret == 0:
            break
        elif ret == 1:
            print("用户名格式错误，请重新输入！")
        elif ret == 2:
            print("用户名已存在，请重新输入！")

    #密码验证
    while True:
        while True:
            password = input("请输入密码（密码长度6-15位）：")
            ret = check_password(password)
            if ret == 0:
                break
            elif ret == 1:
                print("密码不符合长度要求，请重新输入！")
            elif ret == 2:
                m = input("密码太简单,是否继续(N/Y)")
                if m.lower() == 'y':
                    break

        confirm_pass = input("请再次输入密码：")

        if password == confirm_pass:
            break
        else:
            print("两次输入的密码不一致，请重新输入！")
    
    while True:
        phone = input("请输入手机号：")

        if check_phone(phone):
            print("手机号输入错误，请重新输入！")
        else:
            break
    
    while True:
        email = input("请输入邮箱：")
        # 校验邮箱的合法性
        if check_email(email) == 1:
            print('输入的邮箱格式有误，请重新输入。。。')
        else:
            break
    while True:
        print("\n请选择验证方式：1.短信验证 2.邮箱验证\n")
        op = input("输入验证方式的代号：")
        if op == '1':
            #短信验证
            verify_code = send_sms_code(phone)
            if verify_code:
                print("短信验证码已发送！")
            else:
                print("短信验证码发送失败，请检查网络连接或联系软件开发商！")
                sys.exit(1)

            while True:
                verify_code2 = input("请输入短信验证码：")
                if verify_code2 != verify_code:
                    print("短信验证码输入错误，请重新输入！")
                else:
                    break
            break

        elif op == '2':
            #邮箱验证
            verify_code1 = send_sms_code(phone)
            if verify_code1:
                print("邮箱验证码已发送！")
            else:
                print("短信验证码发送失败，请检查网络连接或联系软件开发商！")
                sys.exit(1)

            while True:
                verify_code2 = input("请输入短信验证码：")
                if verify_code2 != verify_code1:
                    print("短信验证码输入错误，请重新输入！")
                else:
                    break
            break
        else:
            print("输入错误，请重新选择！")


    #注册用户
    if user_reg(user_name, password, phone, email):
        print("注册成功！")
    else:
        print("注册失败！")

def login_main():
    '''
    函数功能：用户登录验证
    函数参数：无
    返回值：登录验证结果
    '''
    while True:
        uuser_name =input('\n输入用户名：')
        flag =  check_user_name(uuser_name)
        if flag == 1:
            print("用户格式错误，请重新输入。。。")
        elif flag == 0:
            print("用户不存在，请重新输入。。。")
        else:
            break
    while True:
        password = input("\n密码：")
        flag = check_password(password)
        if flag == 0 or flag == 2:
            break
        else:
            print('格式错误，请重新输入。。。')
    
    return check_user(uuser_name,password)


    









#!/usr/bin/env python3
#-*- code: utf-8 -*-


import pymysql
import json
import os

conf = json.load(open(os.path.join(os.path.split(os.path.realpath(__file__))[0],'config.json'))) #配置信息数据


def show(sc):
    '''根据选择条件排序显示，返回查询条件,空为0，否则返回数据'''

    conn = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("select * from good ORDER BY %s "%sc)
            # 通过游标获取执行结果
            r = cur.fetchall()
            if not r:
               return 0
            else:
               return r
    except:
        return 1

def find(sc,info):
    '''根据选择条件排序显示，返回查询条件,若不存在返回1，若查询失败返回2'''
    conn = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("select * from good where %s = '%s' " % (sc, info))
            # 通过游标获取执行结果
            r = cur.fetchall()
            if not r:
               return 1
            else:
               return r
    except :
        return 2


def insert(id,name,num,size,price):
    '''插入成功返回1，插入失败返回0,存在返回2'''
    con = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])
    try:
        with con.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
                    # 执行任意支持的SQL语句
                    cur.execute("select * from good where name='%s' and size='%s' "% (name, size))
                    # 通过游标获取执行结果
                    r = cur.fetchall()
                    if not r:
                        cur.execute("insert into good (id,name,size, number, price) values (%s,%s, %s, %s, %s)",\
                                    (id, name, size, num, price))
                        r = cur.rowcount
                        con.commit()
                        if r != 0:
                            return 1
                        else:
                            return 0
                    else:
                        return 2
    except:
        return 0

def delete(id, name):
    """删除成功返回1，失败返回0"""
    con = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])
    try:
        with con.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("delete from good where id='%s' and name='%s'" % (id,name))
            r = cur.rowcount
            con.commit()
            if r != 0:
                return 1
            else:
                return 2
    except :
        return 0

def updata(id,name,num,size,price):
    '''修改成功返回1，失败返回0'''
    con = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])
    try:
         with con.cursor() as cur:
            cur.execute("update good set name='%s',size='%s',number='%s',price='%s'  where id='%s'" %\
                        (name,size,num,price,id))
            r = cur.rowcount
            con.commit()
            if r != 0:
                return 1
            else:
                return 0
    except Exception as e:
            print(e)
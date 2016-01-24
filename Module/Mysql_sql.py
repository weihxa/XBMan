#!/usr/bin/env python
#_*_coding:utf-8_*_

import MySQLdb
import conf

class MysqlHelper(object):

    def __init__(self):
        self.__conn_dict = conf.conn_dict


    def Get_one(self,sql):
        conn = MySQLdb.connect(**self.__conn_dict)
        #cur = conn.cursor()
        #cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        cur = conn.cursor()
        #sql = "select * from "
        #params =('����')
        reCount = cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return data

    def Get_dict(self,sql):
        conn = MySQLdb.connect(**self.__conn_dict)
        #cur = conn.cursor()
        cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        #sql = "select * from "
        #params =('����')
        reCount = cur.execute(sql)
        data = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return data

    def In_sql(self,sql):
        conn = MySQLdb.connect(**self.__conn_dict)
        cur = conn.cursor()
        #cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        reCount = cur.execute(sql)
        data = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return data
    def IP_lite(self,username):
        conn = MySQLdb.connect(**self.__conn_dict)
        cur = conn.cursor()
        sql1 = "select id from user where username ='%s';"% username
        reCount = cur.execute(sql1)
        datt = cur.fetchone()
        #print datt[0]
        sql2 = "select server_id from competence where user_id ='%s';"% datt[0]
        reCount = cur.execute(sql2)
        aa=[]
        while True:
            data = cur.fetchone()
            if data ==None:
                break
            else:
                #print data[0]
                aa.append(data[0])
        cc={}
        for i in aa:
            sql3 = "select ip from server where id ='%s';"% i
            reCount = cur.execute(sql3)
            data = cur.fetchone()
            #print data[0]
            cc[i]=data[0]
        conn.commit()
        cur.close()
        conn.close()
        return cc



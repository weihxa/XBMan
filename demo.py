#!/usr/bin/env python
#_*_coding:utf-8_*_
# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import time
import traceback
from paramiko.py3compat import input
from Module import Mysql_sql
from Module import Passwd
import MySQLdb
import paramiko
try:
    import interactive
except ImportError:
    from . import interactive


def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """
    
    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return
        
    for key in agent_keys:
        print('Trying ssh-agent key %s' % hexlify(key.get_fingerprint()))
        try:
            transport.auth_publickey(username, key)
            print('... success!')
            return
        except paramiko.SSHException:
            print('... nope.')


def manual_auth(username, hostname,pw):
    '''default_auth = 'p'
    #auth = input('Auth by (p)assword, (r)sa key, or (d)ss key? [%s] ' % default_auth)
    auth = 'P'
    if len(auth) == 0:
        auth = default_auth

    if auth == 'r':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        path = input('RSA key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('RSA key password: ')
            key = paramiko.RSAKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    elif auth == 'd':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_dsa')
        path = input('DSS key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.DSSKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('DSS key password: ')
            key = paramiko.DSSKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    else:
        #pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
        pw = '123123'
        '''
    t.auth_password(username, pw)

def login(username,password):
    aa = Mysql_sql.MysqlHelper()
    sql = "select password from user where username ='%s';" %username
    #params = Username
    c=aa.Get_one(sql)
    if password == Passwd.jiami().decrypt(c[0][0]):
        print '登陆成功'
        return False
    else:
        print '登陆失败'

def Add_user(username,password):
    Xpasswd=Passwd.jiami().encrypt(password)
    sql="insert into user(username,password) values('%s','%s');"%(username,Xpasswd)
    X_password=Mysql_sql.MysqlHelper().In_sql(sql)
    print('\033[3;31;40m'+'添加成功!\n'+'\033[0m')

def Add_server(ip,username,password):
    Xpasswd=Passwd.jiami().encrypt(password)
    sql="insert into server(ip,username,password) values('%s','%s','%s');"%(ip,username,Xpasswd)
    X_password=Mysql_sql.MysqlHelper().In_sql(sql)
    print('\033[3;31;40m'+'添加成功!\n'+'\033[0m')
os.system('clear')
while True:
    User_name = input('Please enter your user :').strip()
    if len(User_name) == 0:
        print('不得为空')
        continue
    Pass_wd = input('Please enter your password :').strip()
    if len(User_name) == 0:
        print('不得为空')
        continue
    os.system('clear')
    if login(User_name,Pass_wd) ==False:
        break
HQ = Mysql_sql.MysqlHelper()
#print HQ.IP_lite(User_name)
List=HQ.IP_lite(User_name)
if User_name =='admin':
    List[0]='权限管理'
else:
    List[0]='修改密码'
while True:
    for key,values in List.items():
        print key,values
    BH=input('\033[3;36;40m'+'请输入主机编号(退出:exit)：\n'+'\033[0m')
    if len(BH) == 0:
        os.system('clear')
        continue
    elif BH =='exit':
        os.system('clear')
        exit()
    elif int(BH)== 0 and User_name=='admin':
        while True:
            BH=input('1  添加主机\n2  修改密码:\n3  添加用户\n请输入编号(退出:exit)')
            if BH == '1':
                add_ip = input('请输入ip:').strip()
                add_user = input('请输入用户名：').strip()
                add_passwd = input('请输入密码:').strip()
                Add_server(add_ip,add_user,add_passwd)
            elif BH == '2':
                os.system('clear')
                X_passwd=input('输入新密码(exit):')
                if X_passwd == 'exit':
                    continue
                else:
                    Xpasswd=Passwd.jiami().encrypt(X_passwd)
                    sql="update user set password='%s' where username='%s';"%(Xpasswd,User_name)
                    X_password=Mysql_sql.MysqlHelper().In_sql(sql)
                    print('\033[3;31;40m'+'修改成功!\n'+'\033[0m')
                    time.sleep(1)
            elif BH == '3':
                add_user = input('请输入用户名：').strip()
                add_passwd = input('请输入密码:').strip()
                Add_user(add_user,add_passwd)
            elif BH == 'exit':
                break
    elif int(BH)== 0 and User_name!='admin':
        os.system('clear')
        X_passwd=input('输入新密码(exit):')
        if X_passwd == 'exit':
            continue
        else:
            Xpasswd=Passwd.jiami().encrypt(X_passwd)
            sql="update user set password='%s' where username='%s';"%(Xpasswd,User_name)
            X_password=Mysql_sql.MysqlHelper().In_sql(sql)
            print('\033[3;31;40m'+'修改成功!\n'+'\033[0m')
            time.sleep(1)
    elif int(BH) not in List.keys():
        print('\033[3;31;40m'+'无此序号！请重新输入.\n'+'\033[0m')
        continue
    else:
        # setup logging
        paramiko.util.log_to_file('demo.log')

        username = ''
        if len(sys.argv) > 1:
            hostname = sys.argv[1]
            if hostname.find('@') >= 0:
                username, hostname = hostname.split('@')
        else:
            #hostname = input('Hostname: ')
            hostname = List[int(BH)]
        if len(hostname) == 0:
            print('*** Hostname required.')
            sys.exit(1)
        port = 22
        if hostname.find(':') >= 0:
            hostname, portstr = hostname.split(':')
            port = int(portstr)

        # now connect
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((hostname, port))
        except Exception as e:
            print('*** Connect failed: ' + str(e))
            traceback.print_exc()
            sys.exit(1)

        try:
            t = paramiko.Transport(sock)
            try:
                t.start_client()
            except paramiko.SSHException:
                print('*** SSH negotiation failed.')
                sys.exit(1)

            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
            except IOError:
                try:
                    keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
                except IOError:
                    #print('*** Unable to open host keys file')
                    keys = {}

            # check server's host key -- this is important.
            key = t.get_remote_server_key()
            if hostname not in keys:
                print('*** WARNING: Unknown host key!')
            elif key.get_name() not in keys[hostname]:
                print('*** WARNING: Unknown host key!')
            elif keys[hostname][key.get_name()] != key:
                print('*** WARNING: Host key has changed!!!')
                sys.exit(1)
            else:
                print('*** Host key OK.')

            # get username
            '''
            if username == '':
                default_username = getpass.getuser()
                #username = input('Username [%s]: ' % default_username)
                username = 'whx'
                if len(username) == 0:
                    username = default_username
                    '''
            User=Mysql_sql.MysqlHelper()
            sql = "select username,password from server where ip ='%s';" %hostname
            Dict=User.Get_dict(sql)
            username = Dict['username']
            password = Passwd.jiami().decrypt(Dict['password'])
            sa_username = User_name+'('+Dict['username']+')'

            agent_auth(t, username)
            if not t.is_authenticated():
                manual_auth(username, hostname,password)
            if not t.is_authenticated():
                print('*** Authentication failed. :(')
                t.close()
                sys.exit(1)

            chan = t.open_session()
            chan.get_pty()
            chan.invoke_shell()
            os.system('clear')
            print('\033[3;36;40m'+'已登陆:%s\n'%str(hostname)+'\033[0m' )
            print('\033[3;31;40m'+'!!!谨慎操作，切勿犯错!!!\n'+'\033[0m')
            interactive.interactive_shell(chan,hostname,username,sa_username)
            chan.close()
            t.close()

        except Exception as e:
            print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
            traceback.print_exc()
            try:
                t.close()
            except:
                pass
            sys.exit(1)



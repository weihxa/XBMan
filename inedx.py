#!/usr/bin/env python
#_*_coding:utf-8_*_

from Module import Passwd

a= Passwd.jiami()

d = a.encrypt('123456')
print d
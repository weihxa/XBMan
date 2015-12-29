#!/usr/bin/env python
#_*_coding:utf-8_*_

import base64
from pyDes import *
class jiami(des):
    def __init__(self):
        super(jiami,self).__init__(b"asd12131", CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    def encrypt(self, data, pad=None, padmode=None):
        str = super(jiami,self).encrypt(data=data,pad=pad,padmode=padmode)
        return base64.b64encode(str)

    def decrypt(self, data, pad=None, padmode=None):
        data = base64.b64decode(data)
        str = super(jiami,self).decrypt(data=data,pad=pad,padmode=padmode)
        return str

k = jiami()
d = k.encrypt('test')
print d
print k.decrypt(d)
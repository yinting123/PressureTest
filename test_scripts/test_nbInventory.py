#-*-coding:utf-8-*-

import sys,ConfigParser
sys.path.append('./PressureTest')
sys.path.append('./PressureTest/conf/')

sys.path.append('../')
from base.build_message import *

class Transaction(object):
    def __init__(self):
        self.result = []

    def run(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read('../conf/data.conf')
        print cfg.sections()
        bm = build_message()
        req = bm.nb_request(cfg.get('NB','data'))
        con = transport()
        res = con.connect_nbInv(cfg.get('NB','HOST'),
                                cfg.get('NB','PORT'),req)
        self.result.append([res.return_code,res.return_msg])

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    for line in trans.result:
        print line


#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2021/4/8 16:02
# @File :  dadb.py
import os
import re
import sys

path = os.path.dirname(os.path.dirname(__file__))
print(path)


ad = ['请求数量', '失败', '成功率', '平均响应时间', '39', '1', '97.44%', '758 ms']

file = 'test_abc.html'
# with open( 'test_abc.html', 'r+', encoding='utf-8' ) as f:
#     a = f.read().replace('OpenApiTest_2021_0404_215535','aadfs.html')
#     f.write(a)


rcfile = sys.argv
print(rcfile)

# newfile = open(file,'w',encoding='utf-8')
# newfile.write(abc)
# newfile.close()
# print(abc)

# report_name = re.findall('<th>(.*?)</th><th>(.*?)</th><th>(.*?)</th><th>(.*?)</th>',abc,re.S|re.I)[0]
# report_value = re.findall('\n<td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td>',abc,re.S|re.I)[0]
# print(list(report_name))
# print(list(report_value))
# report_dict = dict(zip(report_name,report_value))
# report_dict['更新模块']='gic-weiapp-web'
# print(report_dict)
#
#
# cc = 'gic-webapp-api/open_api_dev.jmx'
# print(cc.split('/')[1])



import os
import threading


cmd = 'nohup python3 runUpLoad.py gic-marking &'

# def run(cmd):
#     try:
#         os.system( cmd )
#     except Exception as e:
#         print(e)
#
# res = os.popen( 'netstat -anp |grep 8005' ).read()
# # print(res)
# # print( "%s端口正常，服务正在启动中！" % (self.port) )
# if str(res).__contains__('LISTEN') :
#     print( f"8005端口被占用：\n {res}")
# else:
#     # 创建一个线程
#     th = threading.Thread( target=run, args=(cmd,) )
#     th.start()
#     print( 'web服务器 正在运行' )

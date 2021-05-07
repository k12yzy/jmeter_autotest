#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2021/4/15 10:05
# @File :  runUpLoad.py

import flask, os, sys,time
from flask import request,render_template
from flask_script import Manager

'''
# web页面文件上传
# Web程序采用后台方式运行：nohup python3 runUpLoad.py gic-marking 172.16.30.92 8006 &
'''
interface_path = os.path.dirname(__file__)
sys.path.insert(0, interface_path)  #将当前文件的父目录加入临时系统变量

rcfile = sys.argv

host = rcfile[2] # IP '10.105.220.75'# linux服务器  '172.16.30.92' # win服务器
port = rcfile[3] # 端口

base_path = os.path.dirname( os.path.realpath( __file__ ) )  # 获取脚本路径
upload_path = os.path.join( base_path, rcfile[1] )  # 上传文件目录
if not os.path.exists( upload_path ):
    os.makedirs( upload_path )

server = flask.Flask(__name__, static_folder='static')
manager = Manager(server)

@server.route('/', methods=['get'])
def index():
    # return HTML
    # return render_template('OpenApiTest_2021_0404_215535.html')
    return f'<head><title>{rcfile[1]}</title></head>' \
           '<form action="/upload" method="post" enctype="multipart/form-data">' \
           '<input type="file" id="img" name="img"><button type="submit">上传</button></form>'

@server.route('/upload', methods=['post'])
def upload():
    fname = request.files['img']  #获取上传的文件
    # print(fname.filename)
    if fname:
        # 拼接文件名路径
        file_name = os.path.join( upload_path, fname.filename )
        # 判断文件是否存在
        if os.path.exists(file_name):
            os.remove(file_name)
        # 保存文件
        try:
            fname.save(file_name)  #保存文件到指定路径
        except IOError:
            return '上传文件失败'

        # t = time.strftime('%Y%m%d%H%M%S')
        # new_fname = r'static/' + t + fname.filename
        return '上传文件成功, 文件名: {}'.format( file_name )
    else:
        return '{"msg": "请上传文件！"}'
# print('----------路由和视图函数的对应关系----------')
# print(server.url_map) #打印路由和视图函数的对应关系
server.run(host=host,port=port)

# if __name__ == '__main__':
    # -d 是否开启调式模式
    # -r 是否自动重新加载文件
    # -h --host 指定主机
    # -p --port 指定端口
    # --threaded 是否使用多线程
    # -？ --help 查看帮忙
    # 运行：python runUpLoad.py runserver -h 192.168.10.5 -p 8005
    # manager.run()
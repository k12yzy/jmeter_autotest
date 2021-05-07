#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2021/4/16 15:25
# @File :  get_data.py

# 列出文件夹下面最新的文件
import re, os

from common import logger


def get_latest_file(file_path):
    '''
    获取最新的文件保存到file_new
    :param file_path: 文件路径
    :return:
    '''
    lists = os.listdir( file_path )  # 列出目录的下所有文件和文件夹保存到lists
    # 按时间排序
    lists.sort( key=lambda fn: os.path.getmtime( file_path + "/" + fn ) )
    file_new = lists[-1]
    return file_new


def update_file(file_path, report_name, api_name, module_name):
    '''
    # 替换报告中链接为生成最新的文件
    :param file_path: 打开文件时，需要路径
    :param report_name: 报告的html文件名
    :param api_name: 脚本路径，*.jmx
    :param module_name: 执行模块的名称
    :return:
    '''
    read_file = open( file_path, 'r', encoding='utf-8' ).read()
    read_file = read_file.replace( 'index.html', report_name )
    read_file = read_file.replace( 'testcase.jmx', api_name )
    read_file = read_file.replace( '执行接口自动化测试', f'{module_name}接口测试报告' )
    save_file = open( file_path, 'w', encoding='utf-8' )
    save_file.write( read_file )
    save_file.close()
    return read_file



def report_get_data(read_file, api_name, module_name ):
    '''
    获取报告中数据，用于钉钉发送
    :param read_file: 测试报告文件，已打开
    :param api_name: 脚本路径，*.jmx
    :param module_name: 执行模块的名称
    :return:
    '''
    report_name = re.findall( '<th>(.*?)</th><th>(.*?)</th><th>(.*?)</th><th>(.*?)</th>', read_file, re.S | re.I )[0]
    report_value = re.findall(
        '\n<td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td><td align="center">(.*?)</td>',
        read_file, re.S | re.I )[0]
    dingding_conect = dict( zip( report_name, report_value ) )
    dingding_conect['模块'] = module_name
    dingding_conect['脚本'] = api_name.split( '/' )[1]
    logger.info( f'接口测试结果：--> {dingding_conect}' )
    return dingding_conect


# 多线程，启用web服务器，上传脚本
def run(cmd):
    try:
        os.system( cmd )
    except Exception as e:
        print( e )


def run_fileupload(target_module, host, port):
    '''
     启动web服务器，用于脚本，上传和更新
    :param target_module: 模块名称
    :param host: web服务器IP
    :param port: 端口
    :return:
    '''
    # 查询端口是否被占用
    res = os.popen( f'netstat -anp |grep {port}' ).read()
    if str( res ).__contains__( 'LISTEN' ):
        logger.info( f"{port}端口已占用：http://{host}:{port}/" )
    else:
        # Web程序采用后台方式运行：nohup python3 runUpLoad.py gic-marking &
        os.system( f"nohup python3 runUpLoad.py {target_module} {host} {port} &" )
        logger.info( f"{port}端口已启用：http://{host}:{port}/" )

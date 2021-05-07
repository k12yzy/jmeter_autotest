#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2021/4/21 20:38
# @File :  test_yapi.py


'''
Created on 2020年3月11日
@author: qguan
'''

import json
# from utils.HandleRequests import do_request
# from utils.HandleExcel import Write_excel
# import conftest

# 获取接口文档项目id
pro_url = '接口文档地址'
# 接口文档登录地址
login_url = '接口文档登录地址'
# 接口文档用户信息
login_info = {"email": "账号", "password": "密码"}
# 用户登录接口文档地址
do_request( "POST", login_url, login_info, is_json=True )

# 登录后获取接口文档所有项目
res0 = do_request( "get", pro_url )
pro_info = res0['data']['list']


def get_pro_name():
    '''获取项目名称list'''
    name_list = []
    # 遍历获取所有项目名称加入list
    for i in range( len( pro_info ) ):
        pro_name = pro_info[i]['name']
        name_list.append( pro_name )

    return name_list


def get_pro_id():
    '''根据获取项目名称list，输入选择的项目，获取id'''
    print( get_pro_name() )
    pro_name = input( "根据以上列出的项目名称输入：" )
    # 遍历项目，通过输入的项目名，获取项目id
    for i in range( len( pro_info ) ):
        pro_job = pro_info[i]['name']
        if pro_job == pro_name:
            pro_id = pro_info[i]['_id']
            return pro_id


def get_jk_info(pro_id):
    '''通过项目id获取接口信息'''
    # 获取项目接口信息
    in_url = '接口文档地址?page=1&limit=80&project_id={}'.format( pro_id )
    pro_url = '接口文档地址/get?id={}'.format( pro_id )
    # 获取项目接口信息
    res1 = do_request( "get", in_url )
    # 获取项目信息
    res2 = do_request( 'get', pro_url )
    # 提取测试的路径
    env = res2['data']['env']

    for j in range( len( env ) ):
        if env[j]['name'] == 'test':
            env_url = env[j]['domain']
        else:
            env_url = "本地测试环境"
    # 接口信息
    jk_list = []
    jk_list.append( env_url )
    # 接口关键信息：地址、方法、名称、及id
    interface = res1['data']['list']
    for i in range( len( interface ) ):
        method = interface[i]['method']
        path = interface[i]['path']
        title = interface[i]['title']
        jk_id = interface[i]['_id']
        jk_info = '-'.join( (path, title, method, str( jk_id )) )
        jk_list.append( jk_info )

    return jk_list


def get_jk_body(jk_id):
    '''通过接口id，获取接口请求参数'''
    body_url = '接口文档地址/get?id={}'.format( jk_id )
    res = do_request( 'get', body_url )
    # 请求参数
    body_info = res['data'].get( 'req_body_other' )
    res_q = {}
    if body_info:  # 如果有参数
        res1 = json.loads( body_info )
        if res1.get( 'properties' ):
            for k in res1['properties'].keys():
                res_q[k] = ""

    return res_q


def write_to_excel(jk_info, file_path):
    '''解析接口信息数据 ，写入excel'''
    ws = Write_excel( file_path )
    count = 1  # 列数
    caseid = 0  # 用例编号
    env = jk_info[0]
    for el in jk_info[1:]:
        count += 1
        caseid += 1
        jk_list = el.split( '-' )
        path = jk_list[0]
        title = jk_list[1]
        method = jk_list[2]
        jk_id = jk_list[3]
        #         print(path,title,method,jk_id)
        if method == 'POST':
            params = get_jk_body( jk_id )
            ws.write( count, 1, caseid )
            ws.write( count, 2, title )
            ws.write( count, 3, env )
            ws.write( count, 4, path )
            ws.write( count, 5, method )
            if params:  # 如果参数不为空
                ws.write( count, 6, str( params ).replace( "'", '"' ) )
        else:
            ws.write( count, 1, caseid )
            ws.write( count, 2, title )
            ws.write( count, 3, env )
            ws.write( count, 4, path )
            ws.write( count, 5, method )


if __name__ == '__main__':
    pro_id = get_pro_id()
    jk_info = get_jk_info( pro_id )
    file_path = conftest.data_path + "interface_001interface_001.xlsx"
    write_to_excel( jk_info, file_path )

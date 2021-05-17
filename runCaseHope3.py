#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2021/4/6 23:09
# @File :  runCaseHope3.py
import re
import sys
import time, os
from common import logger
from common.get_data import *
from common.send_mail import Mail
from common.send_dingding import result_to_dingding

# datetime = time.strftime( "%Y%m%d-%H_%M_%S", time.localtime() )

host = '10.105.220.75'
# host = '212.64.23.196'

if __name__ == '__main__':
    '''
    与开发部署关联，实现持续集成测试！
    ssh root@212.64.23.196 'cd /opt/apitest/apiAutoTest && python3 runner.py %s'" % target_module
    ssh root@10.105.220.75 "cd /opt/apitest/DmTest/jmeter && python3 runCaseDev3.py gic-webapp-api"
    '''

    # 更新模块名与用例脚本名称
    cases_api = {'gic-webapp-api': ['gic-webapp-api/open_api_hope.jmx','Hope开放平台','8005','浮光'],
                 'gic-integral-mall': ['gic-integral-mall/integral-mall-hope.jmx','Hope积分商城','8007','良超'],
                 'gic-member': ['gic-member/member-hope.jmx','Hope会员','8009','白月初']}

    # jmeter报告地址
    jmeter_path = '/opt/apitest/DmTest/lib/test_result/jmeter/'
    # 测试报告目录地址
    files_path = {'html': 'html/request/', 'detail': 'html/detail/', 'failure': 'html/failure/'}

    # 第一步 获取模块名
    try:
        rcfile = sys.argv[1]
        # 第二步 如果模块名与脚本中的名称一样，运行相应模块的测试
        for target_module in cases_api:
            if rcfile == target_module:
                logger.info( '=' * 20 + f'【生产环境-正在执行接口测试，大概需要2分钟左右-->模块名：{rcfile}】' + '=' * 20 )
                # 第三步 调相应的脚本运行
                # linux执行时将结果文件拷贝到发布目录;os.path.abspath返回当前目录的绝对路径
                os.system(
                    f'cd /usr/local/apache-ant-1.10.6/bin && ./ant -Dcase={cases_api[target_module][0]} -Dcasename={cases_api[target_module][1]}' )
                for key in files_path:
                    file_new = get_latest_file( jmeter_path + files_path[key] )
                    # 测试报告全路径
                    jmeter_report = jmeter_path + files_path[key] + file_new
                    # 替换报告中链接为生成最新的文件
                    read_file = update_file( jmeter_report, file_new, cases_api[target_module][0],
                                             cases_api[target_module][1] )
                    if key == 'html':
                        # 提取报告中的结果
                        dingding_conect = report_get_data( read_file, cases_api[target_module][0], target_module )
                        # 发送钉钉消息
                        result_to_dingding( cases_api[target_module][1], cases_api[target_module][0], file_new,
                                            dingding_conect, cases_api[target_module][2], cases_api[target_module][3])
                    if key == 'failure':
                        # 发送邮件
                        Mail().send( read_file, cases_api[target_module][1] )
                        logger.info( f'测试结果报告：--> https://four.gicdev.com/DmTest/jmeter/html/detail/{file_new}' )

                # 多线程，启用web服务器，上传脚本
                run_fileupload( target_module, host, cases_api[target_module][2] )
                logger.info( '=' * 20 + '【接口测试完成】' + '=' * 20 )
        logger.info( f'生产环境： {rcfile}' )

    except Exception as e:
        logger.info( '您更新的模块名不存在，无法启动接口自动化测试！' )



#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2021/4/6 23:09
# @File :  runCaseDev3.py
import re
import sys
import threading
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
    持续集成：
        ssh root@212.64.23.196 'cd /opt/apitest/apiAutoTest && python3 runner.py %s'" % target_module
        ssh root@10.105.220.75 "cd /opt/apitest/DmTest/jmeter && python3 runCaseDev3.py gic-webapp-api"
    业务模块：
        'gic-enterprise': ['gic-enterprise/enterprise-dev.jmx','企业后台','8006','夜澜'],
        'gic-integral-mall': '['gic-integral-mallintegral-mall_dev.jmx','积分商城','8007','良超']',
        'gic-wx-app': '['gic-wx-app/wx-app-dev.jmx','小程序','8008','良超']',
        'gic-member': '['gic-member/member-dev.jmx','会员','8009','白月初']',
        'gic-marketing': '['gic-marketing/marketing_dev.jmx','营销','8010','无双']',
        'gic-operations': '['gic-operations/operations_dev.jmx','运维后台','8011','白月初']',
        'gic-clerk': '['gic-clerk/clerk_dev.jmx','导购','8012','夜澜']',
        'gic-ecm': '['gic-ecm/ecm_dev.jmx','ECM','8013','无双']',
        'gic-mall': '['gic-mall/mall_dev.jmx','微商城','8014','良超']',
        'gic-webapp-marketing': '['gic-webapp-marketing/webapp-marketing_dev.jmx','XXX','8015','雅讯']',
        'gic-webapp-member': '['gic-webapp-member/webapp-member_dev.jmx','XXX','8016','雅讯']',
        'gic-webapp-admin': '['gic-webapp-admin/webapp-admin_dev.jmx','XXX','8017','雅讯']',
        'gic-store-goods': '['gic-store-goods/store-goods_dev.jmx','门店商品','8018','良超']',
        'gic-task': '['gic-task/task_dev.jmx','工作台','8019','雅讯']',
        'gic-thirdparty': '['gic-thirdparty/thirdparty_dev.jmx','XXX','8020','雅讯']'
        'gic-goods': '['gic-goods/goods_dev.jmx','商品','8021','良超']'
    '''

    # 更新模块名与用例脚本名称
    cases_api = {'gic-webapp-api': ['gic-webapp-api/open_api_dev.jmx','Dev开放平台','8005','雅讯'],
                 'gic-integral-mall': ['gic-integral-mall/integral-mall-dev.jmx','积分商城','8007','良超']}

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
                logger.info( '=' * 30 + f'【开发环境-开始执行接口测试-->模块名：{rcfile}】' + '=' * 30 )
                # 第三步 调相应的脚本运行
                # linux执行时将结果文件拷贝到发布目录;os.path.abspath返回当前目录的绝对路径
                os.system(
                    f'cd /usr/local/apache-ant-1.10.6/bin && ./ant -Dcase={cases_api[target_module][0]} -Dcasename={cases_api[target_module][1]}' )
                for key in files_path:
                    file_new = get_latest_file( jmeter_path + files_path[key] )
                    # 测试报告全路径
                    jmeter_report = jmeter_path + files_path[key] + file_new
                    # 替换报告中链接为生成最新的文件
                    read_file = update_file( jmeter_report, file_new, cases_api[target_module][0], cases_api[target_module][1] )
                    if key == 'html':
                        # 提取报告中的结果
                        dingding_conect = report_get_data( read_file, cases_api[target_module][0], target_module )
                        # 发送钉钉消息
                        result_to_dingding( cases_api[target_module][1], cases_api[target_module][0], file_new, dingding_conect, cases_api[target_module][2], cases_api[target_module][3])
                    if key == 'failure':
                        # 发送邮件
                        Mail().send( read_file, cases_api[target_module][1] )
                        logger.info( f'测试结果报告：--> https://four.gicdev.com/DmTest/jmeter/html/detail/{file_new}' )

                # 多线程，启用web服务器，上传脚本
                run_fileupload( target_module, host, cases_api[target_module][2] )
                logger.info( '=' * 30 + '【接口测试完成】' + '=' * 30 )
            else:
                logger.info( f'开发环境： {rcfile}' )
                pass

    except Exception as e:
        logger.info( '您更新的模块名为空，无法启动接口自动化测试！' )

    # # 运行的相对路径
    # path = '.'
    # # 用例路径
    # srcfile = ''
    # savefile = ''
    # # 获取test_case目录下面的用例文件名
    # try:
    #     srcfile = sys.argv[1]
    # except:
    #     srcfile = ''
    #
    #
    # # 为空，则使用默认的
    # if srcfile == '':
    #     # 文件路径
    #     srcfile = path + '/lib/test_case/Apitest.xls'
    #     # 文件保存路径
    #     savefile = path + '/lib/test_result/%s-%s.xls' % (srcfile[srcfile.rfind('/'):-4], datetime)
    #
    # else:
    #     # 如果是绝对路径，就使用绝对路径
    #     if srcfile.find( ':' ) >= 0:
    #         # windows下获取用例文件名
    #         savefile = path + '/lib/test_result/%s-%s.xls' % (srcfile[srcfile.rfind( '\\' )+1:-4], datetime)
    #     elif srcfile.find( ':' ) < 0:
    #         #linux下运行shell脚本使用
    #         savefile = path + '/lib/test_result/%s-%s.xls' % (srcfile[srcfile.rfind( '/' ):-4], datetime)
    #     else:
    #         logger.error( '非法用例路径' )
    #
    # # 读取所有execl内容用例，组合二维列表
    # datadriver.getparams( srcfile, savefile )
    # print( datadriver.alllist )
    #
    # # 执行htttest.py文件的内容，输出HTML报告
    # suite = unittest.defaultTestLoader.discover( path + "/uittest/", pattern="test_unittest.py", top_level_dir=None )
    # # 生成执行用例的对象
    # runner = bf( suite )
    # htmlpath = path + '/lib/test_result/%s.html' % (savefile[savefile.rfind( '/' ):-4])
    # runner.report( filename=htmlpath, description=datadriver.casetitle)
    # datadriver.writer.savefile()
    # # 本地拷贝文件发服务器发布目录，用于调试
    # try:
    #     if platform.platform().__contains__( 'Windows' ):
    #         # 将本地结果拷贝到服务器备份目录与发布目录
    #         datadriver.ssh_linux_file(htmlpath,'/home/apitest/MyTestApi/lib/test_result/%s.html'% (savefile[savefile.rfind( '/' ):-4]))
    #         datadriver.ssh_linux_file(htmlpath,'/home/wwwroot/default/index.html')
    #         # 自动打开服务器测试结果
    #         webbrowser.open_new( 'http://www.k12yzy.cn/' )
    #     else:
    #         # linux执行时将结果文件拷贝到发布目录;os.path.abspath返回当前目录的绝对路径
    #         os.system(f'cp {os.path.abspath( htmlpath )} /home/wwwroot/default/index.html')
    # except Exception as e:
    #     pass

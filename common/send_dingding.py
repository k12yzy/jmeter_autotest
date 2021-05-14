#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2021/12/6 21:39
# @File :  send_dingding.py
from time import strftime
from dingtalkchatbot.chatbot import DingtalkChatbot
from common import logger


def result_to_dingding(case_name, case_path, file_name, dingding_conect, port, test_name):
    '''
        送钉钉消息，目前支持三种格式
    :param case_name: 本次测试用例名称
    :param case_path: 测试用例脚本路径，用于脚本下载
    :param file_name: 测试报告路径，用于测试报告浏览
    :param dingding_conect: 测试报告结果，字典形式用于钉钉发送内容
    :param port: web服务器端口，按模块分配不同的商品，用于web端服务器启动
    :param test_name: 测试人员名字
    :return:
    '''
    #判断是为空
    now = strftime( "%Y-%m-%d %H:%M:%S" )  # 获取测试时间
    if file_name is None or file_name == '':
        pass
        logger.info( file_name )

    # WebHook——>TAPD测试提醒
    # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=707e529dfe123770549f0b0007cfed259c1b1090e07fdc2d47e17aefdbe00f7b'
    # TAPD问题处理提醒——>内部调试测试群
    # webhook=https://oapi.dingtalk.com/robot/send?access_token=96b7353c953e92218c0af0daf504c98e4ede265aea0078dafd910be6eaf4bf84
    # webhook——>个人测试群
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=0e8790a03d47c22641bbb3fb3d85e47a30aeb8bc5bb6fa21c0ed21e3d6c82783'

    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    jmeter_path = 'https://four.gicdev.com/DmTest/jmeter/'
    test_mobile = {'雅讯': '13989812663', '良超': '13803544685', '夜澜': '15869132266', '无双': '15732638539',
                   '白月初': '18268191752', '时荒': '18272872382', '浮光': '18758228432','君笑': '13097284062'}

    # 图片加文本样式（3）
    request_url = f'{jmeter_path}html/request/{file_name}'
    detail_url = f'{jmeter_path}html/detail/{file_name}'
    failure_url = f'{jmeter_path}html/failure/{file_name}'
    case_url = f'{jmeter_path}{case_path}'
    send_info = f"<font color=\'#FFA500\'>[通知] </font>[{case_name}接口测试结果..]({request_url})   \n\n --- \n\n " \
                f"<font color=\'#708090\' size=2>脚本下载：</font><font color=\'#708090\' size=3>[{dingding_conect['脚本']}]({case_url})</font> \n\n " \
                f"<font color=\'#708090\' size=2>脚本更新：</font><font color=\'#708090\' size=3>[点击更新脚本](http://10.105.220.75:{port}/)</font> \n\n " \
                f"<font color=\'#708090\' size=2>更新模块：</font><font color=\'#708090\' size=3>{dingding_conect['模块']}</font> \n\n " \
                f"<font color=\'#708090\' size=2>用例数量：</font><font color=\'#708090\' size=3>{dingding_conect['请求数量']}</font> \n\n " \
                f"<font color=\'#FF0000\' size=2>失败数量：</font><font color=\'#708090\' size=3>[{dingding_conect['失败']}]({failure_url})</font> \n\n " \
                f"<font color=\'#708090\' size=2>成 功 率：</font><font color=\'#708090\' size=3>{dingding_conect['成功率']}</font> \n\n " \
                f"<font color=\'#708090\' size=2>平均响应时间：</font><font color=\'#708090\' size=3>{dingding_conect['平均响应时间']}</font> \n\n " \
                f"<font color=\'#708090\' size=2>测试人员：</font><font color=\'#708090\' size=2>{test_name}</font> \n\n " \
                f"</font><font color=\'#708090\' size=2>测试时间：</font><font color=\'#708090\' size=2>{now}</font> \n\n " \
                f"--- \n\n  @{test_mobile[test_name]} <font color=\'#888888\' size=2>[查看详细报告]({detail_url}) </font>"
    #逻辑有错误的列表，将error字段拼接msg
    taplink = ''
    # try:
    #     for i in range(len(errorlist)):
    #         dinglink = f"<font color=\'#708090\' size=2>失败用例{str(i+1)}：</font><font color=\'#708090\' size=3>[失败名称]({testcase_url})</font> \n\n "
    #         dinglink = dinglink.replace( '失败名称', str(errorlist[i][2:5]) )
    #         taplink += dinglink
    # except Exception as e:
    #     logger.info(e)
    # send_info = send_info.replace( '问题链接', taplink )
    message_data = xiaoding.send_markdown(title=f'{case_name}接口测试结果..', text=send_info  ,at_mobiles=[{test_mobile[test_name]}])
    logger.info( f'钉钉发送：--> {message_data}' )

# if '__name__' == '__main__':
    # sendmessage( 'apitest' )
    # '#### 接口自动化执行结果... \n'
    # '> %s \n' % (msg) + '\n'
    # '> \n'
    # '> ###### 测试报告详情： @13989812663 [查看](%s) \n' % (message_url),
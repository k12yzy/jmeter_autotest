#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2020/11/30 20:34
# @File :  logger.py

import logging
import os
import colorlog

"""
        powered by Mr yaxun
        at 2019-12-22
        日志文件的配置
        用来格式化打印日志到文件和控制台
"""
#获取存入日志文件路径
path = os.path.dirname(os.path.dirname(__file__))

log_colors_config = {
    'DEBUG': 'white', #36  cyan
    'INFO': 'white', # green
    'WARNING': 'yellow',#33
    'ERROR': 'red', #31
    'CRITICAL': 'bold_red',
}

logger = logging.getLogger()
# 输出到控制台
console_handler = logging.StreamHandler()
# 输出到文件
file_handler = logging.FileHandler( filename='jmeter_api.log', mode='a', encoding='utf8' )

# 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
logger.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

# 日志输出格式 %(filename)s %(funcName)s
file_formatter = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)03d]->line:%(lineno)d [%(levelname)s] : %(message)s',datefmt='%Y%m%d %H:%M:%S')
console_formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s[%(asctime)s.%(msecs)03d]->line:%(lineno)d [%(levelname)s] : %(message)s',
    datefmt='%Y%m%d %H:%M:%S',log_colors=log_colors_config)
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

# 重复日志问题：
# 1、防止多次addHandler；
# 2、loggername 保证每次添加的时候不一样；
# 3、显示完log之后调用removeHandler
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

console_handler.close()
file_handler.close()

# 打印debug级别日志
def debug(ss):
    global logger
    try:
        logger.debug(ss)
    except:
        return

# 打印info级别日志
def info(ss):
    global logger
    try:
        logger.info(ss)
    except:
        return


# 打印warn级别日志
def warn(ss):
    global logger
    try:
        logger.warning(ss)
    except:
        return


# 打印error级别日志
def error(ss):
    global logger
    try:
        logger.error(ss)
    except:
        return


# 打印异常日志
def exception(e):
    global logger
    try:
        logger.exception(e)
        print(e)
    except:
        return


def printfont(value, font='black'):
    # 开头部分：\033[显示方式;前景色;背景色m + 结尾部分：\033[0m
    try:
        if font == 'black':
            return '\033[1;30;0m%s\033[0m' % (value)
        elif font == 'red':
            return '\033[0;31m%s\033[0m' % (value)
        else:
            return print('你输入的字体颜色有误，目前只支持"black"和"red"')
    except Exception as e:
        print(e)
    # print('\033[1;45m 字体不变色，有背景色 \033[0m')  # 有高亮
    # print('\033[1;35;46m 字体有色，且有背景色 \033[0m')  # 有高亮
    # print('\033[0;35;46m 字体有色，且有背景色 \033[0m')  # 无高亮
    # print('\033[0;36m字体变色，但无背景色 \033[0m') #青色


# 调试
if __name__ == '__main__':
    # debug('test')
    logger.debug( 'debug' )
    logger.info( 'aabbc22222' )
    logger.warning( 'WARNING' )
    logger.error( 'error' )
    logger.critical( 'critical' )




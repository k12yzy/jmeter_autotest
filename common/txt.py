#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2019/11/30 23:06
# @File :  txt.py
import re

from common import logger


class Txt:
    """
    用来读写txt文档
    """

    def __init__(self,path):
        #保存文件路径
        self.path = path
        #将txt文件内容保存
        self.data = []
        #将写入的txt文件保存
        self.w = None


    def read(self,coding='utf8'):
        #只读文件 coding: 打开文件的编码，默认utf8
        try:
            #逐行读取
            res = open(self.path,encoding=coding)
            for i in res:
                if len(i)> 1:
                    self.data.append(i)
            #去掉末尾换行、空格
            for i in range(len(self.data)):
                # 处理非法字符
                self.data[i] = self.data[i].encode('utf-8').decode('utf-8-sig')
                self.data[i] = self.data[i].replace('\t','')
                self.data[i] = self.data[i].replace('\n','')
                replace_str =self.data[i][self.data[i].find( '=' ) - 1] # 查询=号左边是否有空格
                replace_str1 = self.data[i][self.data[i].find( '=' ) + 1]# 查询=号右边是否有空格
                if replace_str == ' ':
                    self.data[i] = re.sub(r' ', '',self.data[i],count=1)
                if replace_str1 == ' ':
                    self.data[i] = re.sub(r' ', '',self.data[i],count=1)
            # logger_yzy.debug('读取内容' + str(self.data))
        except Exception as e:
            logger.exception( e )
        #return返回读取的内容
        return self.data



    def write(self,content,coding = 'utf8'):
        # a代表在末尾添加
        self.w = open(self.path,'a',encoding=coding)
        if self.w is None:
            logger.error( 'error：未打开可写入txt文件' )
            return
        #需要写入的内容，若要换行，请自己添加\n
        self.w.write(str(content))
        logger.debug( '写入成功：' + str( content ) )
        return



    def readwrite(self,content ,conding = 'utf8'):
        # 逐行读取
        res = open(self.path,encoding=conding)
        for i in res:
            self.data.append(i)
        # 去掉末尾换行、空格
        for i in range(self.data.__len__()):
            self.data[i] = self.data[i].encode('utf-8').decode('utf-8-sig')
            self.data[i] = self.data[i].replace('\t','')
            self.data[i] = self.data[i].replace('\n','')
        logger.debug( '读取内容' + str( self.data ) )

        # a代表在末尾添加
        self.w = open(self.path,'a',encoding=conding)
        if self.w is None:
            logger.error( 'error：未打开可写入txt文件' )
            return
        #需要写入的内容，若要换行，请自己添加\n
        self.w.write(str(content))
        logger.debug( '写入成功：' + str( content ) )
        return


    def savetxt(self):
        #写入文件后，必须要保存
        if self.w is None:
            logger.error( 'error：未打开可写入txt文件' )
            return
        self.w.close()
        logger.debug( '保存成功' )


# if __name__ = '__main__':
if __name__ == '__main__':
    txt = Txt( '../conf/conf.txt' )
    txt.read()
    print(txt.data)


    # txt.write('哈哈111哈\n')
    # txt.readwrite('213241213\n')
    # txt.savetxt()
    # txt.read()






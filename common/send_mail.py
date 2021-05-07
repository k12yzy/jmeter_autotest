#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time :  2021/4/6 23:09
# @File :  send_mail.py
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from common import logger


class Mail:
    """
        powered by Mr yaxun
        at 2021/4/6
        用来获取配置并发送邮件
    """

    def __init__(self):
        self.mail_info = {}
        # 发件人
        self.mail_info['from'] = 'apitest@demogic.com'
        self.mail_info['username'] = 'apitest@demogic.com'
        # smtp服务器域名
        self.mail_info['hostname'] = 'smtp.' + 'apitest@demogic.com'[
                                               'apitest@demogic.com'.rfind( '@' ) +
                                               1:'apitest@demogic.com'.__len__()]
        # 发件人的密码
        self.mail_info['password'] = 'Api@201906'
        # 收件人
        self.mail_info['to'] = str( 'k12yzy@qq.com,k12yzy@163.com' ).split( ',' )
        # 抄送人
        self.mail_info['cc'] = str( 'yangzongyin@demogic.com' ).split( ',' )
        # 邮件标题
        self.mail_info['mail_subject'] = ''
        self.mail_info['mail_encoding'] = 'gbk'
        # 附件内容
        self.mail_info['filepaths'] = []
        self.mail_info['filenames'] = []

    def send(self, text, mail_subject):
        # 这里使用SMTP_SSL就是默认使用465端口，如果发送失败，可以使用587
        # smtp = SMTP_SSL(self.mail_info['hostname'])
        smtp = SMTP_SSL( 'smtp.exmail.qq.com' )
        # smtp = SMTP_SSL('smtp.163.com')
        smtp.set_debuglevel( 0 )

        ''' SMTP 'ehlo' command.
        Hostname to send for this command defaults to the FQDN of the local
        host.
        '''
        self.mail_info['mail_subject']=f'{mail_subject}接口测试报告'
        smtp.ehlo( self.mail_info['hostname'] )
        smtp.login( self.mail_info['username'], self.mail_info['password'] )

        # 普通HTML邮件
        # msg = MIMEText(text, 'html', self.mail_info['mail_encoding'])

        # 支持附件的邮件
        msg = MIMEMultipart()
        msg.attach( MIMEText( text, 'html', self.mail_info['mail_encoding'] ) )
        msg['Subject'] = Header( self.mail_info['mail_subject'], self.mail_info['mail_encoding'] )
        # msg['from'] = self.mail_info['from']
        h = Header( r'达摩自动化测试', 'utf-8' )
        h.append( '<' + self.mail_info['from'] + '>', 'ascii' )
        msg["from"] = h

        # logger.debug( self.mail_info )
        # logger_yzy.debug(text)
        msg['to'] = ','.join( self.mail_info['to'] )
        receive = self.mail_info['to']

        # 抄送
        if self.mail_info['cc'] is None or self.mail_info['cc'][0].__len__() < 1:
            logger.info( '没有抄送' )
        else:
            msg['cc'] = ','.join( self.mail_info['cc'] )
            receive += self.mail_info['cc']

        # 添加附件
        for i in range( len( self.mail_info['filepaths'] ) ):
            att1 = MIMEText( open( self.mail_info['filepaths'][i], 'rb' ).read(), 'base64', 'utf-8' )
            att1['Content-Type'] = 'application/octet-stream'
            # att1['Content-Disposition'] = 'attachment; filename= "'+self.mail_info['filenames'][i]+'"'
            att1.add_header( 'Content-Disposition', 'attachment', filename=('gbk', '', self.mail_info['filenames'][i]) )
            msg.attach( att1 )

        try:
            smtp.sendmail( self.mail_info['from'], receive, msg.as_string() )
            smtp.quit()
            logger.info( '邮件发送：--> 成功(雅讯邮箱)' )
        except Exception as e:
            logger.info( '邮件发送失败：' )
            logger.info( e )


if __name__ == '__main__':
    mail = Mail()
    file = 'OpenApiTest_2021_0403_203838.html'
    mail.mail_info['filepaths'] = ['D:\MyTestApi\OpenApiTest_2021_0403_203838.html']
    mail.mail_info['filenames'] = ['OpenApiTest_2021_0403_203838.html']
    html = open( file, 'r', encoding='utf-8' ).read()
    mail.send( html, '自动化测试')

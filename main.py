import time
import requests
from bs4 import BeautifulSoup
import os
from email.mime.text import MIMEText
import smtplib

url = 'https://yzw.xpu.edu.cn/index/tzgg1.htm'
infoNew = []
infoOld = []
title = ""

key = os.environ.get('KEY', '')
send = os.environ.get('SEND', '')
receive = os.environ.get('RECEIVE', '')


def sendMessage(text, send, receive, key, ):
    msg_from = send  # 发送方邮箱
    passwd = key  # 填入发送方邮箱的授权码
    msg_to = receive  # 收件人邮箱

    subject = "通知更新"  # 主题
    content = text  # 正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    finally:
        s.quit()


if os.path.exists("info.txt"):
    # 读取本地数据
    with open("info.txt", "r", encoding='utf-8') as file:
        infoOld = file.readlines()
    # print(infoOld)

# 获取新内容
soup = BeautifulSoup(requests.get(url).content.decode('utf-8'), "html.parser")
html = soup.select("body > div.main.cl > div.wape-right > ul > li")

for review in html:
    titleName = review.select("a")[0].get("title")
    titleTime = review.select("span")[0].text
    title = titleName + titleTime + "\n"
    infoNew.append(title)

# print(infoNew)

if infoNew != infoOld:
    sendMessage("请到官网查看")

# 更新通知列表
with open("info.txt", "w", encoding='utf-8') as f:
    f.writelines(infoNew)

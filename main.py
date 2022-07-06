import time
import requests
from bs4 import BeautifulSoup
import os
from email.mime.text import MIMEText
import smtplib

url = 'https://yzw.xpu.edu.cn/index/tzgg1.htm'

key = os.environ.get('KEY', '')
send = os.environ.get('SEND', '')
receive = os.environ.get('RECEIVE', '')

# oneday = 86400
"一天的时间戳相差 86400"


def sendMessage(text, send, receive, key):
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


# 获取当前时日
def get_time(fmt: str = '%Y-%m-%d') -> str:
    ts = time.time()
    ta = time.localtime(ts)
    t = time.strftime(fmt, ta)
    return t


# 日期转换成时间戳
def unix_time(dt):
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    return timestamp


print("今天日期为：" + get_time())
now = int(unix_time(get_time()))

soup = BeautifulSoup(requests.get(url).content.decode('utf-8'), "html.parser")
html = soup.select("body > div.main.cl > div.wape-right > ul > li")

for review in html[:1]:
    titleName = review.select("a")[0].get("title")
    titleTime = review.select("span")[0].text
    newUrl = "https://yzw.xpu.edu.cn/" + review.select("a")[0].get("href")[2:]

    if unix_time(titleTime) == now:
        print("新通知提醒,请访问:\n" + newUrl)
        sendMessage("新通知提醒,请访问:\n" + newUrl, send, receive, key)
    else:
        print("暂无新通知")

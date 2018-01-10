# coding:utf-8

from urllib import request
from urllib import error
import sys
import importlib
import re
import io
import time
import xlsxwriter
from multiprocessing import Pool
from models import session,Qshi

"""
#第二页：https://www.qiushibaike.com/pic/page/2/?s=5049862
#第三页：https://www.qiushibaike.com/pic/page/3/?s=5049862
page=1

logo_list=[]
title_list=[]
content_list=[]
img_list=[]

hearders={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}


logo_pattern=re.compile(u'<div.*?class="author clearfix">.*?<img.*?src="(.*?)".*?</div>',re.S)#头像地址
title_pattern=re.compile(u'<div.*?class="author clearfix">.*?<img.*?alt="(.*?)">.*?</div>',re.S)#用户名
content_pattern=re.compile(u'<div.*?class="content">.*?<span>(.*?)</span>.*?</div>',re.S)#内容
img_pattern=re.compile(u'<div.*?class="thumb">.*?<img.*?src="(.*?)".*?>.*?</div>',re.S)#图片地址

while page<=35:
    url = 'https://www.qiushibaike.com/pic/page/' + str(page) + '/?s=5049862'
    html = request.Request(url=url, headers=hearders)
    response = request.urlopen(html)
    html_str = response.read().decode('utf-8')

    logo_item = re.findall(logo_pattern, html_str)
    for v in logo_item:
        logo_list.append(v)
    # print(logo_item)
    print('第%d页logo_item的长度为%d'%(page,len(logo_item)))

    title_item = re.findall(title_pattern, html_str)
    for v in title_item:
        title_list.append(v)
    # print(title_item)
    print('第%d页title_item的长度为%d' % (page, len(title_item)))

    content_item = re.findall(content_pattern, html_str)
    for v in content_item:
        content_list.append(v)
    # print(content_item)
    print('第%d页content_item的长度为%d' % (page, len(content_item)))

    img_item = re.findall(img_pattern, html_str)
    for v in img_item:
        img_list.append(v)
    # print(img_item)
    print('第%d页img_item的长度为%d' % (page, len(img_item)))
    page=page+1
print(len(logo_list))
print(len(title_list))
print(len(content_list))
print(len(img_list))
"""


class QiuShi_Re:
    def __init__(self):
        importlib.reload(sys)
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        self.page = 1
        self.endpage = 35

        self.logo_list = []
        self.title_list = []
        self.content_list = []
        self.img_list = []

        self.hearders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
        # Referer
        self.filepath = 'static/qiushi.txt'
        self.xlsxpath = 'static/qiushi.xlsx'
        self.logoPath='static/logo'
        self.imgPath='static/img'

    def get_html(self, page):
        try:
            URL = 'https://www.qiushibaike.com/pic/page/' + str(page) + '/?s=5049862'
            html = request.Request(url=URL, headers=self.hearders)
            response = request.urlopen(html)
            html_str = response.read().decode('utf-8')
            return html_str
        except error:
            if hasattr(error, 'reason'):
                print('抓取失败,具体原因：', error.reason)
        #URLError与HTMLError双重
        # except error.URLError as e:
        #     if hasattr(e, 'code'):
        #         print("HTTPError" + e.code)
        #     elif hasattr(e, 'reason'):
        #         print("URLError" + e.reason)

    def get_data(self,page):
        print('---------------------------------------------------------------------------------------------')
        print("开始爬取第%d页。。。"%page)
        logo_pattern = re.compile(u'<div.*?class="author clearfix">.*?<img.*?src="(.*?)".*?</div>', re.S)  # 头像地址
        title_pattern = re.compile(u'<div.*?class="author clearfix">.*?<img.*?alt="(.*?)".*?</div>', re.S)  # 用户名
        content_pattern = re.compile(u'<div.*?class="content">.*?<span>(.*?)</span>.*?</div>', re.S)  # 内容
        img_pattern = re.compile(u'<div.*?class="thumb">.*?<img.*?src="(.*?)".*?>.*?</div>', re.S)  # 图片地址
        html = self.get_html(page)
        logo_item = re.findall(logo_pattern, html)
        print("%d页的logo_item: "%page)
        print(logo_item)
        for v in logo_item:
            self.logo_list.append(v)
            print(v)
        print('第%d页logo_item的长度为%d' % (page, len(logo_item)))
        # print(len(self.logo_list))

        title_item = re.findall(title_pattern, html)
        # print(title_item)
        for v in title_item:
            self.title_list.append(v)
        # print('第%d页title_item的长度为%d' % (page, len(title_item)))
        # print(len(self.title_list))

        content_item = re.findall(content_pattern, html)
        # print(content_item)
        for v in content_item:
            self.content_list.append(v)
        # print('第%d页content_item的长度为%d' % (page, len(content_item)))
        # print(len(self.content_list))

        img_item = re.findall(img_pattern, html)
        # print(len(img_item))
        for v in img_item:
            self.img_list.append(v)
        # print('第%d页img_item的长度为%d' % (page, len(img_item)))
        # print(len(self.img_list))
        print('---------------------------------------------------------------------------------------------')
        print('第%d页爬取结束！'%page)
        print(img_item[0])
        print(img_item[19])
        self.storage_in_mysql(len(title_item),title_item,content_item,logo_item,img_item)
        time.sleep(1)

    def output_txt(self):#文本显示
        f = open(self.filepath, 'w', encoding='utf-8')
        try:
            for v in range(0, len(self.logo_list)):
                f.write('头像地址' + self.logo_list[v] + '\r\n')
                f.write('用户名：' + self.title_list[v] + '\r\n')
                f.write('内容:' + self.content_list[v] + '\r\n')
                f.write('图片地址：' + self.img_list[v] + '\r\n\r\n')
                # print('文件写入成功...')
        finally:
            f.close()

    def output_xlsx_row(self):#横向表格显示
        row = 1
        col = 0
        w = xlsxwriter.Workbook(self.xlsxpath)
        worksheet = w.add_worksheet(u"所有数据")
        worksheet.write("A1", u"头像地址")
        worksheet.write("B1", u'用户名')
        worksheet.write('C1', u'内容')
        worksheet.write('D1', u'图片地址')
        for v in range(0, len(self.logo_list)):
            worksheet.write(row, col, self.logo_list[v])
            worksheet.write(row,col+1,self.title_list[v])
            worksheet.write(row, col+2, self.content_list[v])
            worksheet.write(row,col+3,self.img_list[v])
            row += 1
        w.close()

    def storage_in_mysql(self,length,name_list,content_list,logo_url_list,img_url_list):
        for v in range(0,length):
            print("v ",v)
            print("length",length)
            print("name数组长度： ",len(name_list))
            name=name_list[v]
            content=content_list[v]

            logo_url=logo_url_list[v]
            logo_str=str(logo_url).rsplit('/',1)[1]
            logo=self.logoPath+logo_str

            img_url = img_url_list[v]
            img_str = str(img_url).rsplit('/', 1)[1]
            img = self.imgPath + img_str

            data = Qshi(name=name, logo=logo, content=content, img=img)
            session.add(data)
            session.commit()
            print('第%d条数据存储成功！'%v)
        session.close()

    def main(self):
        print('正在从糗事百科抓取数据...')
        time1=time.time()
        while self.page<=1:
            self.get_data(self.page)
            print("第%d页抓取完毕!" % self.page)
            self.page+=1

        time2=time.time()
        print("单进程抓取时间: ",time2-time1)
        """
        time3=time.time()
        pool=Pool(4)
        # for v in range(1,11):
        #     pool.apply_async(self.get_data,args=(v,))
        #     print("第%d页抓取完毕!" % v)
        pool.map(self.get_data,range(1,11))
        pool.close()
        pool.join()
        time4=time.time()
        print("多进程抓取时间： ",time4-time3)
        """
        print(len(self.logo_list))
        print(len(self.title_list))
        print(len(self.content_list))
        print(len(self.img_list))
        self.output_xlsx_row()
        print('抓取完毕...')

if __name__=='__main__':
    Spider = QiuShi_Re()
    Spider.main()

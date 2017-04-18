# -*- coding: utf-8 -*-
# @Time    : 2017/3/8 19:47
# @Author  : euscu
# @remark  : 
__author__ = 'euscu'
from selenium import webdriver
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import csv

nowurl = ""
urltotal = set([])  # 总共爬到的url
message = ''
nowpage = 0


def login_url(keywords, frompage, totalpage, path):
    global urltotal
    global message
    global nowpage
    myurl = 'https://s.1688.com/company/company_search.htm'
    driver = webdriver.Firefox()
    driver.get(myurl)
    # 以下做了两次验证，因为可能会出现先跳到商户界面又出现让你输入验证码的情况
    while 1:
        pattern = re.compile(r"https://s.1688.com/company")
        if re.match(pattern, driver.current_url):
            print("success")
            break
        else:
            print("fail")
            time.sleep(5)
    print("成功")
    driver.get(myurl)
    # 可能跳转至验证码界面
    time.sleep(5)
    while 1:
        pattern = re.compile(r"https://s.1688.com/company")
        if re.match(pattern, driver.current_url):
            print("success")
            break
        else:
            print("fail")
            time.sleep(5)

    # 获取driver的cookies，并转化成requests用的cookies
    mycookies = driver.get_cookies()
    reqcookies = {}
    # reqcookies是requests请求用的cookie。我将firefox登录后的cookies放进reqcookies。
    # 没有登录状态无法爬取手机号码
    for cookie in mycookies:
        reqcookies[cookie['name']] = cookie['value']
    # 等待加载
    driver.find_element_by_xpath('//*[@id="q"]').send_keys(keywords)
    driver.find_element_by_xpath('//*[@id="s_search_form"]/fieldset/div[2]/div[1]/div/div[2]/button').click()
    # 等待加载
    time.sleep(2)
    # 如果不是第一页开始就先跳到多少页
    if not frompage == 1:
        beginelement = driver.find_element_by_name('beginPage')
        beginelement.click()
        beginelement.clear()
        beginelement.send_keys(frompage)
        beginelement.send_keys(Keys.RETURN)
        time.sleep(5)
        nowpage = frompage
    else:
        nowpage = 1

    f = open(path + '/' + keywords + '_url.csv', 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(('网址',))
    element = driver.find_elements_by_class_name('noresult-content')  # 用来判断当前页面是否有内容
    print("judge success")

    while not element and nowpage <= totalpage:
        while 1 == 1:
            pattern = re.compile(r"https://sec.1688.com/")
            if not re.match(pattern, driver.current_url):
                break
        print(driver.current_url)
        for myelement in driver.find_elements_by_class_name('sm-offerResult-areaaddress'):
            url = myelement.get_attribute('href')
            urltotal.add(url)
            writer.writerow((url,))
        wait = WebDriverWait(driver, 10)
        print("点击下一页")
        time.sleep(5)
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'page-next')))
        except Exception:
            break
        driver.find_element_by_class_name('page-next').click()
        nowpage = nowpage + 1
        time.sleep(5)
        element = driver.find_elements_by_class_name('noresult-content')
    message = 'url收集完毕'
    print("一共收集了%d条数据" % len(urltotal))
    driver.quit()
    f.close()

    # 反爬user-agent，15个，循环使用
    myheaders = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'},
                 {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'},
                 {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'},
                 {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 '
                                '(KHTML, like Gecko) Version/5.1 Safari/534.50'},
                 {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 '
                                '(KHTML, like Gecko) Version/5.1 Safari/534.50'},
                 {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
                 {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
                 {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
                 {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
                 {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
                 {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; '
                                'SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'},
                 {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
                 {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)'},
                 {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
                 {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'}]
    message = '开始解析URL并存储数据'
    g = open(path + '/' + keywords + '_data.csv', 'a', newline='')
    writer = csv.writer(g)
    writer.writerow(('供应商', '电话', '手机', '联系人', '地址', '网址'))
    i = 0
    for url in urltotal:
        if i >= 750:
            i = i - 750
        if i % 50 == 0:
            myheader = myheaders[i // 50]
        try:
            response = requests.get(url, cookies=reqcookies, headers=myheader)
            parseurl(response.text, writer)
            i = i + 1
        except Exception:
            print(Exception.__name__)
            continue
    g.close()
    message = 'success'


# 解析requests.get出的代码
def parseurl(info, writer):
    global message
    gongyingshang = re.compile('<h4>(.*?)</h4>')
    dianhua = re.compile(';话：.*?<dd>(.*?)</dd>', re.S)
    shouji = re.compile('<dt>移动电话：</dt>.*?<dd.*?>(.*?)</dd>', re.S)
    lianxiren = re.compile('<a.*?class="membername".*?>(.*?)</a>')
    dizhi = re.compile('"address">(.*?)</dd>', re.S)
    wangzhi = re.compile('<a.*?href="(.*?)".*?class=.*?subdomain.*?')
    gys = re.findall(gongyingshang, info)
    dianhua = re.findall(dianhua, info)
    shouji = re.findall(shouji, info)
    lxr = re.findall(lianxiren, info)
    address = re.findall(dizhi, info)
    netaddr = re.findall(wangzhi, info)
    if gys:
        gys = gys[0]
    else:
        gys = '空'
    if dianhua:
        dianhua = dianhua[0]
    else:
        dianhua = '空'
    if shouji:
        shouji = shouji[0].strip()
    else:
        shouji = '空'
    if lxr:
        lxr = lxr[0].strip()
    else:
        lxr = '空'
    if address:
        address = address[0].strip()
    else:
        address = '空'
    if netaddr:
        netaddr = netaddr[0].strip()
    else:
        netaddr = '空'
    print(gys, dianhua, shouji, lxr, address, netaddr)
    message = gys, dianhua, shouji, lxr, address, netaddr
    writer.writerow((gys, dianhua, shouji, lxr, address, netaddr))

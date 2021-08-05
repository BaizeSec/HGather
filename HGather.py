<<<<<<< HEAD
# -*- coding: utf-8 -*-
import sys
import re
import json
import requests
import argparse
import base64
import urllib
import time

reload(sys) 
sys.setdefaultencoding('utf-8')

config = open('config.txt','r')
header = {
        'Authorization':config.readline()
    }
api=('https://api.fofa.so/v1/search')

def parser(text):
    url_list=re.findall('"link":"(.*?)"', text)
    ip_list=re.findall('"ip":"(.*?)"', text)
    title_list=re.findall('"title":"(.*?)"', text)
    #country_list=re.findall('"country":"(.*?)"', text)
    #city_list=re.findall('"city":"(.*?)"', text)
    return url_list,ip_list,title_list


def request(url):
    try:
        text = requests.get(url,headers=header).text
        return text
    except requests.exceptions.ConnectTimeout as a:
        print(a)
    except requests.exceptions.ProxyError as b:
        print(b)
    except requests.exceptions.ConnectTimeout as c:
        print(c)
    except requests.exceptions.ConnectionError as d:
        print(d)


def pn_count(url):
    text = request(url)
    total_number = re.findall('"total":(\d*)',text)
    total_number=int(total_number[0])
    if (total_number % 10):
        pn = total_number/10 + 1
    else:
        pn = total_number/10
    return pn


def run(text):
    if args.out:
        for i in range(len(text[0])):
            result=("URL：{:<43}".format(text[0][i])+"\tIP：{:<15}".format(text[1][i])+"\ttitle：{:<20}".format(text[2][i]))
            print(result.encode("GBK","ignore"))
            args.out.write(result+"\n")
    else:
        for i in range(len(text[0])):
            #print("URL："+text[0][i]+"\tIP："+text[1][i]+"\ttitle："+text[2][i]+"\t城市："+text[3][i]+text[4][i])
            result=("URL：{:<43}".format(text[0][i])+"\tIP：{:<20}".format(text[1][i])+"\ttitle：{:<20}".format(text[2][i]))
            print(result.encode("GBK","ignore"))


def C_ip(ip_list):
    print(u"\n*************************************************************\n")
    c_dict={}
    for ip in ip_list:
        try:
            c = re.findall('((?:\d*\.){2}(?:\d)*)',ip)
            c_y = c[0]
            if not c_dict.has_key(c_y):
                c_dict[c_y] = 1
            else:
                c_dict[c_y] +=1
        except:
            continue
    print(u"您搜索的结果共包含{}个C段IP，统计结果如下：\n".format(len(c_dict)))
    c_dict=sorted(c_dict.items(), key=lambda item:item[1], reverse=True)
    for i in range(len(c_dict)):
        print(U"C段：{}.0/24\t{}条数据在此C段中".format(c_dict[i][0],c_dict[i][1]))



def argument():
    parser = argparse.ArgumentParser(prog='HGather', description='资产收集工具——HGather by 白泽Sec-ahui')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q','--qbase64',help=u'指定FOFA中的搜索条件（base64编码）',type=str)
    group.add_argument('-i','--ip',help=u'指定要搜索的IP或IP段，例如：-i 192.168.0.1/24',type=str)
    parser.add_argument('-o','--out',help=u'指定要导出的文件名，例如：-o test.txt',type=argparse.FileType('w+'))
    global args
    args = parser.parse_args()


def check(pn_number):
    if pn_number == 0:
        print(u"您搜索的结果返回为空，请检查您的参数是否正确！")
        sys.exit()
    else:
        print(u"您搜索的结果共有{}页。".format(pn_number))
        time.sleep(2)


def check_cookie(request_result):
    if u"资源访问权限不足" in request_result:
        print(u"您的COOKIE已失效，只能输出前两页内容，请更新您的配置文件！")
        sys.exit()


def main():
    argument()
    print(u"*************************************************************\n资产收集工具——HGather by 白泽Sec-ahui\n联系方式：aaaahuia@163.com\nrunning!\n*************************************************************")
    time.sleep(3)
    if args.qbase64:
        qbase64 = urllib.quote(args.qbase64)
        url = api+"?qbase64="+qbase64
        pn_number = pn_count(url)
        check(pn_number)
        text1_list=[]
        for i in range(pn_number):
            url_y = url + "&pn=" + str(i)
            request_result=request(url_y)
            check_cookie(request_result)
            text = parser(request_result)
            run(text)
            text1_list.extend(text[1])
        C_ip(text1_list)
    if args.ip:
        if not re.match('(?:[0-9]{1,3}\.){3}(?:[0-9]){1,3}(?:\/\d*)?', args.ip):
            print(u"您输入的IP或IP段有误！")
        else:
            query = 'ip="{}" && type="subdomain"'.format(args.ip)
            qbase64 = urllib.quote(base64.b64encode(query))
            url = api+"?qbase64="+qbase64
            pn_number = pn_count(url)
            check(pn_number)
            text1_list=[]
            for i in range(pn_number):
                url_y = url + "&pn=" + str(i)
                request_result=request(url_y)
                check_cookie(request_result)
                text = parser(request_result)
                run(text)
                text1_list.extend(text[1])
            C_ip(text1_list)


if __name__ == "__main__":
=======
# -*- coding: utf-8 -*-
import sys
import re
import json
import requests
import argparse
import base64
import urllib
import time
from colorama import init,Fore,Back,Style

reload(sys) 
sys.setdefaultencoding('utf-8')
init(autoreset=True)

config = open('config.txt','r')
header = {
        'Authorization':config.readline()
    }
api=('https://api.fofa.so/v1/search')

def parser(text):
    url_list=re.findall('"link":"(.*?)"', text)
    ip_list=re.findall('"ip":"(.*?)"', text)
    title_list=re.findall('"title":"(.*?)"', text)
    #country_list=re.findall('"country":"(.*?)"', text)
    #city_list=re.findall('"city":"(.*?)"', text)
    return url_list,ip_list,title_list


def request(url):
    try:
        text = requests.get(url,headers=header).text
        return text
    except requests.exceptions.ConnectTimeout as a:
        print(a)
    except requests.exceptions.ProxyError as b:
        print(b)
    except requests.exceptions.ConnectTimeout as c:
        print(c)
    except requests.exceptions.ConnectionError as d:
        print(d)


def pn_count(url):
    text = request(url)
    total_number = re.findall('"total":(\d*)',text)
    total_number=int(total_number[0])
    if (total_number % 10):
        pn = total_number/10 + 1
    else:
        pn = total_number/10
    return pn



def run(text):
    if args.out:
        for i in range(len(text[0])):
            if u"后台" in text[2][i] or u"系统" in text[2][i] or u"管理" in text[2][i] or u"平台" in text[2][i]:
                print(('\033[1;32;40m{}\033[0m'.format(result)).encode("GBK","ignore"))
            else:
                print(result.encode("GBK","ignore"))
            args.out.write(result+"\n")
    else:
        for i in range(len(text[0])):
            #print("URL："+text[0][i]+"\tIP："+text[1][i]+"\ttitle："+text[2][i]+"\t城市："+text[3][i]+text[4][i])
            result=("URL：{:<43}".format(text[0][i])+"\tIP：{:<20}".format(text[1][i])+"\ttitle：{:<20}".format(text[2][i]))
            if u"后台" in text[2][i] or u"系统" in text[2][i] or u"管理" in text[2][i] or u"平台" in text[2][i]:
                print(('\033[1;32;40m{}\033[0m'.format(result)).encode("GBK","ignore"))
            else:
                print(result.encode("GBK","ignore"))


def C_ip(ip_list):
    print(u"\n*************************************************************\n")
    c_dict={}
    for ip in ip_list:
        try:
            c = re.findall('((?:\d*\.){2}(?:\d)*)',ip)
            c_y = c[0]
            if not c_dict.has_key(c_y):
                c_dict[c_y] = 1
            else:
                c_dict[c_y] +=1
        except:
            continue
    print(u"您搜索的结果共包含{}个C段IP，统计结果如下：\n".format(len(c_dict)))
    c_dict=sorted(c_dict.items(), key=lambda item:item[1], reverse=True)
    for i in range(len(c_dict)):
        print(U"C段：{}.0/24\t{}条数据在此C段中".format(c_dict[i][0],c_dict[i][1]))



def argument():
    parser = argparse.ArgumentParser(prog='HGather', description='资产收集工具——HGather by 白泽Sec-ahui')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q','--qbase64',help=u'指定FOFA中的搜索条件（base64编码）',type=str)
    group.add_argument('-i','--ip',help=u'指定要搜索的IP或IP段，例如：-i 192.168.0.1/24',type=str)
    parser.add_argument('-o','--out',help=u'指定要导出的文件名，例如：-o test.txt',type=argparse.FileType('w+'))
    global args
    args = parser.parse_args()


def check(pn_number):
    if pn_number == 0:
        print(u"您搜索的结果返回为空，请检查您的参数是否正确！")
        sys.exit()
    else:
        print(u"您搜索的结果共有{}页。".format(pn_number))
        time.sleep(2)


def check_cookie(request_result):
    if u"资源访问权限不足" in request_result:
        print(u"您的COOKIE已失效，只能输出前两页内容，请更新您的配置文件！")
        sys.exit()


def main():
    argument()
    print(u"*************************************************************\n资产收集工具——HGather by 白泽Sec-ahui\n联系方式：aaaahuia@163.com\nrunning!\n*************************************************************")
    time.sleep(3)
    if args.qbase64:
        qbase64 = urllib.quote(args.qbase64)
        url = api+"?qbase64="+qbase64
        pn_number = pn_count(url)
        check(pn_number)
        text1_list=[]
        for i in range(pn_number):
            url_y = url + "&pn=" + str(i)
            request_result=request(url_y)
            check_cookie(request_result)
            text = parser(request_result)
            run(text)
            text1_list.extend(text[1])
        C_ip(text1_list)
    if args.ip:
        if not re.match('(?:[0-9]{1,3}\.){3}(?:[0-9]){1,3}(?:\/\d*)?', args.ip):
            print(u"您输入的IP或IP段有误！")
        else:
            query = 'ip="{}" && type="subdomain"'.format(args.ip)
            qbase64 = urllib.quote(base64.b64encode(query))
            url = api+"?qbase64="+qbase64
            pn_number = pn_count(url)
            check(pn_number)
            text1_list=[]
            for i in range(pn_number):
                url_y = url + "&pn=" + str(i)
                request_result=request(url_y)
                check_cookie(request_result)
                text = parser(request_result)
                run(text)
                text1_list.extend(text[1])
            C_ip(text1_list)

if __name__ == "__main__":
>>>>>>> master
    main()
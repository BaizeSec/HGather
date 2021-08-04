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
    text = requests.get(url,headers=header).text
    return text


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



def argument():
    parser = argparse.ArgumentParser(prog='HGather', description='资产收集工具——HGather by 白泽Sec-ahui')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q','--qbase64',help=u'指定FOFA中的搜索条件（base64编码）',type=str)
    group.add_argument('-i','--ip',help=u'指定要搜索的IP或IP段，例如：-i 192.168.0.1/24',type=str)
    parser.add_argument('-o','--out',help=u'指定要导出的文件名，例如：-o test.txt',type=argparse.FileType('w+'))
    global args
    args = parser.parse_args()



def main():
    argument()
    print(u"*************************************************************\n资产收集工具——HGather by 白泽Sec-ahui\n联系方式：aaaahuia@163.com\nrunning!\n*************************************************************")
    time.sleep(3)
    if args.qbase64:
        qbase64 = urllib.quote(args.qbase64)
        url = api+"?qbase64="+qbase64
        pn_number = pn_count(url)
        for i in range(pn_number):
            url_y = url + "&pn=" + str(i)
            text = parser(request(url_y))
            run(text)
    if args.ip:
        if not re.match('(?:[0-9]{1,3}\.){3}(?:[0-9]){1,3}(?:\/\d*)?', args.ip):
            print(u"您输入的IP或IP段有误！")
        else:
            query = 'ip="{}" && type="subdomain"'.format(args.ip)
            qbase64 = urllib.quote(base64.b64encode(query))
            url = api+"?qbase64="+qbase64
            pn_number = pn_count(url)
            print(pn_number)
            for i in range(pn_number):
                url_y = url + "&pn=" + str(i)
                text = parser(request(url_y))
                run(text)


if __name__ == "__main__":
    main()
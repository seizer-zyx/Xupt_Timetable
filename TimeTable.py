from selenium import webdriver
from selenium.webdriver import ChromeOptions
import json
import requests
import time
import sys
import os


class TimeTable:
    def __init__(self, url, uname, pw, year='', flag=0):
        self.url = url
        self.uname = uname
        self.__pw = pw
        self.year = year
        self.flag = flag

    def __get_Identity(self):
        options = ChromeOptions()
        # 不显示浏览器窗口打开
        options.add_argument('--headless')
        # 减少不必要的日志输出
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # 添加 User-Agent 头
        options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"')
        # 访问课程表所在网页
        driver = webdriver.Chrome(executable_path=sys.path[0]+'/chromedriver.exe', options=options)
        driver.get(self.url)
        # 用户登录
        driver.find_element_by_xpath('//*[@id="yhm"]').send_keys(self.uname)
        driver.find_element_by_xpath('//*[@id="mm"]').send_keys(self.__pw)
        os.system('cls')
        print('正在填入信息中---')
        total = 50
        for i in range(total):
            if i+1 == total:
                percent = 100.0
                print('进度: ' + '%s [%d/%d]' % (str(percent)+'%', (i+1)*2, 100), end='\n')
            else:
                percent = round(1.0 * i / total * 100, 2)
                print('进度: ' + '%s [%d/%d]' % (str(percent)+'%', i+1, 100), end='\r')
            time.sleep(0.01)

        driver.find_element_by_id("dl").click()
        os.system('cls')
        print('正在填入信息中---')
        print('进度: ' + '%s [%d/%d]' % ('100'+'%', 100, 100), end='\n')
        print('正在登录中---')
        total = 100
        for i in range(total):
            if i+1 == total:
                print('进度: ' + '%s [%d/%d]' % ('100'+'%', i+1, 100), end='\n')
            else:
                percent = round(1.0 * i / total * 100, 2)
                print('进度: ' + '%s [%d/%d]' % ('100'+'%', i+1, 100), end='\r')
            time.sleep(0.01)
        time.sleep(1)
        # 获取登录凭证
        jsessionid = driver.get_cookies()[0]['value']
        driver.quit()
        cookies = {
            "JSESSIONID": jsessionid
        }
        return cookies

    def get_timetable(self):
        semester = '12' if self.flag else '3'   # 3是第一学期的课表，12是第二学期的课表
        post_data = {
            'xnm': str(self.year),
            'xqm': semester,
            'kzlx': 'ck'
        }
        cookies = self.__get_Identity()
        r = requests.post(self.url, data=post_data, cookies=cookies)
        r.encoding = r.apparent_encoding
        self.timetable_json = json.loads(r.text)
        return self.timetable_json

    def downfile_timetable(self, filename='timetable.json', path=sys.path[0]+'/file/'):
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path + filename, 'w')
        json.dump(self.timetable_json, f)
        f.close()

    def loadfile_timetable(self, filename='timetable.json', path=sys.path[0]+'/file/'):
        if not os.path.exists(path + filename):
            print("The loaded directory or file does not exist!")
            sys.exit(0)
        f = open(path + filename, 'r')
        self.timetable_json = json.load(f)
        f.close()

    def format_timetable(self):
        tables = self.timetable_json['kbList']
        print('\n' + '获取到的课程表如下:' + '\n')
        print('-------------------------------------------------------------------------')
        filename = sys.path[0] + '/timetable.data'
        print(filename)
        if os.path.exists(filename):
            os.remove(filename)
        f = open(filename, 'a', encoding='utf-8')
        for table in tables:
            # 上课时间
            print(table['xqjmc'] + table['jc'], end=' ')
            f.write(table['xqjmc'] + table['jc'] + ' ')
            # 上课地点
            print(table['cdmc'], end=' ')
            f.write(table['cdmc'] + ' ')
            # 课程名字
            print(table['kcmc'], end=' ')
            f.write(table['kcmc'] + ' ')
            # 课程安排
            print(table['zcd'], end=' ')
            f.write(table['zcd'] + '\n')
            # # 教师姓名
            # print(table['xm'])
            # # 课程类型
            # print(table['kclb'])
            # # 考试类型
            # print(table['khfsmc'])
            print()

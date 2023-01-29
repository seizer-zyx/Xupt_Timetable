from lxml import etree
import base64
import rsa
import json
import requests
import time
import sys
import os


class TimeTable:
    def __init__(self, uname, pw, year='2022', flag=0):
        self.s = requests.session()
        self.timetable_api = "http://www.zfjw.xupt.edu.cn/jwglxt/kbcx/xskbcx_cxXsgrkb.html"
        self.__get_Identity(uname, pw)
        self.year = year
        self.flag = flag
        
    def __get_Identity(self, uname, pw):
        def get_token():
            token_url = "http://www.zfjw.xupt.edu.cn/jwglxt/xtgl/login_slogin.html"
            try:
                r = self.s.get(token_url, timeout=10)
            except requests.exceptions.ConnectTimeout:
                print()
                print("获取token超时！")
                sys.exit(0)
            tree = etree.HTML(r.text)
            csrftoken = tree.xpath('/html/body/div[1]/div[2]/div[2]/form/input[1]/@value')[0]
            return csrftoken

        def get_encrypt_pw(password):
            def rsa_encrypt(rsa_n, rsa_e, message):
                key = rsa.PublicKey(rsa_n, rsa_e)
                message = base64.b64encode(rsa.encrypt(message.encode(), key)).decode()
                return message
            rsa_url = "http://www.zfjw.xupt.edu.cn/jwglxt/xtgl/login_getPublicKey.html"
            try:
                js = self.s.get(rsa_url, timeout=10).json()
            except requests.exceptions.ConnectTimeout:
                print()
                print("获取rsa加密参数超时！")
                sys.exit(0)
            n = int.from_bytes(base64.b64decode(js['modulus'].encode()), byteorder='big')
            e = int.from_bytes(base64.b64decode(js['exponent'].encode()), byteorder='big')
            mm = rsa_encrypt(n, e, password)
            return mm
    
        login_url = "http://www.zfjw.xupt.edu.cn/jwglxt/xtgl/login_slogin.html"
        csrftoken = get_token()
        mm = get_encrypt_pw(pw)
        login_date = {
            "csrftoken": csrftoken,
            "language": "zh_CN",
            "yhm": uname,
            "mm": mm
        }
        try:
            r = self.s.post(login_url, data=login_date, timeout=10, allow_redirects=False)
        except requests.exceptions.ConnectTimeout:
            print()
            print("登录超时！")
            sys.exit(0)
        if r.status_code != 302:
            print()
            print("请检查您的用户名和密码是否正确")
            sys.exit(0)


    def get_timetable(self):
        semester = '12' if self.flag else '3'   # 3是第一学期的课表，12是第二学期的课表
        post_data = {
            'xnm': str(self.year),
            'xqm': semester,
            'kzlx': 'ck'
        }
        r = self.s.post(self.timetable_api, data=post_data)
        r.encoding = r.apparent_encoding
        try:
            timetable_json = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print()
            print("接口获取课表失败！")
            sys.exit(0)
        if timetable_json['kbList'] == []:
            print()
            print("该学年学期的课表尚未开放！")
            sys.exit(0)
        return timetable_json

    def downfile_timetable(self, timetable_json):
        try:
            print(sys.path[0])
            f = open(sys.path[0] + "/timetable.json", 'w')
            json.dump(timetable_json, f)
            f.close()
            return True
        except Exception:
            return False
        

    # 格式化输出课表并保存至./timetable.data文件中
    def format_timetable(self, timetable_json):
        tables = timetable_json['kbList']
        print('\n' + '获取到的课程表如下:' + '\n')
        print('-------------------------------------------------------------------------')
        filename = sys.path[0] + '/timetable.data'
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

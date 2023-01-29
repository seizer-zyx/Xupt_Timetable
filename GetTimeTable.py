from TimeTable import TimeTable
import getopt
import sys


def GetTimeTable(args):
    uname = ''
    pw = ''
    year = ''
    flag = 0
    download = False
    try:
        opts, args = getopt.getopt(args, 'hu:p:y:f:', ['uname=', 'pw=', 'year=', 'help', 'download'])
    except getopt.GetoptError:
        print('Please use -h or --help for help')
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('Usage: GetTimeTable.py [-u|--uname] username [-p|--pw] password [-h|--help]')
            print('Required:')
            print('\t -u username, --uname=username \t I think this is your school number')
            print('\t -p password, --pw=password \t Your password, this is very important')
            print('\t -y year, --year=year \t Which year to check (default: 2022)')
            print('\t -f (0 | 1)  \t 0 for the first semester, 1 for the second semester (default: 0)')
            print('Options:')
            print('\t --download Download the raw json data')
            print('\t -h, --help \t show this help message and exit')
            sys.exit(0)
        elif opt in ("-u", "--uname"):
            uname = arg
        elif opt in ("-p", "--pw"):
            pw = arg
        elif opt in ("-y", "--year"):
            year = arg
        elif opt in ("-f"):
            flag = int(arg)
        elif opt in ('--download'):
            download = True
    if uname and pw:
        if year and flag:
            time_table = TimeTable(uname, pw, year, flag)
        time_table = TimeTable(uname, pw)
        timetable_json = time_table.get_timetable()
        if download:
            if not time_table.downfile_timetable(timetable_json):
                print("下载原始数据失败！")
        time_table.format_timetable(timetable_json)
    else:
        print('Parameters -u|--uname and -p|--pw are both required')
        sys.exit(0)


if __name__ == '__main__':
    GetTimeTable(sys.argv[1:])

from TimeTable import TimeTable
import getopt
import sys


def main(args):
    url = 'http://www.zfjw.xupt.edu.cn/jwglxt/kbcx/xskbcx_cxXsgrkb.html'
    uname = ''
    pw = ''
    year = ''
    flag = 0
    downfile = False
    loadfile = False
    try:
        opts, args = getopt.getopt(args, 'hu:p:dd:ll:y:f:', ['uname=', 'pw=', 'downfile=', 'downfile', 'loadfile=', 'loadfile', 'year=', 'help'])
    except getopt.GetoptError:
        print('Please use -h or --help for help')
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('Usage: main.py [-u|--uname] username [-p|--pw] password [-h|--help]')
            print('Required:')
            print('\t -u username, --uname=username \t I think this is your school number')
            print('\t -p password, --pw=password \t Your password, this is very important')
            print('\t -y year, --year=year \t Which year to check')
            print('\t -f (0 | 1)  \t 0 for the first semester, 1 for the second semester')
            print('Options:')
            print('\t -d (filename), --downfile=(filename) \t This will help you download the timetable')
            print('\t -l (filename), --loadfile=(filename) \t This will help you load the timetable.json')
            print('\t (Default:filename=./file/timetable.json)')
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
        elif opt in ("-d", "--downfile"):
            downfile = arg
        elif opt in ("-l", "--loadfile"):
            loadfile = arg
    if uname and pw:
        time_table = TimeTable(url, uname, pw, year, flag)
        if loadfile is not False:
            if loadfile:
                time_table.loadfile_timetable(loadfile)
            else:
                time_table.loadfile_timetable()
        else:
            time_table.get_timetable()
        time_table.format_timetable()
    else:
        print('Parameters -u|--uname and -p|--pw are both required')
        sys.exit(0)
    if downfile is not False:
        if downfile:
            time_table.downfile_timetable(downfile)
        else:
            time_table.downfile_timetable()


if __name__ == '__main__':
    main(sys.argv[1:])

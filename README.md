# 西邮教务系统爬取课程表

---

## 简介：

之后学累的时候还会优化并且加入更多的功能！

该项目只针对西安邮电大学教务系统，其他的应该都不适用，代码也都比较简单，感兴趣的下载下来玩一玩，也可以改善更多的功能。

## 用法：

```shell
git clone https://github.com/seizer-zyx/Xupt_Timetable.git
cd Xupt_Timetable
pip install -r requirements.txt
python3 main.py -u username -p password -y 2021 -f 0
```

## 选项：

```
Usage: main.py [-u|--uname] username [-p|--pw] password [-h|--help]
Required:
         -u username, --uname=username   I think this is your school number
         -p password, --pw=password      Your password, this is very important
         -y year, --year=year    Which year to check
         -f (0 | 1)      0 for the first semester, 1 for the second semester
Options:
         -d (filename), --downfile=(filename)    This will help you download the timetable
         -l (filename), --loadfile=(filename)    This will help you load the timetable.json
         (Default:filename=./file/timetable.json)
         -h, --help      show this help message and exit
```

如果没有正确的`-y`和`-f`参数，结果是不会查询出课程表的

## 特点：

获取到了课程表的`json`数据，可以使用`-d`进行将`json`数据保存到本地，也可自行将`json`数据放到指定目录下通过`-l`加载，可提高速度。

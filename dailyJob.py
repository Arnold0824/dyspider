from datetime import date, time, datetime, timedelta
import sys
import os

def work():
    os.system('nohup scrapy crawl dy >dy.out &')
    os.system('nohup scrapy crawl kanxi >kanxi.out &')
    os.system('nohup scrapy crawl kanxitv >kanxitv.out &')


def runTask(func,tid, day=0, hour=0, min=0, second=0):
    # Init time
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    print("now:",strnow)
    # First next run time
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print("下一次执行:",strnext_time)
    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            print("start work: %s" % iter_now_time)
            a=datetime.now()
            try:
            # Call task func
                func()
            except:
                pass
            b=datetime.now()
            print("命令提交完毕")
            dura=b-a    
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            print("下次抓取: %s" % strnext_time)
            # Continue next iteration
            continue
work()

runTask(work,tid=1,day=0, hour=6, min=0)
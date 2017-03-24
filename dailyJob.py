from datetime import date, time, datetime, timedelta
import sys
import os

def work(i):
    if i==1:
        os.system('nohup scrapy crawl dy >dy.out &')
    elif i==2:
        os.system('nohup scrapy crawl kanxi >kanxi.out &')
    elif i==3:
        os.system('nohup scrapy crawl kanxitv >kanxitv.out &')
    elif i==4:
        os.system('nohup scrapy crawl bt >bt.out &')
    elif i==5:
        os.system('nohup scrapy crawl bttv >bttv.out &')

def runTask(day=0, hour=0, min=0, second=0):
    # Init time
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M')
    print("now:",strnow)
    # First next run time
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M')
    print("下一次执行:",strnext_time)
    work(4)
    x=1
    while True:
        # Get system current time

        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            print("start work: %s" % iter_now_time)
            a=datetime.now()
            try:
            # Call task func
                work(x)
            except:
                pass
            b=datetime.now()
            print("job done")
            dura=b-a    
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M')
            print("next : %s" % strnext_time)
            x+=1
            if x>5:
                x=1
            # Continue next iteration
            continue
#work()

runTask(day=0, hour=4, min=0)

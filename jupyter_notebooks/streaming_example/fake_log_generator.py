# https://github.com/kiritbasu/Fake-Apache-Log-Generator/blob/master/apache-fake-log-gen.py

#get_ipython().system('pip install tzlocal')

from faker import Faker
import time
import numpy
import glob
import random
import os
import datetime
from tzlocal import get_localzone
local = get_localzone()

faker = Faker()

timestr = time.strftime("%Y%m%d-%H%M%S")
outFileName = 'access_log_'+timestr+'.log'

response=["200","404","500","301"]

verb=["GET","POST","DELETE","PUT"]

resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]

ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

def create_log_line():
    ip = faker.ipv4()
    otime = datetime.datetime.now()
    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(local).strftime('%z')
    vrb = numpy.random.choice(verb,p=[0.6,0.1,0.1,0.2])

    uri = random.choice(resources)
    if uri.find("apps")>0:
        uri += str(random.randint(1000,10000))

    resp = numpy.random.choice(response,p=[0.9,0.04,0.02,0.04])
    byt = int(random.gauss(5000,50))
    referer = faker.uri()
    useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
    return('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"' % (ip,dt,tz,vrb,uri,resp,byt,referer,useragent))


# log rotation:
# 1. Write a set of lines to a file with timestamp in name
# 1. Increment the 

max_file_count=5
while (True):
    timestr = time.strftime("%Y%m%d-%H:%M:%S")
    outFileName = 'access_log_'+timestr+'.log'
    list_of_lines=[]
    # create the log file
    for line_indx in range(4):
        time.sleep(1)
        list_of_lines.append(create_log_line())
    # given a completed buffer, dump to file
    with open(outFileName,'w') as f:
        for line in list_of_lines:
            f.write(line+'\n')
    # remove old logs
    list_of_files=glob.glob('access_log_*.log')
    list_of_files.sort(key=str.lower) # in-place sort
    
    if (len(list_of_files)>max_file_count):
        files_to_delete = list_of_files[0:len(list_of_files)-max_file_count]
        for file_to_del in files_to_delete:
            os.remove(file_to_del)

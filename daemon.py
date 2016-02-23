import gradCafeScrapy
import time
import os
import urllib2
from multiprocessing import Process

while True:
	if os.path.isfile("result.json") == True:
		os.remove("result.json")
	p = Process(target=gradCafeScrapy.run_proc_scrapy, args=('result.json',))
	p.start()
	p.join()
	urllib2.urlopen("http://127.0.0.1:8000/results/updateDB/")
	time.sleep(60)
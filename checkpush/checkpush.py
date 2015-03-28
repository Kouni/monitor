#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
pure push channel test for NginX push Module
NginX Push Stream Module: https://github.com/wandenberg/nginx-push-stream-module
SUB: curl -s -v 'http://172.19.78.55/sub/978'
PUB: curl -s -v -X POST 'http://172.19.78.55/pub?id=978' -d 'Hello_Kitty'
'''
import http.client, urllib.request, urllib.parse, threading

host = "172.19.78.55"
channel = "999"
content = {host:channel}
getresult = ""
threadflag = "0"

class SUBSCRIBE(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        global getresult
        global threadflag
        subconn = http.client.HTTPConnection(host)
        subconn.request('GET', '/sub/'+channel)
        subresp = subconn.getresponse()
        #if subresp.reason == "OK":
        threadflag = "1"
        subdata = subresp.read()
        getresult = subdata.decode('UTF-8')
        #else:
        #    return("Connection Failure")
            #return(subdata)

count = 0
SubThread = SUBSCRIBE(1)
SubThread.start()

while (not getresult):
    pubconn = http.client.HTTPConnection(host)
    pubparams = urllib.parse.urlencode(content)
    pubconn.request('POST', '/pub?id='+channel, pubparams)
    count =count+1
    print(str(count)+" Hit!")
#SubThread.join()
pubconn.close()
if getresult.strip() == host+"="+channel:
    print('SUCCESS')
else:
    print("ERROR")
print("DONE")
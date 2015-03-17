#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
pure push channel test for NginX push Module
NginX Push Stream Module: https://github.com/wandenberg/nginx-push-stream-module
SUB: curl -s -v 'http://10.78.78.88/sub/978'
PUB: curl -s -v -X POST 'http://10.78.78.88/pub?id=978' -d 'Hello_Kitty'
'''
import http.client, urllib.request, urllib.parse, threading

host = "10.78.78.88"
channel = "978"
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
        #subdata = subresp.read()
        #getresult = subdata.decode('UTF-8')
        if subresp.reason == "OK":
            threadflag = "1"
            subdata = subresp.read()
            getresult = subdata.decode('UTF-8')
        else:
            return("Connection Failure")
            #return(subdata)

def PUBLISH():
    pubconn = http.client.HTTPConnection(host)
    pubparams = urllib.parse.urlencode(content)
    pubconn.request('POST', '/pub?id='+channel, pubparams)
    pubresp = pubconn.getresponse()
    pubdata = pubresp.read()
    print(pubresp.status, pubresp.reason)
    #return(pubdata.strip())
    pubconn.close()

SubThread = SUBSCRIBE(1)
SubThread.start()
print('啟動 Thread')
#print("FLAG",threadflag)
while (True):
    PUBLISH()
    SubThread.join()
    print("FLAG",threadflag)
    #if threadflag == "1":
    print('送出 Post')
    if getresult == host+"="+channel:
        print('SUCCESS')
    else:
        print("ERROR")
        break
    break
print("DONE")
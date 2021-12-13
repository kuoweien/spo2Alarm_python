#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 17:25:46 2021

@author: weien
"""

import requests
import pushMessage as pm
import sys
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import json

def spo2Message(): 
    def getRawList(server,XID,dateurl):
        try:
            if not dateurl:
                urlstart="http://"+server+".ym.edu.tw/"+XID
                
            if dateurl:
                urlstart="http://"+server+".ym.edu.tw/"+XID+"/"+dateurl 
        except:
            print('Error: {}. {}, line: {}'.format(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2].tb_lineno))                        
        r = requests.get(urlstart)
        rawtxt=r.text
        rawtxt=rawtxt.replace("/","-")
        rawlist=rawtxt.split("\r\n")
        return rawlist
    
    #找當下時間及其實間前五分鐘
    nowtime=datetime.datetime.now()
    #pasttime=nowtime+datetime.timedelta(days=-1)
    nowtime_str=nowtime.strftime('%Y-%m-%d %H:%M:%S')
    nowdate_str=nowtime.strftime('%Y-%m-%d')
    pasttime=nowtime+datetime.timedelta(days=-1)
    pasttime_str=pasttime.strftime('%Y-%m-%d %H:%M:%S')

    
    def spo2Alarm(XID,roomid):
        #判斷是否有當日資料
        server='xds'
        #XID='02690040'
        #XID='024E0040'
        line_message='initial'
       
        #是否有最新資料料，並在10:00及21:00提醒未量測者
        #查看是否有新上傳資料
        try:
            update=getRawList(server,XID,'')
            for i in range(len(update)):
                templist=update[i].split("  ")   
                if 'txt' not in templist[2]:
                    continue
                if 'txt' and '2021' in templist[2]:
                    newupdatetime_str=templist[0]#暫時刪掉
                    #newupdatetime_str=((templist[2].split('_')[2]).split('.')[0])
                    
                    #newupdatetime_str='2021-09-06 00:00:00'
                    url=(templist[2].split('>')[1]).split('<')[0]
                    break
        except:
            print('Error: {}. {}, line: {}'.format(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
    
        #新資料做判斷，並撈rawdatalist，沒有資料加入message
        try:
            if pasttime_str<newupdatetime_str and newupdatetime_str<nowtime_str:#期間內有新資料   
                rawlist = getRawList(server,XID,url)
            
            if newupdatetime_str<pasttime_str:
                line_message=roomid+' ('+XID+')'+u" 未量測\n"
                return line_message
    
        except:
            print('Error: {}. {}, line: {}'.format(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2].tb_lineno))        

        #比對datatime
        try:
            data_array=[]#新加入的data
           
            for i in range(len(rawlist)):
                templist=rawlist[i].split(",")
                if ";O2" in templist[0]:
                    
                    datatime_str=templist[1]
                    
                    if datatime_str<pasttime_str:
                        #alldata=0#表示沒資料

                        continue#沒有量測紀錄#暫時刪除
                    elif datatime_str>=pasttime_str:
                        #alldata=1#表示有資料
                        data_array.append([(templist[1])[11:],templist[2],templist[3],templist[4]])
            if len(data_array)==0:
                line_message=roomid+' ('+XID+')'+u" 未量測\n"
                return line_message
            lasttime=(datatime_str.split(" ")[1])[0:5]#最後量測時間       
            #刪除血氧心跳活動量不合理值
            a=len(data_array)
        except:
            line_message=roomid+' ('+XID+')'+u" 未量測\n"
            return line_message
        
        #刪除不正常值
        try:
            for i in range(a-1,-1,-1):
                spo2=data_array[i][1]
                hr=data_array[i][2]
                pa=data_array[i][3]
                if int(spo2)>=200 or int(spo2)<=40:#血氧不合理值
                    del data_array[i]
                    continue
                
                if int(hr)<=20 or int(hr)>=150:#心跳不合理值
                    del data_array[i]
                    continue  
                
                if int(pa)>=25:#活動量不合理值
                    del data_array[i]
                    continue
                if int(spo2)<60 and int(hr)>120:
                    del data_array[i]
                    continue  
                    
        except:
            print('Error: {}. {}, line: {}'.format(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        
        #Spo2平均值
        spo2_list=[]
        hr_list=[]
        for i in range(len(data_array)):
            spo2_list.append(int(data_array[i][1]))
            hr_list.append(int(data_array[i][2]))
        try:
            spo2_mean=int(round(np.mean(spo2_list)))
            hr_mean=int(round(np.mean(hr_list)))
        except:
            line_message=roomid+' ('+XID+')'+u" 資料傳輸不完整\n" #如spo2_list是空值
            return line_message
        
        #血氧判斷訊息
        try:
            if spo2_mean<=90:
                line_message=roomid+' ('+XID+')'+" SpO2="+str(spo2_mean)+", HR="+str(hr_mean)+" ("+lasttime+")"+u"血氧過低！\n"
            if spo2_mean<=94 and spo2_mean>90:
                line_message=roomid+' ('+XID+')'+" SpO2="+str(spo2_mean)+", HR="+str(hr_mean)+" ("+lasttime+")"+u" 血氧偏低！\n"
            if spo2_mean>94:
                line_message=roomid+' ('+XID+')'+" SpO2="+str(spo2_mean)+", HR="+str(hr_mean)+" ("+lasttime+")"+"\n"
        except:
            print('Error: {}. {}, line: {}'.format(sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2].tb_lineno))
        
        return line_message
    
    
    #解API接設備號及房號
    url="http://service.kylab906.com/getSPO2checkingXID"
    header={'Content-Type': 'application/json'}
    dic={"pwd":"r906r906"}
    temp=json.dumps(dic)
    r=requests.post(url,data=temp,headers=header)
    list_of_dicts = r.json()
    jsonData = list_of_dicts["data"]
    
    mess_str=''
    
    roomid='602'
    XID='028B0040'
    mess_str=mess_str+spo2Alarm(XID,roomid)
    
    for i in jsonData:
        XID=i["XID"]
        roomid=i["RoomID"]
        mess_str=mess_str+spo2Alarm(XID,roomid)
#   測試用

    print('SpO2 Check time:'+nowtime_str)
    print(mess_str)
    #pm.push_message(mess_str)
 
    return

spo2Message()
#執行排程

try:
    scheduler = BlockingScheduler()
    #scheduler.add_job(spo2Message, 'interval', hours=1,id='my_job_id')
    scheduler.add_job(spo2Message, 'cron', day_of_week='mon-sun', hour=13, minute=00)
    #scheduler.add_job(spo2Message, 'cron', day_of_week='mon-sun', hour=17, minute=00)
    #scheduler.add_job(spo2Message, 'cron', day_of_week='mon-sun', hour=22, minute=00)
    scheduler.start()
       
except KeyboardInterrupt:
        print('Interrupted')
        



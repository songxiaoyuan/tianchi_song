# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from sklearn import  linear_model
from sklearn import gaussian_process
import csv

class linearRegression ():
    def  __init__(self):
        print "this is linearRegression modal!"
        self.actionFilePath = "/home/sxy/tianchi/data/mars_tianchi_user_actions.csv"
        self.songFilePath="/home/sxy/tianchi/data/mars_tianchi_songs.csv"
        self.retPath="/home/sxy/tianchi/data/artist_day_num.csv"

    def mapDayToNumber(self, day):
        count_for_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month = int(day[4: 6])
        number = 0;
        for i in range(0, month - 1):
            number += count_for_month[i]
        number += int(day[6: 8])
        # print number
        return number

    def mapNumberToDay(self, number):
        "from 185-246 to 20150901 to 20151031"
        data ="2015"
        number = number-184
        if number<=0 | number >62:
          return data
        elif  number <31:
            #this is 9
          if number<10:
            tmp = "090"
            tmp += str(number)
            data +=tmp
            return data
          else:
            tmp = "09"
            tmp += str(number)
            data +=tmp
            return data
        else:
          number -=30
          if number<10:
            tmp = "100"
            tmp+=str(number)
          else:
            tmp="10"
            tmp+=str(number)
          data +=tmp
          return data


    def buildSongPlaytimesDic(self):
        song_playtimes_dic = dict()
        file = open(self.actionFilePath)
        for line in file:
            strings = line.split(',')
            if len(strings) != 5:
                print "dirty record!"
                continue
            song_id = strings[1]
            action_type = strings[3]
            day = self.mapDayToNumber(strings[4].replace('\n', '')) - 59
            if action_type == '1':
                if song_id not in song_playtimes_dic:
                    song_playtimes_dic[song_id] = {day: 1}
                else:
                    if day not in song_playtimes_dic[song_id]:
                        song_playtimes_dic[song_id][day] = 1
                    else:
                        song_playtimes_dic[song_id][day] += 1
        # print len(song_playtimes_dic)
        return song_playtimes_dic

    def buildArtistSongsDic(self):
        artist_songs_dic = dict()
        file = open(self.songFilePath)
        for line in file:
            strings = line.split(',')
            if len(strings) != 6:
                print "ditry record"
                continue
            song_id = strings[0]
            artist_id = strings[1]
            if artist_id not in artist_songs_dic:
                artist_songs_dic[artist_id] = set()
                artist_songs_dic[artist_id].add(song_id)
            else:
                artist_songs_dic[artist_id].add(song_id)
        # print artist_songs_dic
        return artist_songs_dic

    def getFitData(self):
   	    artist_songs_dic = self.buildArtistSongsDic()
   	    song_playtimes_dic = self.buildSongPlaytimesDic()
   	    artist_day_playnum = dict()
   	    for artist in artist_songs_dic:
   			setSong = artist_songs_dic[artist]
   			artist_day_playnum[artist] = {}
   			for song in setSong:
   				if song in song_playtimes_dic:
   				    songDic = song_playtimes_dic[song]
   				else:
   					songDic = {}
   				for day in songDic:
   					if day in artist_day_playnum[artist]:
   						artist_day_playnum[artist][day] +=songDic[day]
   					else:
   						artist_day_playnum[artist][day] = songDic[day]
   	    return artist_day_playnum

    def  lrFitFunction(self):
        artist_day_playnum = self.getFitData()
        artist_predict = dict()
        for artist in artist_day_playnum:
           datatrain_x = []
           datatest_x = []
           datatrain_y =[]
           for day in artist_day_playnum[artist]:
               tmp = []
               tmp.append(day)
               tmp.append(day*day)
               tmp.append(day*day*day)
               datatrain_x.append(tmp)
               # tmp1=[]
               # tmp1.append(artist_day_playnum[artist][day])
               datatrain_y.append(artist_day_playnum[artist][day])
           regr = linear_model.LinearRegression()
           regr.fit(datatrain_x, datatrain_y)
           # gp = gaussian_process.GaussianProcess(theta0=5, thetaL=10, thetaU=10)
           # gp.fit(datatrain_x,datatrain_y)
           for i in range(185,246):
               tmp = []
               tmp.append(i)
               tmp.append(i*i)
               tmp.append(i*i*i)
               datatest_x.append(tmp)
           artist_predict[artist] = regr.predict(datatest_x)
           # artist_predict[artist] = gp.predict(datatest_x)
           print('------------------------------------------------------------------------------\n')
           print artist_predict[artist]
           print('-----------------------------------------------------------------------\n')
        return artist_predict

    def  writeToFile(self):
      retFile = file(self.retPath,'wb')
      writer=csv.writer(retFile)
      artist_predict= self.lrFitFunction()
      for artist in artist_predict:
        predict = artist_predict[artist]
        for i in range(185,246):
          data = self.mapNumberToDay(i)
          number = int(predict[i-185])
          if number<0:
            number = 3
          writer.writerow([artist,str(number),data])
      retFile.close()

   		




if __name__ == '__main__':
    lr= linearRegression()
    # useraction.buildSongPlaytimesDic()
    # lr.lrFitFunction()
    lr.writeToFile()
    # data = lr.mapNumberToDay(245)
    # print data
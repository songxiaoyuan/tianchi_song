# -*- coding: utf-8 -*-

class UserAction ():
    def  __init__(self):
        print "user action class!"
        self.filepath = "/home/wangyu/tianchi/data/mars_tianchi_user_actions.csv"

    def mapDayToNumber(self, day):
        count_for_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month = int(day[4: 6])
        number = 0;
        for i in range(0, month - 1):
            number += count_for_month[i]
        number += int(day[6: 8])
        #print number
        return number

    def buildSongPlaytimesDic(self):
        song_playtimes_dic = dict()
        file = open(self.filepath)
        for line in file:
            strings = line.split(',')
            if len(strings) != 5:
                print "tirty record!"
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
        print len(song_playtimes_dic)
        return song_playtimes_dic


if __name__ == '__main__':
    useraction = UserAction()
    useraction.buildSongPlaytimesDic()
    #useraction.mapDayToNumber('20150815')
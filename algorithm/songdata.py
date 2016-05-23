# -*- coding: utf-8 -*-

class Song():
    def __init__(self):
        print "song class"
        self.filepath = "/home/sxy/tianchi/data/mars_tianchi_songs.csv"

    def buildArtistSongsDic(self):
        artist_songs_dic = dict()
        file = open(self.filepath)
        for line in file:
            strings = line.split(',')
            if len(strings) != 6:
                print "ditry record"
                continue
            song_id = strings[0]
            artist_id = strings[1]
            if artist_id not in artist_songs_dic:
                artist_songs_dic[artist_id] = [song_id]
            else:
                artist_songs_dic[artist_id].append(song_id)
        #print artist_songs_dic
        return artist_songs_dic

if __name__ == '__main__':
    song = Song()
    song.buildArtistSongsDic()

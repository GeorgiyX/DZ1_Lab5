from django.db import models
import psycopg2
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import math


# Create your models here.
class Tracks(models.Model):
    song_name = models.TextField()
    artist = models.TextField()
    album = models.TextField(null=True)
    genre = models.TextField()
    year_published = models.DateField()
    album_picture = models.TextField(null=True)
    song_file = models.TextField()
    likes = models.ManyToManyField(User)

    def __str__(self):
        return "Track: %s, %s, %s" % (self.song_name, self.artist, self.genre)

    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/Saved_Media/Avatar')
    play_lists = models.ManyToManyField(Tracks)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='static/Saved_Media/Avatar')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class SongComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now=True)




#Классы предметной области
class Connection:
    '''Класс для работы с подключением'''
    def __init__(self,*, dbname='Music_db', user='postgres', password='Zc%ys%aiGhgl4rve', host='localhost' ):#!!!
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.__connection = None
    @property
    def connection(self):
        return self.__connection
    def __enter__(self):
        self.connect()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dissconect()
    def connect(self):
        if not self.__connection: #!!!!
            self.__connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host = self.host)
    def dissconect(self):
        if self.__connection:
            self.__connection.close()


class Tracks_cls:
    def __init__(self, db_con):
        self.db_con = db_con.connection

    def save(self, song_name,artist, genre, year, file,album = None, album_pic = None):
        self.song_name=song_name
        self.artist= artist
        self.genre = genre
        self.year =year
        self.file = file
        self.album = album
        self.album_pic=album_pic

        cur = self.db_con.cursor()
        cur.execute("INSERT INTO \"Lab4_tracks\" (song_name, artist,album,genre,year_published,album_picture,song_file) VALUES (%s,%s,%s,%s,%s,%s,%s)",(self.song_name, self.artist, self.album, self.genre,self.year, self.album_pic, self.file))
        self.db_con.commit()
        cur.close()
    def get_all(self):
        cur = self.db_con.cursor()
        cur.execute("SELECT song_name, artist, song_file, album_picture  FROM \"Lab4_tracks\"")
        self.song_list = cur.fetchall()
        # for el in cur.fetchall():
        #     self.temp_list  = [str(e).strip() for e in el]
        #     self.song_list.append(self.temp_list)
        cur.close()
        return self.song_list
    def get_one_record(self, song, artist):
        cur = self.db_con.cursor()
        cur.execute("SELECT song_name, artist,album,genre,year_published,album_picture,song_file FROM \"Lab4_tracks\" WHERE song_name = %s and artist = %s", (song, artist))
        for element in cur.fetchall():
            self.song_data = [ str(el) for el in element]
        cur.close()
        return self.song_data

def GetTrackList():
    '''Функция добывающая необходимые значения для загрузки треков'''
    con = Connection()
    with con:
        track = Tracks_cls(con)
        first_list = track.get_all()
        splitted_list = {'list1': first_list[0:int(int(len(first_list)) / 2)], 'list2': first_list[int(int(len(first_list)) / 2):int(len(first_list))]}
        return splitted_list

def GetTrackInfo(song, artist):
    '''Функция добывающая необходимые значения для загрузки треков'''
    con = Connection()
    with con:
        track = Tracks_cls(con)
        list = track.get_one_record(song, artist)
        return list

def Save_file(file, name):
    with open('G:\Prog\Python\Files\Django_Lab5\static\{}'.format(name), 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

def paginator_for_2list(diction, on_page=5, page=1):
    total_el = max(len(diction['list1']), len(diction['list2']))
    total_page = list(range(1, math.ceil(total_el / on_page) + 1))
    final_dict = {}
    if page in total_page:
        if page*on_page <= len(diction['list1']):
            final_dict['list1'] = diction['list1'][page*on_page-on_page:page*on_page]
        else:
            final_dict['list1'] = diction['list1'][(len(diction['list1']) // on_page)*on_page :len(diction['list1']) + 1]
        if page*on_page <= len(diction['list2']):
            final_dict['list2'] = diction['list2'][page*on_page-on_page:page*on_page]
        else:
            final_dict['list2'] = diction['list2'][(len(diction['list2']) // on_page)*on_page :len(diction['list2']) + 1]
    return total_page, page, final_dict
#Test
# con = Connection()
# with con:
#     track = Tracks_cls(con)
#     track.save('This is the life','Amy Macdonald', 'pop', '1990.01.01', 'Media/Amy Macdonald - This is the life.mp3')
#     track.save('Zeitreise', 'Unheilig', 'instrumental', '2010.01.01','Media/06 - Zeitreise.mp3')
#     print(track.get_all())
#     # print(track.get_one_record('This is the life','Amy Macdonald'))
#     print (GetTrackInfo('This is the life','Amy Macdonald'))
#End Test
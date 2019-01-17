
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_Lab4.settings")
import django
django.setup()
from Lab4.models import Tracks, UserProfile,SongComment, GetTrackList
from django.contrib.auth.models import User
# cur_user = UserProfile.objects.get(user__username='ivan')
user = User.objects.get(username = 'ivan')
# track =Tracks.objects.get(artist= 'Queen')
# print(user)
# # print( list(str(el) for el in list(Tracks.objects.filter(song_name='Flower Power').values())[0]))
# print(list(Tracks.objects.get(song_name='Flower Power').likes.all().values()))

# print(
# for key, el in list(Tracks.objects.filter(song_name='Flower Power').values())[0]:
#
#
# )
# try:
#     likes = Tracks.objects.get(song_name='', artist='').likes.all()
# except:
#     print('Nothing')
#
# print(user)
# print( type(list(Tracks.objects.all().values())[0]))
# print( (list(Tracks.objects.all().values())[0]))
# key = 'song_name'
# # if 'song_name' in list(Tracks.objects.all().values())[0] and list(Tracks.objects.all().values())[0][key] =='Das Leben ist meine Religion':
# #     print('yes')
# if 'song_name' in list(Tracks.objects.get(song_name='Flower Power').likes.all().values())[0] and list(Tracks.objects.get(song_name='Flower Power').likes.all().values())[0][key] =='Das Leben ist meine Religion':
#     print('yes')
#
# print(User.objects.filter()

# print([list(el) for el in list(SongComment.objects.raw('SELECT sc.id, sc.comment, sc.date, u.username FROM "Lab4_songcomment" as sc JOIN auth_user as u ON sc.user_id = u.id WHERE sc.song_id = (SELECT tr.id FROM "Lab4_tracks" as tr WHERE tr.song_name = %s)',['You Don\'t Fool Me']))])

# track = Tracks.objects.filter(song_name='Flower Power')
# print(Tracks.objects.filter(song_name='This is the life',likes__username='ivan').count())
# print(Tracks.objects.filter(likes__username = 'ivan').count()) #Треки usera
#
# list1 = [i for i in range(20)]
# print(list1)
# print(list1[::2])
# print(list1[::-2])

# print(Tracks.objects.all()[::2])




import math

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

#=====================TEST====================
diction = {'list1': list(range(1,23)),'list2': list(range(1,24))}
print(diction)

print(paginator_for_2list(diction, page=5))









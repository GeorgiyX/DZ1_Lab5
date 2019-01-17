import os
# import eyed3
def Get2ListOfFile():
    files = os.listdir('G:\Prog\Python\Files\Django_Lab5\static\Media')
    files = list(filter(lambda x: x.endswith('.mp3'), files))
    files = list(map(lambda x: x.replace('.mp3', ''), files))
    files_2 = {'list1': files[0:int(int(len(files))/2)],'list2':files[int(int(len(files))/2):int(len(files))]}
#     return files_2
# def Mp3Info(filename):
#     route = 'G:\Prog\Python\Files\Django_Lab5\static\Media\{}.mp3'.format(str(filename))
#     audiofile = eyed3.load(route)
#     return {
#         'artist' : audiofile.tag.artist,
#         'album' : audiofile.tag.album,
#         'track_num' : audiofile.tag.track_num[0],
#         'title' : audiofile.tag.title
#     }


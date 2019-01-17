from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from Lab4 import FilesList
from django.views.generic import View
from .Forms import AddTrackForm, Comment, UserForm, ProfileForm
from .models import GetTrackList, GetTrackInfo, Connection, Tracks_cls, Save_file, Tracks, UserProfile, SongComment, paginator_for_2list
from django.contrib.auth.models import User
#Для пользователей:
from django.views.generic.edit import FormView
from .Forms import UserCreate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login, logout
from django.views.generic import ListView
#####
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator

def index(request):
    dict = FilesList.Get2ListOfFile()
    return render(request, 'index_final.html', context=dict)
def resp(request, param):
    return HttpResponse("You say:" + param)
def AboutTrack(request, name):
    diction = {'val' : name}
    diction['info'] = FilesList.Mp3Info(diction['val'])
    return render(request, 'AboutTrack.html', context=diction)
def redir(request):
    return HttpResponseRedirect("/ ")


#CBV
class IndexPage(View):
    '''CBV для главной страницы с формой'''

    def get(self, request, page =1):
        if request.user.is_authenticated:
            form = AddTrackForm()
            dict = {'form' : form}
            dict['total_page'], dict['page'], dict['songs'] = paginator_for_2list(GetTrackList(), page=page)
            return render(request, 'index_final.html', context=dict)
        else:
            return HttpResponseRedirect('/login')

    def post(self, request, page = 1):
        form = AddTrackForm(request.POST, request.FILES)
        print('\n\n\n\n Im in\n viev! \n\n\n\n')
        dict = {'form': form}
        dict['total_page'], dict['page'], dict['songs'] = paginator_for_2list(GetTrackList(), page=page)
        if form.is_valid():
            print('\n\n\n\n Form valid! \n\n\n\n')
            self.con = Connection()
            self.song_name = form.cleaned_data["song_name"]
            self.artist = form.cleaned_data["artist"]
            self.album = form.cleaned_data["album"]
            self.genre = form.cleaned_data["genre"]
            self.year = form.cleaned_data["year"]
            self.file_name = str('Saved_Media/'+self.song_name + ' - ' + self.artist+".mp3")
            Save_file(request.FILES['file'],self.file_name)
            self.pic_name = 'Saved_Media/Default.png'
            if 'album_pic' in request.FILES:
                self.pic_name = str('Saved_Media/' + self.song_name  + ' - ' +  self.artist + ".jpg")
                Save_file(request.FILES['album_pic'], self.pic_name)
            self.redirect_adress =str('music/' + self.artist + '/' + self.song_name)
            with self.con:
                track = Tracks_cls(self.con)
                track.save(self.song_name,self.artist,self.genre,self.year,self.file_name,album=self.album, album_pic=self.pic_name)
            return HttpResponseRedirect(self.redirect_adress)
        else:
            print('\n\n\n\n Im NOT VALID! BB \n\n\n\n')
            return render(request, 'index_final.html', context=dict)

class TrackPage(View):
    '''CBV для страницы с сущностью'''

    def get(self, request,artist, song ):
        if request.user.is_authenticated:
            form = Comment()
            dict = {'info' : Tracks.objects.get(song_name=song, artist=artist), 'likes' : Tracks.objects.get(song_name=song).likes.all(), 'comments' : SongComment.objects.raw('SELECT sc.id, sc.comment, sc.date, u.username FROM "Lab4_songcomment" as sc JOIN auth_user as u ON sc.user_id = u.id WHERE sc.song_id = (SELECT tr.id FROM "Lab4_tracks" as tr WHERE tr.song_name = %s)',[song]), 'form': form, 'user_like' : Tracks.objects.filter(artist=artist ,song_name=song,likes__username=request.user.username)}
            return render(request, 'TrackPage.html', context=dict)
        else:
            return HttpResponseRedirect('/login')

    def post(self,request, artist, song):
        comment = SongComment(user=User.objects.get(username=request.user.username), song=Tracks.objects.get(song_name=song, artist=artist))
        form = Comment(request.POST, instance= comment)
        dict = {'info': Tracks.objects.get(song_name=song, artist=artist),
                'likes': Tracks.objects.get(song_name=song).likes.all(), 'comments': SongComment.objects.raw(
                'SELECT sc.id, sc.comment, sc.date, u.username FROM "Lab4_songcomment" as sc JOIN auth_user as u ON sc.user_id = u.id WHERE sc.song_id = (SELECT tr.id FROM "Lab4_tracks" as tr WHERE tr.song_name = %s)',
                [song]), 'form': form, 'user_like': Tracks.objects.filter(artist=artist, song_name=song,
                                                                          likes__username=request.user.username)}

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(song)
        else:
            return render(request, 'TrackPage.html', dict)


@login_required
@transaction.atomic
def update_profile(request):
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=userprofile)
        profile_form = ProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/account')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=userprofile)
    return render(request, 'Profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })




class TrackLike(View):

    def get(self,request, artist, song):
        track = Tracks.objects.get(song_name=song, artist=artist)
        user = User.objects.get(username= request.user.username)
        if Tracks.objects.filter(artist=artist ,song_name=song,likes__username=request.user.username).count() == 0:
            track.likes.add(user)
            print("\n\n\n\nAdd like")
        else:
            user.tracks_set.remove(track)
            print("\n\n\n\nDel like")
        return HttpResponseRedirect('/music' '/' + artist + '/' + song )

class Playlist(ListView):

    model = Tracks
    template_name = 'play_list.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Playlist, self).get_context_data(**kwargs)
        if Tracks.objects.filter(likes__username = self.request.user.username).count() == 1:
            context['list1'] = Tracks.objects.filter(likes__username=self.request.user.username)
        else:
            context['list1'] = Tracks.objects.filter(likes__username = self.request.user.username)[::2]
            context['list2'] = Tracks.objects.filter(likes__username = self.request.user.username)[::-2]
        return context

#===Регистрация, Логин, Логаут===

class Registration(FormView):
    form_class = UserCreate
    success_url = '/login'
    template_name ='Registration.html'

    def form_valid(self, form):
        form.save()
        return super(Registration, self).form_valid(form)
    def form_invalid(self, form):
        return super(Registration, self).form_invalid(form)


class LogIn(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'LogIn.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LogIn, self).form_valid(form)

class LogOut(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


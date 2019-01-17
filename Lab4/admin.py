from django.contrib import admin
from Lab4.models import Tracks, Profile, SongComment

# Register your models here.
class TracksAdmin(admin.ModelAdmin):
    search_fields = ('song_name','artist', 'genre')
    list_display = ('song_name','artist', 'genre')
    list_filter = ('artist',)
    class Meta:
        model = Tracks

admin.site.register(Tracks, TracksAdmin)
admin.site.register(Profile)
admin.site.register(SongComment)
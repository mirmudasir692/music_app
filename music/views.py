from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from music.models import MusicAudio, PlayList, history, Watch_Later
from artists.models import Artist
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.core.cache import cache
from datetime import time, datetime
# Create your views here.


def Music_home(request):
    audios = cache.get('audios')
    if audios is None:
        audios = MusicAudio.objects.all()
        expires_at = time(0, 0)
        now = datetime.now().time()
        time_difference = datetime.combine(
            datetime.today(), now) - datetime.combine(datetime.today(), expires_at)
        cache_timeout = time_difference.total_seconds()
        cache.set('audios', audios, timeout=cache_timeout)
        print("cache setted")
    audios_per_page = 8
    paginator = Paginator(audios, audios_per_page)
    page = request.GET.get('page', 1)
    audios_for_page = paginator.get_page(page)
    artists = Artist.objects.all().order_by('rating')
    artists_per_page = 4
    paginator2 = Paginator(artists, artists_per_page)
    page = request.GET.get('page', 1)
    artists_for_page = paginator2.get_page(page)
    playlists = PlayList.objects.all()
    context = {'audios': audios_for_page,
               'artists': artists_for_page, 'playlists': playlists}
    return render(request, 'music/index.html', context)


def listen_music(request, id):
    audio = MusicAudio.objects.get(id=id)
    if request.user.is_authenticated:
        user = request.user
        try:
            history_audio = history.objects.get(user=user)
        except history.DoesNotExist:
            history_audio = history(user=user)
            history_audio.save()
        if audio not in history_audio.music.all():
            history_audio.music.add(audio)

        if user not in audio.viewer.all():
            audio.viewer.add(user)
            audio.views += 1
            audio.save()
    else:
        history_data = request.session.get('anonymous_history', [])
        if audio.id not in history_data:
            history_data.append(audio.id)
            request.session['anonymous_history'] = history_data

    related_audios = MusicAudio.objects.filter(catagory=audio.catagory)
    context = {'audio': audio, 'related_audios': related_audios}

    return render(request, 'music/listen_music.html', context)


def songs_of_artist(request, id):
    artist = Artist.objects.get(id=id)
    audios = MusicAudio.objects.filter(artist=artist)
    songs_per_page = 8
    paginator2 = Paginator(audios, songs_per_page)
    page = request.GET.get('page')
    audios = paginator2.get_page(page)
    artists = Artist.objects.exclude(name=artist)
    context = {'artist': artist, 'audios': audios, 'artists': artists}
    return render(request, 'music/songs_of_artist.html', context)


class Watch_laterview(View):
    def get(self, request):
        if request.user.is_authenticated:
            watch_later_instance = Watch_Later.objects.filter(
                user=request.user).first()
            if watch_later_instance is None:
                context = {}
            else:
                watch_later_audios = watch_later_instance.later_audios.all()
                audios_per_page = 8
                paginator = Paginator(watch_later_audios, audios_per_page)
                page = request.GET.get('page')
                audios_for_page = paginator.get_page(page)
                context = {'audios': audios_for_page}
        else:
            later_audios = []
            saved_later_ids = request.session.get('watch_later', [])
            for id in saved_later_ids:
                audio = MusicAudio.objects.get(id=id)
                later_audios.append(audio)
            audios_per_page1 = 8
            paginator1 = Paginator(later_audios, audios_per_page1)
            page_num1 = request.GET.get('page')
            audios_for_page1 = paginator1.get_page(page_num1)
            context = {'audios': audios_for_page1}
        return render(request, 'music/watch_later.html', context)

    def post(self, request, id):
        if request.user.is_authenticated:
            audio = MusicAudio.objects.get(id=id)
            watch_later_instance = Watch_Later.objects.filter(
                user=request.user).first()
            if watch_later_instance is None:
                watch_later_instance_create = Watch_Later.objects.create(
                    user=request.user)
                watch_later_instance_create.save()
                watch_later_instance_create.later_audios.add(audio)
            else:
                if not watch_later_instance.later_audios.filter(id=id).exists():
                    watch_later_instance.later_audios.add(audio)
                    messages.success(request, 'added to watch later')

        #  for un-authenticated users, used django session

        else:
            watch_later_data = request.session.get('watch_later', [])
            if id not in watch_later_data:
                watch_later_data.append(id)
                request.session['watch_later'] = watch_later_data

        return redirect('music:home')

    def delete(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body)
            audio_id = data['audio_id']
            audio = MusicAudio.objects.get(id=audio_id)
            watch_later_instance = Watch_Later.objects.filter(
                user=request.user).first()
            watch_later_instance.later_audios.remove(audio)
            return JsonResponse(data="", safe=False, status=200)


class PlaylistSongsView(View):
    template_name = 'music/playlist_songs.html'

    def get(self, request, id):

        playlist = PlayList.objects.get(id=id)
        playlist_songs = playlist.music_tracks.all()
        songs_per_page = 8
        paginator = Paginator(playlist_songs, songs_per_page)
        page = request.GET.get('page')
        songs_for_page = paginator.get_page(page)
        context = {'audios': songs_for_page, 'playlist': playlist}
        return render(request, self.template_name, context)


class History_of_user(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                user_history = history.objects.get(user=request.user)
                audios = user_history.music.all()
                audios_per_page = 8
                paginator = Paginator(audios, audios_per_page)
                page_num = request.GET.get('page')
                audios_for_page = paginator.get_page(page_num)

                context = {'audios': audios_for_page}
            except Exception as e:
                audios = []
                context = {'audios': audios}

        else:
            history_data = request.session.get('anonymous_history', [])
            history_audios = []
            for id in history_data:
                audio = MusicAudio.objects.get(id=id)
                history_audios.append(audio)
            audios_per_page = 8
            paginator = Paginator(history_audios, audios_per_page)
            page_num = request.GET.get('page')
            audios_for_page = paginator.get_page(page_num)
            context = {'audios': audios_for_page}
        return render(request, 'music/user_history.html', context)


def delete_history(request):
    if request.user.is_authenticated:
        user_history = history.objects.get(user=request.user)
        user_history.music.clear()
    else:
        request.session.flush()
    return redirect("music:user_history")


class SearchMusicView(View):
    def post(self, request):
        music_name = request.POST.get('music_name')
        name_string = music_name.split(" ")
        result = " ".join(name_string)
        audios = MusicAudio.objects.filter(name__icontains=result)
        audios_per_page = 8
        paginator = Paginator(audios, audios_per_page)
        page = request.GET.get('page')
        audios_for_page = paginator.get_page(page)
        artists = Artist.objects.all()
        artists_per_page = 4
        paginator1 = Paginator(artists, artists_per_page)
        page1 = request.GET.get('page')
        artists_for_page = paginator1.get_page(page1)
        context = {'audios': audios_for_page, 'artists': artists_for_page}
        return render(request, 'music/searchMusic.html', context)

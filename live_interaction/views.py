from django.shortcuts import render, HttpResponse, redirect
from music.models import MusicAudio
from django.core.paginator import Paginator
from django.views import View
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from live_interaction.models import Room
from music.models import MusicAudio
# Create your views here.


def Room_Box(request):
    rooms = Room.objects.all()
    rooms_per_page = 4
    paginator = Paginator(rooms, rooms_per_page)
    page_num = request.GET.get('page')
    room_for_page = paginator.get_page(page_num)
    context = {'rooms': room_for_page}
    return render(request, 'music/room_box.html', context)


class CreateRoomView(View):
    def get(self, request):
        audios = MusicAudio.objects.all()
        audios_per_page = 4
        paginator = Paginator(audios, audios_per_page)
        page_num = request.GET.get('page')
        audios_for_page = paginator.get_page(page_num)
        context = {'audios': audios_for_page}
        return render(request, 'music/start_room.html', context)

    def post(self, request):
        data = json.loads(request.body)
        roomName = data['roomName']
        audio_id = data['audio_id']
        print("room name :", roomName)
        print('audio id :', audio_id)
        print(request.user)
        user_room = Room.objects.filter(admin=request.user).first()
        print(user_room)

        if user_room is None:
            roomName = roomName.replace(' ', '_')
            print("it is empty")
            try:
                audio = MusicAudio.objects.get(id=audio_id)
                room = Room.objects.create(
                    name=roomName, admin=request.user, music=audio)
                room.save()
                context = {'room': room.name, 'user': room.admin.username}
                return JsonResponse("", safe=False, status=200)
            except Exception as e:
                return JsonResponse("some went wrong ", safe=False, satus=201)


class JoinRoomUserView(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        user = request.user
        username = user.username
        roomName = room.name
        context = {'roomName': roomName, 'username': username, 'room': room}
        return render(request, 'music/music_room.html', context)

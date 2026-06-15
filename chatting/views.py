from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse

import requests

from .models import *
from .forms import *
from users.views import login_required

# Create your views here.
@login_required
def create_room(request):
    if not request.user.teacher:
        messages.warning(request, 'Только для учителей')
        return redirect('users:signin')
    if request.method =='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            
            category = request.POST.get('cat')
            dificulty = request.POST.get('dificulty')
            url = 'https://opentdb.com/api_category.php'
            response = requests.get(url)
            data = response.json()
            for cat in data['trivia_categories']:
                if cat['id'] == int(category):
                    room.category = cat['name']
            room.dificulty = dificulty
            room.question = f'https://opentdb.com/api.php?amount=1&category={category}&difficulty={dificulty}'
            room.teacher = request.user
            room.save()
            return redirect('chatting:chat_room', room_id=room.id)
    else:
        form = RoomForm()
    return render(request,'create_room.html',{'form':form})


@login_required
def delete_room(request,room_id):
    room = Room.objects.filter(id=room_id).first()
    if request.user != room.teacher:
        messages.warning(request, 'Вам нельзя этого делать')
        return redirect('users:signin')
    room.delete()
    return redirect('chatting:teacher_cabinet')

@login_required
def all_rooms(request):
    if request.method =='POST':
        title = request.POST.get('title').strip()
        rooms = Room.objects.filter(category__icontains=title)
    else:
        rooms = Room.objects.all()
    return render(request,'all_rooms.html',{'rooms':rooms})

@login_required
def chat_room(request,room_id):
    room = Room.objects.filter(id=room_id).first()
    top_answers = Answer.objects.filter(room=room).order_by('right')[:3]
    return render(request,'chat.html',{'room':room,'top_answers':top_answers})

@login_required
def teacher_cabinet(request):
    rooms = Room.objects.filter(teacher=request.user)
    return render(request,'teacher_cabinet.html',{'rooms':rooms})


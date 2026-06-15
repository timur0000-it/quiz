import json
import requests

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from users.models import *
from .models import *

@sync_to_async
def update_room(room_id,user_id):
    user = CustomerUser.objects.filter(id=user_id).first()
    room = Room.objects.filter(id=room_id).first()
    if user not in room.students.all():
        room.students.add(user)
    else:
        room.students.remove(user)
@sync_to_async
def send_answer(room_id,answer,user_id):
    user = CustomerUser.objects.filter(id=user_id).first()
    room = Room.objects.filter(id=room_id).first()
    print(user_id)
    log,created = Answer.objects.get_or_create(student=user,room=room)
    log.total_count += 1
    log.right += answer
    log.save()

@sync_to_async
def get_scores(room_id):
    room = Room.objects.filter(id=room_id).first()
    top_answers = list(
    Answer.objects.filter(room=room)
    .values(
        'student__username',
        'right',
        'total_count'
    )
    .order_by('-right')[:3]
)
    return top_answers


class ChatConsumer(AsyncWebsocketConsumer):
    # Функция срабатывающая на подключение клиента к нашему серверу
    async def connect(self):
        # Записываю имя группы, куда можно отправить человека
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        user_id = self.scope["url_route"]["kwargs"]["user_id"]
        username = self.scope["url_route"]["kwargs"]["username"]
        await update_room(room_id,user_id)
        self.username = username
        self.user_id = user_id
        self.room_group_name = room_id
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Принимаем соединение
        await self.accept()
        # Функция send - это функция, которая отправляет сообщение
        # в канал веб сокета
        await self.send(text_data=json.dumps({
            'message': 'Привет, добро пожаловать к нам на сервер!'
        }))

    async def disconnect(self, close_code):
        await update_room(self.room_group_name,self.user_id)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        pass
    # Ресив - это функция, которая срабатывает, когда в канал вебсокета приходит сообщение
    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        print(1)
        if text_data_json:
            try:
                question = text_data_json['question']
                top_answers = await get_scores(self.room_group_name)
                if not question:
                    await self.send(text_data=json.dumps({ "message": "сообщение об ошибке"}))
                else:
                    response = requests.get(question)
                    data = response.json()
                    self.correct_answer = data['results'][0]['correct_answer']
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'next_question',
                            'data': data,
                            'top_answers':top_answers
                        }
                    )
            except Exception as e:
                print(e)    
            try:
                chat = text_data_json['chat']
                if not chat:
                    await self.send(text_data=json.dumps({ "message": "сообщение об ошибке"}))
                else:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': chat,
                            'user': self.username
                        }
                    )
            except Exception as e:
                print(e)
            try:
                answer = text_data_json['answer']
                if answer == None:
                    await self.send(text_data=json.dumps({ "message": "сообщение об ошибке"}))
                else:
                    if answer == 1:
                        await send_answer(self.room_group_name,answer,self.user_id)
                        await self.send(text_data=json.dumps({
                        'message': 'Правильно!'
                        }))
                    elif answer == 0:
                        await send_answer(self.room_group_name,answer,self.user_id)
                        await self.send(text_data=json.dumps({
                        'message': 'Нe правильно!'
                        }))
            except Exception as e:
                print(e) 
        else:
            await self.send(text_data=json.dumps({ "message": "сообщение об ошибке"}))
        
    async def chat_message(self,event):
        message = event['message']
        user = event['user']
        await self.send(text_data=json.dumps({
            'message':message,
            'user':user
        }))
    
    async def next_question(self,event):
        data = event['data']
        top_answers = event['top_answers']
        await self.send(text_data=json.dumps({
            'data':data,
            'top_answers':top_answers
        }))

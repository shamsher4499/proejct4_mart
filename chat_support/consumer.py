from django.shortcuts import render
from channels.consumer import AsyncConsumer
from time import sleep
import asyncio
import json
from adminpanel.models import *
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name
    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )
    await self.accept()

  async def disconnect(self, close_code):
    # Leave room group
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
  )

  async def receive(self, text_data):
    data = json.loads(text_data)
    sender = data['sender']
    receiver = data['receiver']
    message = data['message'].strip()
    room = self.room_name
    await self.save_message(room, message, sender, receiver)

    # Send message to room group
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message,
        'sender':sender,
        'receiver':receiver,
        'room':room
      }
    )
   
  # Receive message from room group
  async def chat_message(self, event):
    message = event['message']
    sender = event['sender']
    receiver = event['receiver']
    room = event['room']

    # Send message to WebSocket
    data = {
      'message': message,
      'sender': sender,
      'receiver': receiver,
      'room': room,
    }
    await self.send(text_data=json.dumps(data))
    
  @sync_to_async
  def save_message(self, room, message, sender, receiver):
    human_chat_data = HumanChatData(room_id=room, message=message)

    if eval(sender):
      human_chat_data.sender_id = sender

    if eval(receiver):
      human_chat_data.reciever_id=receiver

    human_chat_data.save()
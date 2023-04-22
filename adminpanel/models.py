from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from django.urls import reverse
from adminpanel.manager import *

class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class HumanChatRoom(models.Model):
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    support_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_user", null=True)
    query_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="query_user", null=True)

    def reply_to_customer_url(self):
        return reverse('reply_to_customer', kwargs={'room_slug': self.slug})
    
    def set_admin_to_room_url(self):
        return reverse('set_admin_to_room', kwargs={'room_slug': self.slug})

class HumanChatData(models.Model):
    room = models.ForeignKey(HumanChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_user", null=True)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciever_user", null=True, blank=True)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AIChatData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_user', null=True)
    user_input = models.CharField(max_length=255, null=True, blank=True)
    ai_response = models.TextField(null=True, default="Not Able to Respond")
    created_at = models.DateTimeField(auto_now_add=True)

class QuestionAnswer(models.Model):
    slug = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    question = models.CharField(max_length=255, null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def edit_url(self):
        return reverse('edit_question_and_answer', kwargs={'slug': self.slug})

    def delete_url(self):
        return reverse('delete_question_and_answer', kwargs={'slug': self.slug})
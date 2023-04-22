
from .openai_functions import question_from_ai
from adminpanel.models import (User, HumanChatRoom, HumanChatData, AIChatData, QuestionAnswer)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def chat_support_register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password')
        if (
                not (first_name and not first_name.isspace())
                or not (last_name and not last_name.isspace())
                or not (username and not username.isspace())
                or not (email and not email.isspace())
                or not (password and not password.isspace())
            ):
            messages.error(request, "All Field is Required")
            return redirect('chat_support_register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect('chat_support_register')
        
        user = User(email=email, first_name=first_name, last_name=last_name, username=username)
        user.set_password(password)
        user.save()
        return redirect('chat_support_login')

    template_name = "chat-support/register-and-login/signup.html"
    return render(request, template_name)
 

def chat_support_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('customer_list')
        return redirect('chat_options')

    if request.method == "POST":
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password')

        if not email or not password or email.isspace() or password.isspace():
            messages.error(request, "Email and Password is required")
            return redirect('chat_support_login')

        if not User.objects.filter(email=email).exists():
            messages.error(request, "User Doesn't Exists")
            return redirect('chat_support_login')

        user = authenticate(email=email, password=password, is_active=True)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('customer_list')
            return redirect('chat_options')
        else:
            messages.error(request, "Email and Password Didn't Match")
            return redirect('chat_support_login')

    template_name = "chat-support/register-and-login/login.html"
    return render(request, template_name)

@login_required(login_url="chat_support_login")
def chat_support_logout(request):
    logout(request)
    return redirect('chat_support_login')

@login_required(login_url="chat_support_login")
def chat_options(request):
    template_name = "chat-support/chat/options.html"
    human_chat_room = HumanChatRoom.objects.filter(query_user_id=request.user.id)
    render_data = {
        'is_room_exist': human_chat_room.exists(),
        'human_chat_room': human_chat_room.first()
    }
    return render(request, template_name, render_data)

@login_required(login_url="chat_support_login")
def chat_with_ai(request):
    template_name = "chat-support/chat/with-ai.html"
    user_id = request.user.id
    chat_data = AIChatData.objects.filter(user_id=user_id).order_by('created_at')

    if request.method == "POST":
        user_input = request.POST.get('user_input')
        ai_response = question_from_ai(user_input)

        answer = ai_response['choices'][0]['text'].strip()

        AIChatData.objects.create(user_id=user_id, user_input=user_input, ai_response=answer)
        return redirect('chat_with_ai')

    return render(request, template_name, {'chat_data': chat_data})

@login_required(login_url="chat_support_login")
def create_human_chat_room(request):
    if not request.user.is_staff and not HumanChatRoom.objects.filter(query_user_id=request.user.id).exists():
        human_chat_room = HumanChatRoom.objects.create(query_user_id=request.user.id)
        return redirect('chat_with_human', human_chat_room.slug)
        
    try:
        human_chat_room = HumanChatRoom.objects.get(query_user_id=request.user.id)
        return redirect('chat_with_human', human_chat_room.slug)
    except HumanChatRoom.DoesNotExist:
        return redirect('chat_options')

@login_required(login_url="chat_support_login")
def chat_with_human(request, room_slug):
    template_name = "chat-support/chat/with-human.html"
    try:
        chat_room = HumanChatRoom.objects.get(slug=room_slug)
        chat_data = HumanChatData.objects.filter(room_id=chat_room.id).order_by('created_at')
        questions_and_answers = QuestionAnswer.objects.filter(is_active=True)
        return render(request, template_name, {'chat_room': chat_room, 'chat_data': chat_data, 'questions_and_answers': questions_and_answers})
    except HumanChatRoom.DoesNotExist:
        return redirect('chat_options')


def coming_soon(request):
    return render(request, 'chat-support/chat/coming-soom.html')

def testing(request):
    user = authenticate(email="customer@getnada.com", password="Customer@123", is_active=True)
    login(request, user)
    return redirect('chat_with_ai')
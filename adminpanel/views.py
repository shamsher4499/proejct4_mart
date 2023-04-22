from adminpanel.models import (HumanChatRoom, HumanChatData, QuestionAnswer)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url="chat_support_login")
def customer_list(request):
    # human_chat_room = HumanChatRoom.objects.all()
    human_chat_data = HumanChatData.objects.all().order_by('created_at').last()
    if human_chat_data:
        return redirect('reply_to_customer', human_chat_data.room.slug)
    else:
        template_name = "admin/chat/no-chat.html"
        return render(request, template_name)

@login_required(login_url="chat_support_login")
def set_admin_to_room(request, room_slug):
    try:
        chat_room = HumanChatRoom.objects.get(slug=room_slug)
        chat_room.support_user_id = request.user.id
        chat_room.save()
        return redirect('reply_to_customer', room_slug)
    except HumanChatRoom.DoesNotExist:
        return redirect('customer_list')

@login_required(login_url="chat_support_login")
def reply_to_customer(request, room_slug):
    try:
        all_chat_room = HumanChatRoom.objects.all()
        chat_room = HumanChatRoom.objects.get(slug=room_slug)
        chat_data = HumanChatData.objects.filter(room_id=chat_room.id).order_by('created_at')
        template_name = "chat-support/chat/with-human.html"
        return render(request, template_name, {'chat_room': chat_room, 'chat_data': chat_data, 'all_chat_room': all_chat_room})
    except HumanChatRoom.DoesNotExist:
        return redirect('customer_list')

def question_and_answer_list(request):
    template_name = "admin/questions-and-answers/list.html"
    questions_and_answers = QuestionAnswer.objects.filter(is_active=True)
    return render(request, template_name, {'questions_and_answers': questions_and_answers})


def add_question_and_answer(request):
    template_name = "admin/questions-and-answers/add.html"
    if request.method == "POST":
        try:
            data = {
                'question': request.POST.get('question'),
                'answer': request.POST.get('answer')
            }
            QuestionAnswer.objects.create(**data)
            return redirect('question_and_answer_list')
        except:
            return render(request, template_name, data)
    return render(request, template_name)

def edit_question_and_answer(request, slug):
    template_name = "admin/questions-and-answers/edit.html"
    try:
        question_and_answer = QuestionAnswer.objects.get(slug=slug)
    except QuestionAnswer.DoesNotExist:
        return redirect('question_and_answer_list')

    if request.method == "POST":
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        question_and_answer.question = question
        question_and_answer.answer = answer
        question_and_answer.save()
        return redirect('question_and_answer_list')
    return render(request, template_name, {'question_and_answer': question_and_answer})

def delete_question_and_answer(request, slug):
    QuestionAnswer.objects.get(slug=slug).delete()
    return redirect('question_and_answer_list')
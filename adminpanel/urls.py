from django.urls import path
from . import views

urlpatterns = [
    path('customer/list/', views.customer_list, name="customer_list"),
    path('set-admin-to-room/<slug:room_slug>', views.set_admin_to_room, name="set_admin_to_room"),
    path('reply-to-customer/<slug:room_slug>', views.reply_to_customer, name="reply_to_customer"),

    path('question-and-answer/list/', views.question_and_answer_list, name="question_and_answer_list"),
    path('question-and-answer/add/', views.add_question_and_answer, name="add_question_and_answer"),
    path('question-and-answer/edit/<slug:slug>/', views.edit_question_and_answer, name="edit_question_and_answer"),
    path('question-and-answer/delete/<slug:slug>/', views.delete_question_and_answer, name="delete_question_and_answer"),
]

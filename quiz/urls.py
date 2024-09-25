from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('add/', views.quiz_add, name='quiz_add'),
    path('edit/<int:pk>/', views.quiz_edit, name='quiz_edit'),
    path('delete/<int:pk>/', views.quiz_delete, name='quiz_delete'),
    path('detail/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('question/add/<int:quiz_id>/', views.question_add, name='question_add'),
    path('question/edit/<int:question_id>/', views.question_edit, name='question_edit'),
    path('quiz/question/delete/<int:pk>/', views.question_delete, name='question_delete'),
    path('question/detail/<int:pk>/', views.question_detail, name='question_detail'),
    path('answer_option/add/<int:question_pk>/', views.answer_option_add, name='answer_option_add'),
    path('answer_option/edit/<int:pk>/', views.answer_option_edit, name='answer_option_edit'),
    path('answer_option/delete/<int:pk>/', views.answer_option_delete, name='answer_option_delete'),
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('<int:quiz_id>/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
]

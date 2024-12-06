from django.urls import path
from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
   path('', views.home , name = 'home'),
   path('quiz/', views.quiz, name= 'quiz'),
   path('api/get-quiz/', views.get_quiz, name='get_quiz'),
   path('api/submit-answer/', views.submit_answer, name='submit_answer'),
   path('results/', views.results, name='results'),
  path('api/save-answers/', views.save_answers, name='save_answers'),
  path('api/get-quiz-results/', views.get_quiz_results, name='get_quiz_results'),
 ]

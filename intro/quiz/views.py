
from django.http import HttpResponse




# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render,  redirect
from django.http import JsonResponse  
from .models import *


import random

def home(request):
    context = {'categories': Types.objects.all()}
    
    if request.GET.get('gfg'):
        return redirect(f"/quiz/?gfg={request.GET.get('gfg')}")
    
    return render(request, 'home.html', context)

def quiz(request):
    context = {'gfg': request.GET.get('gfg')}
    return render(request, 'quiz.html', context)



def get_quiz(request):
    try:
        # Todas las preguntas
        question_objs = Question.objects.all()
        
        # Filtrar las preguntas por el cuestionario
        if request.GET.get('gfg'):
            question_objs = question_objs.filter(gfg__gfg_name__icontains = request.GET.get('gfg'))
        
        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)
        
        
        for question_obj in question_objs:
            
            data.append({
                "uid" : question_obj.uid,
                "gfg": question_obj.gfg.gfg_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answer" : question_obj.get_answers(),
            })

        payload = {'status': True, 'data': data}
        
        return JsonResponse(payload)  # Return JsonResponse
        
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")

from .models import UserAnswer, Question

def submit_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user  # Asegúrate de que el usuario esté autenticado

            for answer in data['answers']:
                question_uid = answer['question_uid']
                selected_answer = answer['selected_answer']
                is_correct = answer['is_correct']
                
                # Encuentra la pregunta
                question = Question.objects.get(uid=question_uid)
                
                # Guarda la respuesta del usuario
                UserAnswer.objects.create(
                    user=user,
                    question=question,
                    answer=selected_answer,
                    is_correct=is_correct
                )

            return JsonResponse({'status': 'success', 'message': 'Respuesta recibida correctamente'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
from .models import UserAnswer

def results(request):
    # Asegúrate de que el usuario esté autenticado
    if not request.user.is_authenticated:
        return redirect('login')  # Redirigir a la página de inicio de sesión si el usuario no está autenticado
    
    # Obtiene todas las respuestas del usuario
    answers = UserAnswer.objects.filter(user=request.user)

    # Calcula el puntaje sumando las respuestas correctas
    score = sum(1 for answer in answers if answer.is_correct)

    # Obtén el total de respuestas
    total = answers.count()

    # Pasa los resultados a la plantilla
    return render(request, 'results.html', {'score': score, 'total': total})


from .models import UserAnswer
def save_answers(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user  # Asegúrate de que el usuario esté autenticado
            UserAnswer.objects.filter(user=user).delete()
            for answer in data['answers']:
                question_uid = answer['question_uid']
                selected_answer = answer['selected_answer']
                is_correct = answer['is_correct']
                
                # Encuentra la pregunta
                question = Question.objects.get(uid=question_uid)
                existing_answer = UserAnswer.objects.filter(user=user, question=question).first()
                # Guarda la respuesta del usuario
                UserAnswer.objects.create(
                    user=user,
                    question=question,
                    answer=selected_answer,
                    is_correct=is_correct
                )

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


from .models import Quiz, Answer, UserAnswer


from django.http import JsonResponse
from .models import Mark, Question
from django.contrib.auth.models import User

def get_quiz_results(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Usuario no autenticado'}, status=401)
    try:
        user = User.objects.get(id=user_id)  # Obtén el usuario por ID
        marks = Mark.objects.filter(user=user)

        score = 0
        total = marks.count()
        answers = []

        for mark in marks:
            answers.append({
                'question': mark.question.question_text,
                'is_correct': mark.is_correct
            })
            if mark.is_correct:
                score += 1

        return JsonResponse({
            'score': score,
            'total': total,
            'answers': answers
        })

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)

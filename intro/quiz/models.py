from django.db import models
import uuid
import random
from django.contrib.auth.models import User

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    
    
    class Meta:
        abstract = True

# Tipo de Cuestionario        
class Types(BaseModel):
    gfg_name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.gfg_name
    
    
# Pregunta    
class Question(BaseModel):
    gfg = models.ForeignKey(Types, related_name='gfg',on_delete= models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default = 5)
    
    def __str__(self) -> str:
        return self.question
    
    # Obtiene las respuestas para la pregunta
    def get_answers(self):
        answer_objs =  list(Answer.objects.filter(question= self))
        data = []
        random.shuffle(answer_objs)
        
        for  answer_obj in answer_objs:
            # Lista de diccionarios con "respuesta" y si es correcto o no
            data.append({
                'answer' :answer_obj.answer, 
                'is_correct' : answer_obj.is_correct
            })
        return data

# Respuestas a las preguntas   
class Answer(BaseModel):
    question = models.ForeignKey(Question,related_name='question_answer',  on_delete =models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.answer 
    
class Quiz(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField(Question, related_name='quizzes')

    def __str__(self) -> str:
        return self.title
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)  # O el tipo adecuado según las respuestas
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return f"Answer for {self.question.text} by {self.user.username}"

class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Respuesta de {self.user} a {self.question}"

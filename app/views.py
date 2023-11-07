from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

QUESTIONS = [
    {
        'id': i,
        'title': f'question {i}',
        'text': f'This is a text for question {i}'
    } for i in range(10)
]



def index(request):
    return render(request, "index.html", {'questions': QUESTIONS})

def question(request, question_id):
    item = QUESTIONS[question_id]
    answers = [
        {
            'id': i,
            'text': f'This is a text for answer {i}'
        } for i in range(10)
    ]
    return render(request, "question.html", {'question': item, 'answers': answers })

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):

    return render(request, 'ask.html')

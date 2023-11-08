import django.core.paginator
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse

QUESTIONS = [
    {
        'id': i,
        'title': f'question {i}',
        'text': f'This is a text for question {i}'
    } for i in range(100)
]

ANSWERS = [
    {
        'id': i,
        'text': f'This is a text for answer {i}'
    } for i in range(100)
]


def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    try:
        p_page = paginator.page(page)
    except django.core.paginator.EmptyPage:
        p_page = paginator.page(1)
    return [p_page, paginator.get_elided_page_range(number=p_page.number,
                                                    on_each_side=2,
                                                    on_ends=1)]


# Create your views here.
def index(request):
    page, page_range = paginate(QUESTIONS, request.GET.get('page', 1), 10)
    return render(request, "index.html", {'items': page, 'page_range': page_range})


def question(request, question_id):
    item = QUESTIONS[question_id]
    page, page_range = paginate(ANSWERS, request.GET.get('page', 1), 10)
    return render(request, "question.html", {'question': item, 'items': page, 'page_range': page_range})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')

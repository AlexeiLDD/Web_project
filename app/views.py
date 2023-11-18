import django.core.paginator
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Question, Answer, Tag, Profile, Rating


def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    p_page = paginator.get_page(page)
    return [p_page, paginator.get_elided_page_range(number=p_page.number,
                                                    on_each_side=2,
                                                    on_ends=1)]


# Create your views here.
def index(request):
    page, page_range = paginate(Question.objects.new_questions(), request.GET.get('page', 1))
    return render(request, "index.html", {'items': page, 'page_range': page_range})


def hot(request):
    page, page_range = paginate(Question.objects.hot_questions(), request.GET.get('page', 1))
    return render(request, "index.html", {'items': page, 'page_range': page_range, 'hot': True})


def tag(request, tag_id):
    tag_item = get_object_or_404(Tag.objects.all(), id=tag_id)
    page, page_range = paginate(Question.objects.tag_questions(tag_id), request.GET.get('page', 1))
    return render(request, "index.html", {'items': page, 'page_range': page_range, 'tag': tag_item})


def question(request, question_id):
    item = get_object_or_404(Question.objects.all(), id=question_id)
    page, page_range = paginate(Answer.objects.right_question_answers(item.id), request.GET.get('page', 1))
    return render(request, "question.html", {'question': item, 'items': page, 'page_range': page_range})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')


def ask(request):
    return render(request, 'ask.html')

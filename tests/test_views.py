from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from app.models import Question, Answer, Profile, Tag, Rating
from app.views import *
from app.forms import NewAnswerForm


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class HotViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('hot'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class SelfQuestionsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='secret')

    def test_self_questions_view_logged_in(self):
        request = self.factory.get(reverse('index'))
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_self_questions_view_logged_out(self):
        response = self.client.get(reverse('self_questions'))
        self.assertEqual(response.status_code, 302)


class TagViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='secret')
        self.profile = Profile.objects.create(user=self.user)

    def test_tag_view(self):
        tag_ = Tag.objects.create(tag_name='Test Tag')
        question_ = Question.objects.create(author_id=self.profile.id, head='Test Question', body='Test Body')
        question_.tags.add(tag_)
        request = self.factory.get(reverse('tag', args=[tag_.id]))
        request.user = self.user
        response = tag(request, tag_.id)
        self.assertEqual(response.status_code, 200)


class QuestionViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com',
                                                         password='secret')
        self.profile = Profile.objects.create(user=self.user)
        self.question = Question.objects.create(author=self.profile, head='Test Question',
                                                body='This is a test question')

    def test_logged_in_user_view(self):
        request = self.factory.get(reverse('question', args=[self.question.id]))
        request.user = self.user
        response = question(request, self.question.id)
        self.assertEqual(response.status_code, 200)

    def test_logged_out_user_view(self):
        request = self.factory.get(reverse('question', args=[self.question.id]))
        request.user = AnonymousUser()
        response = question(request, self.question.id)
        self.assertEqual(response.status_code, 200)

    # Дополнительные тесты для проверки POST-запросов, редиректов и обработки форм, включая проверку валидности форм

    def test_post_new_answer(self):
        request = self.factory.post(reverse('question', args=[self.question.id]), {'body': 'Test answer body'})
        request.user = self.user
        response = question(request, self.question.id)
        self.assertEqual(response.status_code, 302)  # Проверка редиректа

    def test_post_invalid_answer(self):
        request = self.factory.post(reverse('question', args=[self.question.id]), {'body': ''})  # Пустой ответ
        request.user = self.user
        response = question(request, self.question.id)

        self.assertEqual(response.status_code, 200)  # Проверка остающейся на странице при невалидной форме


class AskViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='secret')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='secret')

    def test_get_ask_view(self):
        request = self.factory.get(reverse('ask'))
        request.user = self.user
        response = ask(request)
        self.assertEqual(response.status_code, 200)

    def test_post_ask_view_valid_form(self):
        data = {
            'head': 'Test Question',
            'body': 'Test Bodydddddddddddddddddddddddddddddddddddddddddddddddd',
            'tags': 'tag1, tag2'
        }
        response = self.client.post(reverse('ask'), data=data)
        question = Question.objects.get(head='Test Question')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('question', args=[question.id]))

    def test_post_ask_view_invalid_form(self):
        data = {
            'head': 'Test Question',
            'body': 'Test Body',
            'tags': '!!@#'
        }

        response = self.client.post(reverse('ask'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'tags', 'List of tags does not meet the requirements')
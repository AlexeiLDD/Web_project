from django.test import SimpleTestCase
from django.urls import include, path, reverse, resolve
from app.views import *


class TestUrls(SimpleTestCase):
    def test_index_view_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_hot_view_is_resolved(self):
        url = reverse('hot')
        self.assertEquals(resolve(url).func, hot)

    def test_self_questions_view_is_resolved(self):
        url = reverse('self_questions')
        self.assertEquals(resolve(url).func, self_questions)

    def test_tag_view_is_resolved(self):
        url = reverse('tag', kwargs={'tag_id': 1})
        self.assertEquals(resolve(url).func, tag)

    def test_question_view_is_resolved(self):
        url = reverse('question', kwargs={'question_id': 1})
        self.assertEquals(resolve(url).func, question)

    def test_ask_view_is_resolved(self):
        url = reverse('ask')
        self.assertEquals(resolve(url).func, ask)

    def test_login_view_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_view)

    def test_logout_view_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_view)

    def test_signup_view_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)

    def test_settings_view_is_resolved(self):
        url = reverse('settings')
        self.assertEquals(resolve(url).func, settings)

    def test_vote_view_is_resolved(self):
        url = reverse('vote')
        self.assertEquals(resolve(url).func, vote)

    def test_correctness_view_is_resolved(self):
        url = reverse('correctness')
        self.assertEquals(resolve(url).func, correctness)


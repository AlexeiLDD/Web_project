from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Question, Answer, Tag, Profile, Rating

User = get_user_model()


class QuestionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='secret')
        self.profile = Profile.objects.create(user=self.user)
        self.question = Question.objects.create(author=self.profile, head='Test Question', body='Test Body')

    def test_tags_list(self):
        tag1 = Tag.objects.create(tag_name='tag1')
        tag2 = Tag.objects.create(tag_name='tag2')
        self.question.tags.add(tag1, tag2)
        tags_list = self.question.tags_list()
        self.assertEqual(len(tags_list), 2)
        self.assertIn(tag1, tags_list)
        self.assertIn(tag2, tags_list)

    def test_rating_count(self):
        rating = Rating.objects.create(profile=self.profile)
        self.question.rating.add(rating)
        self.assertEqual(self.question.rating_count(), 1)

    def test_toggle_rating(self):
        rating = Rating.objects.create(profile=self.profile)
        self.question.toggle_rating(self.profile.id)
        self.assertEqual(self.question.rating_count(), 1)
        self.question.toggle_rating(self.profile.id)
        self.assertEqual(self.question.rating_count(), 0)

    def test_check_rating(self):
        rating = Rating.objects.create(profile=self.profile)
        self.question.rating.add(rating)
        profiles = self.question.check_rating()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0], self.profile.id)

    def test_answers_count(self):
        answer1 = Answer.objects.create(author=self.profile, question=self.question, body='Answer 1')
        answer2 = Answer.objects.create(author=self.profile, question=self.question, body='Answer 2')
        self.assertEqual(self.question.answers_count(), 2)


class AnswerModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='secret')
        self.profile = Profile.objects.create(user=self.user)
        self.question = Question.objects.create(author=self.profile, head='Test Question', body='Test Body')
        self.answer = Answer.objects.create(author=self.profile, question=self.question, body='Test Answer')

    def test_rating_count(self):
        rating = Rating.objects.create(profile=self.profile)
        self.answer.rating.add(rating)
        self.assertEqual(self.answer.rating_count(), 1)

    def test_toggle_rating(self):
        rating = Rating.objects.create(profile=self.profile)
        self.answer.toggle_rating(self.profile.id)
        self.assertEqual(self.answer.rating_count(), 1)
        self.answer.toggle_rating(self.profile.id)
        self.assertEqual(self.answer.rating_count(), 0)

    def test_check_rating(self):
        rating = Rating.objects.create(profile=self.profile)
        self.answer.rating.add(rating)
        profiles = self.answer.check_rating()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0], self.profile.id)


class TagModelTests(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(tag_name='Test Tag')
        self.assertEqual(tag.tag_name, 'Test Tag')


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='secret')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_user(self):
        self.assertEqual(self.profile.user, self.user)

    def test_profile_avatar(self):
        self.assertEqual(self.profile.avatar.name, 'default-avatar.png')


class RatingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='secret')
        self.profile = Profile.objects.create(user=self.user)

    def test_rating_profile(self):
        rating = Rating.objects.create(profile=self.profile)
        self.assertEqual(rating.profile, self.profile)